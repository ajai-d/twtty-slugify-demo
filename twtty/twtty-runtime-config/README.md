# twtty-runtime-config

Project-owned TWTTY binding overrides for slugify-demo. See `runtimeconfig.md`
for the active overrides.

**Override rule:** an attribute listed in `runtimeconfig.md` uses the local file
or directory it points to; an attribute that is absent inherits the methodology
default from the specialization's `default-config.md`.

**Skills:** `reusable-assets/skills/` holds **project-captured skills** — reusable
prompts the AI Agent distilled from work it has already run. The AI Agent
inspects this directory and applies the skills that fit the work in scope, and
refines/consolidates them over time. Capturing or using a skill is not a
replay-log event; this directory's version-control history is the record.
