from fastapi import FastAPI

from .slugify import slugify

app = FastAPI(title="Slugify API", version="1.0.0")


@app.get("/slugify")
def slugify_endpoint(text: str):
    """Return the URL slug for the given text (spec §5)."""
    return {"slug": slugify(text)}


@app.get("/healthz")
def healthz():
    """Readiness probe (spec §5)."""
    return {"status": "ok"}
