#!/usr/bin/env python3
"""Compatibility entry for existing XR commands; use loop_checklist for new work."""
from loop_checklist import *  # Re-export the unchanged checkpoint/accounting API.

if __name__ == "__main__":
    raise SystemExit(main())
