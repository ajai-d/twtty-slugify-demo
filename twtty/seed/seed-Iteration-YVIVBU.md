## What I want to do

Stand up the first working version of the Slugify API and ship it to Azure
through an automated pipeline, scoped within the project seed.

This baseline iteration delivers:

- The slug conversion logic and its rules (casing, spaces, punctuation,
  unicode, trimming, empty input).
- An HTTP API exposing `GET /slugify?text=...` and `GET /healthz`.
- Automated tests for the slug rules and the endpoints.
- Infrastructure-as-code (Bicep) describing the Azure target.
- A CI/CD pipeline (GitHub Actions) that tests, provisions, and deploys on push
  to `main` — no manual resource creation.

## What done looks like

- `GET /slugify?text=Hello, World!` returns `{"slug": "hello-world"}`.
- `GET /healthz` returns HTTP 200.
- All slug-rule and endpoint tests pass locally and in CI.
- The pipeline provisions the Azure App Service (Free F1) via Bicep and deploys
  the app; the running service is reachable at its Azure URL.
- The repo can be cloned and run locally with a documented command.

> Scope note: this is the baseline iteration. Later iterations build on this
> spec, plan, and code rather than replacing them.
