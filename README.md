# Slugify API

A tiny HTTP service that converts text into a URL-friendly slug. Built with
FastAPI and deployed to Azure App Service by a GitHub Actions pipeline. Produced
with the TWTTY methodology — process artifacts live under [`twtty/`](twtty/).

## API

| Method | Path | Example |
|---|---|---|
| GET | `/slugify?text=...` | `/slugify?text=Hello, World!` → `{"slug":"hello-world"}` |
| GET | `/healthz` | → `{"status":"ok"}` |

## Run locally

```powershell
python -m venv .venv
.\.venv\Scripts\pip install -r requirements.txt
.\.venv\Scripts\uvicorn src.app.main:app --reload
# GET http://127.0.0.1:8000/slugify?text=Hello,%20World!
```

## Test

```powershell
.\.venv\Scripts\pytest -q
```

## Deploy (Azure)

Pushing to `main` runs [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml):
test → Azure login (OIDC) → provision [`infra/main.bicep`](infra/main.bicep)
(App Service Free F1) → deploy. The provisioning/deploy step is **billable** and
requires a one-time Azure OIDC federated credential plus three repo secrets
(`AZURE_CLIENT_ID`, `AZURE_TENANT_ID`, `AZURE_SUBSCRIPTION_ID`). See the 3i
Deploy entry in the TWTTY replay log for the exact gated setup.
