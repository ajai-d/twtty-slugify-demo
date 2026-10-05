# Execution Diagram — Iteration-YVIVBU

> Derived from `Iteration-YVIVBU-execution-log.md` (15 entries) + the branch-scoped log. The logs are authoritative; this diagram may be regenerated from them at any time.

```mermaid
flowchart TB
    subgraph SEED["SEED · Interactive"]
        E001["001 · meta/risk-level<br/>L1 (floor) + Azure cloud target"]:::meta
        E002["002 · seed/0a<br/>SEED-EXIT ✓ Human · Interactive"]:::gate
    end
    E003["003 · meta/autopilot-enable<br/>scope: SPEC/PLAN/EXECUTE · billable Azure hard-gated"]:::meta
    subgraph SPEC["SPEC · Autopilot"]
        E004["004 · meta/config<br/>GitHub + Azure App Service F1"]:::meta
        E005["005 · spec/1a · Discovery (Delegated)"]
        E006["006 · spec/1b–1d · requirements + AC-1..7"]
        E007["007 · spec/1d<br/>SPEC-EXIT ✓ Auto"]:::gate
    end
    subgraph PLAN["PLAN · Autopilot"]
        E008["008 · plan/2a–2c · architecture + W-1, W-2"]
        E009["009 · meta/execution-pattern · Sequential"]:::meta
        E010["010 · plan/2c<br/>PLAN-EXIT ✓ Auto"]:::gate
    end
    subgraph EXECUTE["EXECUTE · Autopilot · branch W-1-W-2-slugify (PR #1)"]
        E011["011 · 3b–3f · W-1 app + 8 tests (AC-1..7) pass"]
        E012["012 · 3g–3h · W-2 Bicep IaC + CI/CD pipeline"]
        E013["013 · 3i · Deploy — Escalate (billable, human-gated)"]:::escalate
        E014["014 · meta/branch-integrated · PR #1 merged → main"]:::meta
        E015["015 · 3m<br/>EXECUTE-EXIT ✓ Auto — build done; live deploy pending"]:::gate
    end

    E001 --> E002 --> E003 --> E004 --> E005 --> E006 --> E007 --> E008 --> E009 --> E010
    E010 --> E011 --> E012 --> E013 --> E014 --> E015

    classDef gate fill:#E8F5E9,stroke:#2E7D32,color:#1B5E20;
    classDef meta fill:#FFF3E0,stroke:#EF6C00,color:#E65100;
    classDef escalate fill:#FFEBEE,stroke:#C62828,color:#B71C1C;
```

## Legend

- **Green** = stage-exit gate (with mode). **Orange** = `meta/*` entry. **Red** = `Escalate` (hard-guardrail stop).

## Flow summary

| Stage | Entries | Gate · outcome · mode |
|-------|---------|-----------------------|
| **SEED** | 001 (risk L1 + cloud), 002 | `SEED-EXIT` · Approved · **Human / Interactive** |
| **SPEC** | 003 (autopilot), 004 (config), 005–006 | `SPEC-EXIT` · Approved · **Autopilot** |
| **PLAN** | 008, 009 (Sequential) | `PLAN-EXIT` · Approved · **Autopilot** |
| **EXECUTE** | 011 (W-1), 012 (W-2), 013 (deploy Escalate), 014 (integrated) | `EXECUTE-EXIT` (015) · Approved · **Autopilot** |

## Work items

- **W-1** — slug logic + FastAPI endpoints + 8 tests (AC-1..7). Delivered.
- **W-2** — Bicep IaC + gated CI/CD pipeline. Delivered.

## Notes

- Autopilot authorized at **003** (scope SPEC/PLAN/EXECUTE); the three stage-exit gates self-approved with attribution, SEED stayed Interactive.
- **013 is the one `Escalate`** — the billable Azure provision/deploy is a hard guardrail, handed to the Human User (OIDC + `AZURE_READY` + secrets). The build is complete; only the live deploy (BR-3) is pending that gated setup.
