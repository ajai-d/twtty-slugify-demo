---
id: azure-oidc-cicd
name: Azure OIDC CI/CD pipeline
version: 2
status: active
---

## When to use

EXECUTE stage, when a project has an **Azure cloud Runtime target** and needs
Infrastructure-as-code plus a CI/CD pipeline that **provisions and deploys
automatically** on push. Authentication uses **OIDC federated credentials** —
no stored passwords and, once the one-time federation is in place for the repo
owner, **no manual per-run or per-repo steps**. This is how the reference
projects deploy (e.g. `ajai-d/support-agent`): the three `AZURE_*` secrets + a
federated credential are configured once, and every push just deploys.

**Optional gate:** when the AI Agent must honor a hard guardrail (e.g. operating
under Autopilot on a project where the owner has *not* yet federated), gate the
deploy job behind `if: ${{ vars.AZURE_READY == 'true' }}` so CI stays green until
the human flips the switch. Drop the gate once federation is set up (the common
case) so deploy is fully automatic.

## Prerequisite (one-time per owner/tenant — "done before")

- An Entra app registration or user-assigned managed identity with a **federated
  credential** whose subject matches the deploying repo/branch/environment
  (a per-owner wildcard subject covers all the owner's repos).
- That identity has a role assignment (e.g. Contributor) on the target scope.
- Repo (or org) secrets `AZURE_CLIENT_ID`, `AZURE_TENANT_ID`,
  `AZURE_SUBSCRIPTION_ID` referencing it.

The AI Agent does NOT create these via CLI; they are provisioned once by the
owner. A brand-new repo only needs the three secrets set and its subject added
to the federated credential.

## Applies to

- Stage tasks: **3g (CI/CD)**, **3h (IaC)**, **3i (Deploy)**.
- Risk levels: 1 (cloud target) and up.
- Platforms: GitHub Actions + Azure.

## Inputs

- `{app_name}` — globally-unique Azure resource/app name.
- `{azure_service}` — target service + SKU (e.g., `App Service, Linux, Free F1`).
- `{runtime}` — runtime stack (e.g., `PYTHON|3.12`).
- `{start_command}` — app start command (e.g., gunicorn/uvicorn line).
- `{package_globs}` — files to package for deploy (e.g., `src requirements.txt`).
- `{test_command}` — how CI runs the tests (e.g., `pytest -q`).
- `{health_path}` — endpoint to smoke-test after deploy (e.g., `/healthz`).

## Prompt

```
Produce two artifacts for {app_name}, targeting {azure_service} with runtime
{runtime}:

1. infra/main.bicep — declare the {azure_service} resources via IaC only (no
   manual resource creation). Set the start command to {start_command}; output
   the app name and URL.

2. .github/workflows/deploy.yml — on push to main (plus workflow_dispatch), with
   `permissions: id-token: write, contents: read`:
   - test job: checkout, set up {runtime}, install deps, run {test_command}.
   - deploy job (needs=test): authenticate with
     azure/login@v2 via OIDC using client-id/tenant-id/subscription-id from the
     AZURE_CLIENT_ID / AZURE_TENANT_ID / AZURE_SUBSCRIPTION_ID secrets (no stored
     password). Run azure/arm-deploy@v2 twice — a `--what-if` preview then the
     real deploy of infra/main.bicep — package {package_globs}, deploy to
     {azure_service}, then curl {health_path} as a smoke check.

Deploy runs automatically on push (OIDC federation is set up once per owner — see
Prerequisite). Only add `if: ${{ vars.AZURE_READY == 'true' }}` + an
`environment:` on the deploy job when the owner has NOT yet federated and the
billable step must stay human-gated. Do NOT run any cloud CLI to create
resources yourself — the pipeline provisions via Bicep.
```

## Expected outputs

- `infra/main.bicep` (compiles with `az bicep build`).
- `.github/workflows/deploy.yml` — `test` + `deploy` jobs, `id-token: write`,
  azure/login OIDC (no stored password), arm-deploy what-if + deploy, post-deploy
  smoke check. Auto-deploys on push once federation + the three secrets exist;
  optional `AZURE_READY` gate only until then.

## Provenance

v1 — distilled from Iteration-YVIVBU (Slugify API), gated-deploy variant.
v2 — refined against the reference pattern on `ajai-d/support-agent` main
branch: OIDC federated login with the three `AZURE_*` secrets deploys
automatically (no manual per-run steps); gating demoted to an optional
pre-federation safety. Renamed from `gated-azure-cicd` to `azure-oidc-cicd` to
reflect the primary (automatic OIDC) pattern.
