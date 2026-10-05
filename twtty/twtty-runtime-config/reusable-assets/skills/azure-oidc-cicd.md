---
id: azure-oidc-cicd
name: Azure OIDC CI/CD deploy (identity-first)
version: 3
status: active
---

## When to use

EXECUTE stage, when a project has an **Azure cloud Runtime target** and must
provision + deploy. Follow the TWTTY cloud contract (sdlc §7.1.7 Identity and
access controls; `config/cloud/azure.md`): **all provisioning/deploy runs in the
CI/CD pipeline** — dev-machine `az` / portal / `azd up` are prohibited except the
one-time identity bootstrap. Authentication is **GitHub OIDC → Entra workload
identity federation**, so there are **no client secrets in CI** and **nothing to
do per run** once the federation exists.

This is why the reference projects deploy with no manual per-run steps: the
federated credential is created once by an identity-bootstrap work item, then
every push deploys via OIDC.

## The pattern (per sdlc "Identity before code")

1. **`W-<n>-identity-bootstrap` work item — sequenced before any deploy work item**
   (plan §3.2). It performs the one-time, out-of-band trust that IaC cannot
   self-bootstrap: create the Entra app / user-assigned managed identity, add a
   **GitHub OIDC federated credential** for the repo's deploy ref/environment,
   and assign least-privilege RBAC. Documented in **plan §1.4 Security
   architecture**. (This is the ONLY step allowed outside CI.)
2. **IaC (3h)** declares all resources **and** the RBAC role assignments at
   resource-group / single-resource scope (not portal-added); app-runtime auth is
   **managed identity**; disable shared-key/local auth where supported.
3. **CI/CD (3g→3i)** deploy job authenticates with `azure/login` via **OIDC**
   (`permissions: id-token: write`; client-id/tenant-id/subscription-id are
   **identifiers, not secrets** — no long-lived password), runs the IaC, and
   deploys. Runs automatically on push; no stored secret, no manual step.

## Applies to

- Stage tasks: **3h (IaC + RBAC)**, **3g (CI/CD)**, **3i (Deploy)**, plus a
  `W-<n>-identity-bootstrap` sequenced first.
- Risk levels: §7.1.7 is MUST at **L2+** (a real cloud deploy); at L1 it is
  optional but this is still the correct shape when deploying to Azure.

## Inputs

- `{app_name}`, `{azure_service}` (+ SKU), `{runtime}`, `{start_command}`,
  `{package_globs}`, `{test_command}`, `{health_path}`.
- `{deploy_subject}` — the OIDC federated-credential subject (e.g.
  `repo:<owner>/<repo>:ref:refs/heads/main` or `:environment:<env>`).

## Prompt

```
Deploy {app_name} to {azure_service} ({runtime}) the TWTTY way (config/cloud/azure.md):

1. Plan a W-<n>-identity-bootstrap work item, sequenced BEFORE deploy in
   plan §3.2 and documented in plan §1.4: create the Entra app / managed
   identity, add a GitHub OIDC federated credential for {deploy_subject}, and a
   least-privilege RBAC role assignment. This one-time trust is the only step
   outside CI.

2. infra/main.bicep — declare resources AND RBAC role assignments (resource-group
   scope); app-runtime uses a managed identity; set start command {start_command}.

3. .github/workflows/deploy.yml — on push to main, permissions: id-token: write,
   contents: read. Jobs: test ({test_command}); deploy (needs=test) uses
   azure/login@v2 OIDC with client-id/tenant-id/subscription-id (identifiers, not
   secret passwords), azure/arm-deploy what-if + deploy of infra/main.bicep,
   package {package_globs}, deploy, then smoke-check {health_path}.

Do NOT run dev-machine az/portal/azd deploys — all provisioning/deploy is via the
pipeline. No long-lived client secrets in CI. Add a deploy-your-own-copy README
section (one-time identity setup, deploy, verify, teardown).
```

## Expected outputs

- A `W-<n>-identity-bootstrap` work item (plan §1.4 + §3.2, sequenced first).
- `infra/main.bicep` with resources + least-privilege RBAC (compiles).
- `.github/workflows/deploy.yml` — OIDC login (`id-token: write`, **no secrets
  password**), what-if + deploy + smoke; auto-deploys on push.
- Deployment README (one-time identity setup / deploy / verify / teardown).

## Provenance

v1/v2 — initial captures from Iteration-YVIVBU; WRONG — framed deploy as a manual
human-gated hand-off with CI secrets.
v3 — corrected against the TWTTY spec on `main`: `config/cloud/azure.md` ("all
deploy via CI/CD; dev-machine az prohibited"; "GitHub OIDC → Entra workload
identity federation, no client secrets in CI") and sdlc "Identity before code"
(one-time `W-<n>-identity-bootstrap` sequenced before deploy, documented in
plan §1.4). OIDC federation is why there are no per-run manual steps.
