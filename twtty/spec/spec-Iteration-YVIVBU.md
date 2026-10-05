# Spec — Iteration-YVIVBU · Slugify API

## Metadata

- **Iteration ID:** Iteration-YVIVBU
- **Specialization:** baseline SDLC
- **Discovery mode:** Delegated
- **UX mode:** N/A (no user interface)
- **API mode:** Applies (HTTP/JSON API; L1 minimal bar)
- **Runtime target:** Azure App Service (Linux, Free F1) — subscription "Ajai's Subscription", region eastus
- **Risk level:** 1 (floor) + cloud target
- **Date:** 2026-10-04

## 1. Summary

A tiny HTTP service that converts a text string into a URL-friendly slug. Single
purpose, stateless, no persistence, no auth. Built in Python with FastAPI,
deployed to Azure App Service by a GitHub Actions pipeline.

## 2. Business requirements

- **BR-1** Provide a hosted endpoint that converts arbitrary text to a URL slug.
- **BR-2** Provide a health endpoint for readiness checks.
- **BR-3** The service is deployed to Azure automatically from `main` (no manual
  resource creation) and is reachable at a public URL.
- **BR-4** The project runs and tests locally with a documented command.

## 3. Use cases

- **UC-1** A developer calls `GET /slugify?text=Hello, World!` and receives
  `{"slug": "hello-world"}`.
- **UC-2** A platform calls `GET /healthz` and receives HTTP 200 to confirm the
  service is up.

## 4. Slug rules (functional spec)

Given an input string, the slug is produced by:

1. Unicode-normalize and transliterate to ASCII where reasonable (NFKD, drop
   combining marks).
2. Lowercase.
3. Replace any run of non-alphanumeric characters with a single hyphen `-`.
4. Trim leading/trailing hyphens.
5. Empty or all-separator input yields an empty string `""`.

## 5. API contract

| Method | Path | Query | Success | Error |
|---|---|---|---|---|
| GET | `/slugify` | `text` (string, required) | `200 {"slug": "<slug>"}` | `422` when `text` is missing |
| GET | `/healthz` | — | `200 {"status": "ok"}` | — |

## 6. Acceptance criteria

- **AC-1** `slugify("Hello, World!") == "hello-world"` (spaces + punctuation collapse to single hyphen, lowercased).
- **AC-2** `slugify("  Café del Mar  ") == "cafe-del-mar"` (unicode transliterated, trimmed).
- **AC-3** `slugify("multiple   ---  separators") == "multiple-separators"` (runs collapse to one hyphen).
- **AC-4** `slugify("") == ""` and `slugify("!!!") == ""` (empty / all-separator input).
- **AC-5** `GET /slugify?text=Hello, World!` returns `200` with body `{"slug":"hello-world"}`.
- **AC-6** `GET /slugify` with no `text` returns `422`.
- **AC-7** `GET /healthz` returns `200` with `{"status":"ok"}`.

## 7. Non-functional / constraints

- Python 3.11+, FastAPI + Uvicorn.
- Stateless; no database; no secrets in code.
- L1 controls: secret scanning only (3d); tests (3f); CI/CD + IaC + deploy for
  the cloud target (3g/3h/3i). No code-review gate, security scanning, smoke
  tests, monitoring, or observability (L1 acknowledgment, entry 001).

## 14. Compliance

No regulatory regime applies (throwaway prototype; no personal or customer data).
