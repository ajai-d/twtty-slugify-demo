# Plan — Iteration-YVIVBU · Slugify API

Builds on the baseline spec (`spec-Iteration-YVIVBU.md`). First iteration — nothing prior to extend.

## 1. Architecture

- **Runtime:** Python 3.11, FastAPI app served by Uvicorn/Gunicorn on Azure App
  Service (Linux, Free F1).
- **Shape:** single stateless web process; no datastore, no auth, no secrets.
- **Delivery:** GitHub Actions on push to `main` → run tests → authenticate to
  Azure (OIDC) → provision via Bicep (`infra/main.bicep`) → deploy app code.
- **Provisioning:** Infrastructure-as-code (Bicep) is the only way resources are
  created; no manual `az` resource creation.

## 2. Design

- `src/app/slugify.py` — pure `slugify(text: str) -> str` implementing the spec
  §4 rules (NFKD normalize, lowercase, collapse non-alphanumerics to single
  hyphen, trim).
- `src/app/main.py` — FastAPI app: `GET /slugify?text=` and `GET /healthz`.
- `tests/test_slugify.py` — unit tests for the slug rules (AC-1..4).
- `tests/test_api.py` — endpoint tests via FastAPI TestClient (AC-5..7).
- `requirements.txt` — fastapi, uvicorn/gunicorn, httpx (TestClient), pytest.
- `infra/main.bicep` — App Service plan (F1) + Linux web app (Python runtime).
- `.github/workflows/deploy.yml` — test + provision + deploy pipeline.
- `README.md` — run-locally + architecture summary.

## 3. Work breakdown

### 3.1 Work items

- **W-1 — App + tests.** Implement `slugify()` and the FastAPI endpoints; add
  unit + API tests covering AC-1..7. Definition of done: all tests pass locally.
- **W-2 — IaC + CI/CD.** Add `infra/main.bicep` and `.github/workflows/deploy.yml`
  that tests, provisions (Bicep), and deploys to Azure App Service on push to
  `main`. Definition of done: workflow is valid; the billable provision/deploy
  step is gated to the Human User (entry 003).

### 3.2 Dependencies (DAG)

- W-1 → W-2 (the pipeline deploys the app produced by W-1).
- Not DAG-independent → Parallel not eligible.

## 4. Execution pattern

**Sequential** (W-1 then W-2); W-2 depends on W-1, so Parallel is ineligible.
Both work items bundle onto one short-lived branch with a single PR
(bundle-by-default, sdlc §5.1); EXECUTE goes through a branch + PR per sdlc §9.

## 5. Acceptance-criteria → work-item mapping

| AC | Work item | Verified at |
|---|---|---|
| AC-1..4 | W-1 | `tests/test_slugify.py` (3f) |
| AC-5..7 | W-1 | `tests/test_api.py` (3f) |
| BR-3 deploy | W-2 | pipeline provision+deploy (3g/3h/3i), human-gated |
