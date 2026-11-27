#!/usr/bin/env python3
"""Opt-in local JSONL diagnostics. Records execution, never invents agent/tool results."""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
from functools import wraps
import inspect
import json
import os
from pathlib import Path
import re
import signal
import stat
import subprocess
import sys
import tempfile
import time
import uuid

STATE = '.aidw-debug'
_RUN_ID = uuid.uuid4().hex
_SECRET = re.compile(r'(?i)(?:password|passwd|token|secret|api[-_]?key|authorization|cookie|credential)')
_SAFE_FIELDS = {'preset', 'workflowPreset', 'stages', 'parentStages', 'action', 'recordPath',
                'record_dir', 'status', 'readiness', 'planning', 'resume', 'require_critique', 'ok', 'created'}


def project_root(value=None) -> Path:
    explicit = value or os.getenv('AIDW_PROJECT_ROOT')
    if explicit:
        root = Path(explicit).expanduser().resolve(strict=True)
    else:
        root = Path.cwd().resolve()
        for parent in (root, *root.parents):
            if (parent / STATE / 'config.json').exists():
                root = parent
                break
    if not root.is_dir():
        raise ValueError('project root must be an existing directory')
    return root


def state_dir(root: Path, create=False) -> Path:
    # Compare physical paths, including when a caller supplies a symlinked root.
    root = project_root(root)
    folder = root / STATE
    if folder.is_symlink():
        raise ValueError('debug directory cannot be a symlink')
    if folder.resolve().parent != root:
        raise ValueError('debug directory escapes project')
    if create:
        folder.mkdir(mode=0o700, exist_ok=True)
    if create and not (folder / '.gitignore').exists():
        with (folder / '.gitignore').open('x', encoding='utf-8') as ignore:
            ignore.write('*\n')
    return folder


def settings(root: Path) -> bool:
    override = os.getenv('AIDW_LOG')
    if override is not None:
        if override.lower() in {'0', 'off', 'false'}:
            return False
        if override.lower() in {'1', 'on', 'true'}:
            return True
        raise ValueError('AIDW_LOG must be on/off or 1/0')
    config = state_dir(root) / 'config.json'
    if config.is_symlink():
        raise ValueError('logging config cannot be a symlink')
    if not config.exists():
        return False
    if config.stat().st_size > 4096:
        raise ValueError('logging config is too large')
    value = json.loads(config.read_text(encoding='utf-8'))
    if not isinstance(value, dict) or type(value.get('enabled')) is not bool:
        raise ValueError('logging config requires enabled: true/false')
    return value['enabled']


