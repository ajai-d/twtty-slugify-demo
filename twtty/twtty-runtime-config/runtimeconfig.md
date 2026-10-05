# runtimeconfig — slugify-demo

Project-owned binding overrides (sdlc §1.1). Resolution is per attribute: if an
attribute is listed here, the AI Agent uses the local file/dir it points to;
otherwise it inherits the methodology default from `default-config.md`.

```yaml
reusable-assets:
  skills: reusable-assets/skills/   # project-captured skills live here
```

Only the `reusable-assets.skills` binding is overridden (pointed at this folder's
`reusable-assets/skills/`) so the AI Agent inspects and applies the project's own
captured skills. All other bindings inherit `default-config.md`.
