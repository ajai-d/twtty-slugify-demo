---
id: gated-azure-cicd
name: Gated Azure CI/CD pipeline
version: 1
status: active
---

## When to use

EXECUTE stage, when a project has an **Azure cloud Runtime target** and needs
Infrastructure-as-code plus a CI/CD pipeline, but the **billable provision/deploy
step must stay human-gated** (for example at risk Level 1, or whenever the AI
Agent operates under Autopilot where billable cloud operations are a hard
guardrail). Captures the non-obvious pattern: keep CI green by *skipping* the
deploy job until the human explicitly enables Azure, rather than failing it.

## Applies to

- Stage tasks: **3g (CI/CD)**, **3h (IaC)**.
- Risk levels: 1 (cloud target) and up.
- Platforms: GitHub Actions + Azure (adapt the provider steps for other devtools).

## Inputs

- `{app_name}` — globally-unique Azure resource/app name.
- `{azure_service}` — target service + SKU (e.g., `App Service, Linux, Free F1`).
- `{runtime}` — runtime stack (e.g., `PYTHON|3.12`).
- `{start_command}` — app start command (e.g., gunicorn/uvicorn line).
- `{package_globs}` — files to package for deploy (e.g., `src requirements.txt`).
- `{test_command}` — how CI runs the tests (e.g., `pytest -q`).

## Prompt

```
Produce two artifacts for {app_name}, targeting {azure_service} with runtime
{runtime}:

1. infra/main.bicep — declare the {azure_service} resources only via IaC (no
   manual resource creation). Set the start command to {start_command}; output
   the app name and URL.

2. .github/workflows/deploy.yml — a pipeline with two jobs:
   - test: checkout, set up the runtime, install deps, run {test_command}.
   - deploy: needs=test; GATED — add `if: ${{ vars.AZURE_READY == 'true' }}`
     and an `environment:` so the billable provision/deploy is SKIPPED until the
     Human User enables Azure. Authenticate with azure/login via OIDC
     (client-id/tenant-id/subscription-id from repo secrets — no stored
     password), ensure the resource group, deploy infra/main.bicep, package
     {package_globs}, and deploy to {azure_service}.

Do NOT run any cloud CLI to create resources yourself. Record the one-time human
setup (OIDC federated credential + role assignment + AZURE_READY variable +
secrets) as the 3i Deploy hand-off. Keep CI green until the human enables Azure.
```

## Expected outputs

- `infra/main.bicep` (compiles with `az bicep build`).
- `.github/workflows/deploy.yml` with a `test` job and a **gated** `deploy` job
  (skipped until `AZURE_READY=true`), OIDC auth, no stored secrets in code.
- A documented human hand-off for the billable Azure enablement step.

## Provenance

Distilled from Iteration-YVIVBU (Slugify API) EXECUTE work items W-1/W-2. First
captured version.