def redact(value):
    """Best-effort defence, not a guarantee for arbitrary free text. No outputs are logged."""
    if isinstance(value, dict):
        return {str(k): '[REDACTED]' if _SECRET.search(str(k)) else redact(v)
                for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [redact(v) for v in value]
    if isinstance(value, str):
        value = re.sub(r'(?i)(Bearer\s+)\S+', r'\1[REDACTED]', value)
        value = re.sub(r'(?i)((?:password|passwd|token|secret|api[-_]?key|authorization|cookie|credential)[\w-]*\s*[=:]\s*)[^\s&,;]+', r'\1[REDACTED]', value)
        value = re.sub(r'(https?://)[^\s/@]+:[^\s/@]+@', r'\1[REDACTED]@', value)
        value = re.sub(r'(https?://[^\s?#]+)[?#][^\s]+', r'\1?[REDACTED]', value)
        return value[:2000]
    if value is None or isinstance(value, (int, float, bool)):
        return value
    return redact(str(value))


def safe_argv(argv):
    result, mask = [], False
    for arg in argv:
        if mask:
            result.append('[REDACTED]'); mask = False
        elif arg in {'-c', '-e', '--eval', '--text', '--prompt', '--input'}:
            result.append(arg); mask = True
        elif arg.startswith('-') and _SECRET.search(arg.split('=', 1)[0]):
            result.append(arg.split('=', 1)[0] + ('=[REDACTED]' if '=' in arg else ''))
            mask = '=' not in arg
        else:
            result.append(redact(arg))
    return result


def _append(root: Path, payload: dict) -> None:
    folder = state_dir(root, create=True)
    path = folder / 'events.jsonl'
    if path.is_symlink():
        raise ValueError('debug log cannot be a symlink')
    data = (json.dumps(redact(payload), ensure_ascii=False, separators=(',', ':')) + '\n').encode('utf-8')
    flags = os.O_WRONLY | os.O_CREAT | os.O_APPEND | getattr(os, "O_NONBLOCK", 0) | getattr(os, 'O_NOFOLLOW', 0)
    fd = os.open(path, flags, 0o600)
    try:
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            raise ValueError('debug log must be a regular file')
        # Lock a single complete JSONL record on Unix; children share this append-only log.
        if os.name == 'posix':
            import fcntl
            fcntl.flock(fd, fcntl.LOCK_EX)
        with os.fdopen(fd, 'ab', closefd=False) as stream:
            stream.write(data); stream.flush()
    finally:
        os.close(fd)


def emit(event: str, *, root=None, source='helper', **fields) -> bool:
    """Best-effort diagnostics must never turn a failed operation into a pass or break it."""
    try:
        resolved = project_root(root)
        if not settings(resolved):
            return False
        payload = {'schema': 'aidw-debug/v1', 'eventId': uuid.uuid4().hex,
                   'time': datetime.now(timezone.utc).isoformat(),
                   'runId': os.getenv('AIDW_RUN_ID') or _RUN_ID,
                   'pid': os.getpid(), 'source': source, 'event': event,
                   'preset': os.getenv('AIDW_PRESET'), 'record': os.getenv('AIDW_RECORD'),
                   **fields}
        _append(resolved, payload)
        return True
    except (OSError, ValueError, TypeError) as exc:
        print(f'[aidw-debug] event not recorded ({type(exc).__name__}); operation unchanged', file=sys.stderr)
        return False


def traced(event):
    """Instrument a real helper call; do not log source text, returned data or secrets."""
    def decorate(function):
        signature = inspect.signature(function)
        @wraps(function)
        def wrapped(*args, **kwargs):
            bound = signature.bind_partial(*args, **kwargs).arguments
            root = bound.get('project_root') or bound.get('workspace_root')
            try:
                enabled = settings(project_root(root))
            except (OSError, ValueError):
                # emit() reports configuration trouble without changing task behaviour.
                enabled = None
            if enabled is False:
                return function(*args, **kwargs)
            fields = {k: v for k, v in bound.items() if k in _SAFE_FIELDS}
            if 'selected_preset' in bound:
                fields['preset'] = bound['selected_preset']
            if 'record' in bound:
                fields['record'] = str(bound['record'])
            span_id = uuid.uuid4().hex
            start = time.monotonic()
            emit(event + '.start', root=root, spanId=span_id, **fields)
            try:
                result = function(*args, **kwargs)
            except BaseException as exc:
                emit(event + '.finish', root=root, spanId=span_id,
                     outcome='failed', errorType=type(exc).__name__,
                     durationMs=round((time.monotonic()-start)*1000, 3), **fields)
                raise
            result_fields = {k: v for k, v in result.items() if k in _SAFE_FIELDS} if isinstance(result, dict) else {}
            emit(event + '.finish', root=root, spanId=span_id, outcome='failed' if isinstance(result, dict) and result.get('ok') is False else 'success',
                 durationMs=round((time.monotonic()-start)*1000, 3), **{**fields, **result_fields})
            return result
        return wrapped
    return decorate


def configure(root: Path, enabled: bool) -> None:
    folder = state_dir(root, create=True)
    config = folder / 'config.json'
    if config.is_symlink():
        raise ValueError('logging config cannot be a symlink')
    fd, tmp = tempfile.mkstemp(prefix='.config-', dir=folder)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as stream:
            json.dump({'enabled': enabled}, stream); stream.write('\n')
        os.replace(tmp, config)
    finally:
        if os.path.exists(tmp): os.unlink(tmp)
    ignore = folder / '.gitignore'
    if not ignore.exists():
        with ignore.open('x', encoding='utf-8') as stream: stream.write('*\n')


def run_command(args, root):
    argv = args.command[1:] if args.command[:1] == ['--'] else args.command
    if not argv:
        raise ValueError('run requires a command after --')
    env = os.environ.copy()
    env['AIDW_PROJECT_ROOT'] = str(root)
    env['AIDW_RUN_ID'] = args.run_id or env.get('AIDW_RUN_ID') or _RUN_ID
    if args.preset: env['AIDW_PRESET'] = args.preset
    if args.record: env['AIDW_RECORD'] = args.record
    # Apply the same correlation to this process and its child.
    for key in ('AIDW_PROJECT_ROOT','AIDW_RUN_ID','AIDW_PRESET','AIDW_RECORD'):
        if key in env: os.environ[key] = env[key]
    span_id = uuid.uuid4().hex
    cwd = Path(args.cwd).expanduser().resolve(strict=True) if args.cwd else root
    if not cwd.is_dir(): raise ValueError('cwd must be an existing directory')
    fields = {'spanId': span_id, 'argv': safe_argv(argv), 'cwd': str(cwd), 'step': args.step}
    emit('command.start', root=root, source='runner', **fields)
    started = time.monotonic(); outcome = 'failed'; code = 127; child = None
    try:
        child = subprocess.Popen(argv, cwd=cwd, env=env, start_new_session=os.name == 'posix')
        code = child.wait(timeout=args.timeout)
        outcome = 'success' if code == 0 else 'failed'
    except (subprocess.TimeoutExpired, KeyboardInterrupt) as exc:
        if child is not None:
            if os.name == 'posix': os.killpg(child.pid, signal.SIGTERM)
            else: child.terminate()
            try: child.wait(timeout=3)
            except subprocess.TimeoutExpired:
                if os.name == 'posix': os.killpg(child.pid, signal.SIGKILL)
                else: child.kill()
                child.wait()
        code = 124 if isinstance(exc, subprocess.TimeoutExpired) else 130
        outcome = 'timeout' if code == 124 else 'interrupted'
    except OSError as exc:
        print(f'Unable to execute command ({type(exc).__name__})', file=sys.stderr)
    finally:
        emit('command.finish', root=root, source='runner', outcome=outcome,
             exitCode=code, durationMs=round((time.monotonic()-started)*1000,3), **fields)
    return 128-code if code < 0 else code


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='action', required=True)
    for name in ('enable','disable','status','run','event'):
        p = sub.add_parser(name)
        p.add_argument('--project-root', default=None)
        if name in ('run','event'):
            p.add_argument('--run-id'); p.add_argument('--preset'); p.add_argument('--record')
        if name == 'run':
            p.add_argument('--step'); p.add_argument('--timeout', type=float); p.add_argument('--cwd')
            p.add_argument('command', nargs=argparse.REMAINDER)
        if name == 'event':
            p.add_argument('--kind', choices=['stage','agent','tool','task'], required=True)
            p.add_argument('--phase', choices=['start','finish','blocked'], required=True)
            p.add_argument('--name', required=True); p.add_argument('--call-id')
            p.add_argument('--outcome', choices=['success','failed','blocked','unverified'])
            p.add_argument('--evidence')
            p.add_argument('--source', choices=['host-report','test-adapter'], default='host-report')
    args = parser.parse_args()
    try:
        root = project_root(args.project_root)
        if args.action in ('enable','disable'):
            configure(root, args.action == 'enable')
        if args.action in ('enable','disable','status'):
            print(json.dumps({'enabled': settings(root), 'projectRoot': str(root),
                              'logPath': str(root/STATE/'events.jsonl'),
                              'configPath': str(root/STATE/'config.json')}))
            return 0
        if args.action == 'run':
            if args.timeout is not None and args.timeout <= 0:
                raise ValueError('timeout must be positive')
            return run_command(args, root)
        if args.kind in ('agent','tool') and args.phase != 'blocked' and not args.call_id:
            raise ValueError('agent/tool events require the actual host call ID')
        if args.phase == 'finish' and (not args.outcome or not args.evidence):
            raise ValueError('finish events require outcome and an actual evidence locator')
        if args.run_id: os.environ['AIDW_RUN_ID'] = args.run_id
        emitted = emit(args.kind+'.'+args.phase, root=root, source=args.source,
                       name=args.name, callId=args.call_id, outcome=args.outcome,
                       evidence=args.evidence, preset=args.preset, record=args.record)
        print(json.dumps({'recorded': emitted, 'source': args.source}))
        return 0 if emitted or not settings(root) else 2
    except (OSError, ValueError) as exc:
        parser.exit(2, str(exc)+'\n')


if __name__ == '__main__':
    raise SystemExit(main())
