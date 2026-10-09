# AI Dev Framework — Agent Router

## Skills

| Skill | Description |
|-------|-------------|
| spec-generator | Transforma ideia vaga em PRD (docs/prd.md) + Spec técnica (docs/spec.md) |
| commit-architect | Gera commits Conventional Commits organizados a partir de alterações feitas |
| agile-orchestrator | Orquestra fluxo completo: architect → coder → qa-auditor |

## Router Rules

1. Compare user intent against skill `description` fields
2. Load at most one skill per turn
3. If no match → respond normally (no skill, no question)
4. If two match with similar strength → ask which
5. `use skill X` forces; `no skill` disables

## Skill Chaining

spec-generator → commit-architect
- spec-generator output: `docs/spec.md` + `docs/prd.md`
- commit-architect reads spec for context, produces commit messages

agile-orchestrator coordinates: @agent-architect → @agent-coder → @agent-qa-auditor

## Quality Protocol

- Existing tests immutable by default — changes require explicit, traceable override
- TDD obrigatório — tests written/updated before impl, demonstrate failure first when applicable
- Roles: @agent-architect → @agent-coder → @agent-qa-auditor
- Tests + static analysis + coverage gate must pass before completion
- Coverage Policy — respect project-configured thresholds, log regressions
- Modification Report — code changes produce report in `.kilo/reports/`
- QA failure → coder/fix loop; flow ends only after approval
- Explicit override required for exceptions

## Artifact Convention

- Specs → `docs/spec.md` (markdown)
- PRDs → `docs/prd.md` (markdown)
- Commits → stdout or `.git/COMMIT_EDITMSG`
- Tests → `tests/`
- Coverage → `coverage/`
- QA Reports → `.kilo/reports/`

## Override Commands

- `use skill spec-generator` — force spec generation
- `use skill commit-architect` — force commit generation
- `use skill agile-orchestrator` — force full workflow
- `no skill` — disable all skills this turn