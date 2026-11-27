# WordPress and WooCommerce

Use WordPress and commerce-specific lifecycle, data, permissions and compatibility checks.

Read the [shared specialist contract](../references/specialist-contract.md).
This profile is a domain lens for existing stages, not a separate workflow or native agent registration.
Assessment and review are read-only; code writes require assignment by the selected execution stage.

## Use and exclude

- Use when: A WordPress theme, plugin, block, REST integration or WooCommerce extension is in scope.
- Use when: Content storage, custom checkout/order behaviour or PHP/JavaScript integration depends on WordPress.
- Exclude: Only WHMCS is affected; there is no WordPress/WooCommerce component or integration.
- Exclude: The project has no WordPress runtime or compatibility requirement.

## Discover the actual environment

- Classify the checkout as a plugin, theme, block theme, core tree or complete site.
- Read actual WordPress, PHP and WooCommerce version constraints from source and tooling.
- Locate bootstrap, hooks, routes, capabilities, templates and data access paths.
- Check single-site/multisite, storage mode and enabled extensions only when they affect scope.
- Identify the repository's PHPCS, PHPStan, PHPUnit, JavaScript and integration workflows.
- Read existing migrations and uninstall policy before changing persisted settings or orders.

## Domain techniques

- Use the host's supported hooks and APIs; avoid editing core or recreating its lifecycle.
- Keep authentication, authorisation and CSRF checks distinct at affected entry points.
- Validate input and escape output for its context; use supported parameterised data access.
- Make activation and upgrades repeatable and keep destructive uninstall behaviour explicit.
- Use version-matched WooCommerce CRUD/storage APIs for order or product changes.
- Keep admin-only behaviour and assets scoped to their intended surface.
- Check cron/background operations for duplicates, retries and partial failure.
- Reuse existing PHP/JS build and formatting conventions rather than imposing a new stack.

## Stage handoff

Contribute the domain section to the selected stage's existing artefact and shared task record.

| Stage | Required contribution |
| --- | --- |
| Discover | Host/version matrix, entry points, storage ownership and relevant risk paths. |
| Plan | Hook/API choices, migration steps and user-visible acceptance cases. |
| Execute | Only assigned extension/theme changes; preserve store data and deployment boundaries. |
| Verify | Runtime loading, changed flows, denied requests and targeted lifecycle/data evidence. |

## Acceptance evidence

- The changed extension loads and behaves on the declared WordPress/PHP/WooCommerce versions.
- Relevant authorised and unauthorised requests behave correctly.
- Lifecycle and data changes preserve existing site/store behaviour and intended data.

## Existing capability integration

- Apply official WordPress skills selectively and honour the detected compatibility range.
- Use the WordPress page or article builder only when that plugin owns the requested deliverable.
- Combine content-seo for metadata generation and database for material schema changes.
- Use the shared security stage for findings; this lens does not create another audit pipeline.

## Failure modes

- Do not treat a nonce as permission to perform an action.
- Do not apply a current upstream API to an older installation without checking support.
- Do not assume WooCommerce's small Abilities API skill covers every commerce integration.
- Do not claim live-store verification from a local syntax check or mocked request.
