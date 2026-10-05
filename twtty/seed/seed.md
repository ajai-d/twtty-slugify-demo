## What I Want To Build

A tiny "Slugify" web API: a single HTTP service that turns a text string into a
URL-friendly slug (lowercase, spaces and punctuation collapsed to single
hyphens, trimmed of leading/trailing hyphens). It is for developers who want a
quick, hosted slug utility they can call from scripts or other services.

## Done Looks Like

- `GET /slugify?text=Hello, World!` returns `{"slug": "hello-world"}`
- A health endpoint `GET /healthz` returns HTTP 200
- Automated tests cover the slug rules (spaces, punctuation, casing, unicode,
  empty input) and all pass
- The service is deployed and reachable on Azure, provisioned and deployed by a
  CI/CD pipeline that runs on push to `main` (no manual resource creation)
- Anyone can clone the repo and run the service and its tests locally
