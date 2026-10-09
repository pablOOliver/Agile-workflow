# AI Framework Restructure Plan (Revised)

## Goal
Transform the "receita de bolo" workflow into a proper AI-agent framework with intent-based routing, composable skills, and testable contracts.

## Current State
- `README.md` - mentions "Receita de Bolo"
- `Agile-workflow.md` - 7-step checklist
- `Spec-generator.md` - single skill
- Empty `commit-architect/` and `ideias/` dirs
- `.kilo/plans/` only

## Target Structure
```
ai-dev-framework/
├── AGENTS.md              # Router, ~60 lines max
├── skills/
│   ├── spec-generator.md
│   └── commit-architect.md
├── .kilo/commands/        # 3-line pointers only
│   ├── spec.md
│   └── commit.md
├── tests/
│   └── routing-cases.md   # 15 fixed test cases
└── README.md
```

## Architecture Decisions (Resolved)

| Decision | Resolution |
|----------|------------|
| Routing mechanism | Intent/situation descriptions, not keywords |
| Fallback | No skill → respond normally. Clarification only on high-cost ambiguity |
| Skill limit | Max 1 skill per turn |
| Precedence | Explicit `use skill X` > intent match > no skill |
| Chaining | Skills declare `entrega para` (next skill) + artifact convention |
| Overlap | Each skill has `Quando NÃO usar` pointing to neighbor |
| Source of truth | `skills/` only. `.kilo/commands/*.md` = 3-line pointers |
| Repo name | `ai-dev-framework` (not Agile-workflow) |
| Agile-workflow.md | → `skills/agile-orchestrator.md` (meta-skill) or delete |
| Initial skills | 2: spec-generator, commit-architect |

## Skill Template (with frontmatter)
```markdown
---
name: spec-generator
description: Use quando o usuário precisa transformar uma ideia vaga em PRD ou spec técnica antes de escrever código.
---

## Quando usar
## Quando NÃO usar  → aponta para skill vizinha
## Pré-condições     → o que precisa existir antes
## Instruções
## Formato de saída  → caminho e formato do artefato (ex: docs/spec.md, markdown)
## Entrega para      → próxima skill na cadeia
## Exemplos          → pares entrada → saída reais
```

## Router Rules (AGENTS.md)
1. Compare user intent against skill `description` fields
2. Load at most one skill per turn
3. If no match → respond normally (no skill, no question)
4. If two match with similar strength → ask which
5. `use skill X` forces; `no skill` disables

## Artifact Convention
- Specs → `docs/spec.md` (markdown)
- PRDs → `docs/prd.md` (markdown)
- Commit messages → stdout (copied by user) or `.git/COMMIT_EDITMSG`
- Future: database schemas → `db/schema.sql`, migrations → `db/migrations/`

## Phased Execution

### Phase 0: Foundation (no skills yet)
- [ ] Rename repo to `ai-dev-framework`
- [ ] Standardize naming: kebab-case lowercase
- [ ] Read `ideias/` for salvageable content, then remove dir
- [ ] Remove empty `commit-architect/`
- [ ] `git mv Spec-generator.md skills/spec-generator.md` (commit separately)
- [ ] Create `skills/` dir, `.kilo/commands/`, `tests/`

### Phase 1: spec-generator (single skill)
- [ ] Rewrite `skills/spec-generator.md` to new template
- [ ] Create `.kilo/commands/spec.md` (3-line pointer)
- [ ] Write `tests/routing-cases.md` with 15 cases:
  - 5 positive (should trigger spec-generator)
  - 5 negative (should trigger nothing)
  - 5 ambiguous (should ask clarification)
- [ ] Validate: run test prompts, verify routing

### Phase 2: commit-architect (second skill)
- [ ] Create `skills/commit-architect.md` from template
- [ ] Add `Quando NÃO usar` pointing to spec-generator
- [ ] Create `.kilo/commands/commit.md`
- [ ] Extend `tests/routing-cases.md` with collision cases between the two
- [ ] Validate: run full test suite

### Phase 3: Router & Orchestration
- [ ] Write `AGENTS.md` (~60 lines) with router rules + skill descriptions
- [ ] Decide on `Agile-workflow.md`: convert to `skills/agile-orchestrator.md` or delete
- [ ] Create `README.md` describing framework
- [ ] Final validation pass

### Phase 4: Evaluate Expansion (only if needed)
- [ ] Assess if database-architect, project-initializer, etc. still needed
- [ ] Add via same phased process if yes

## Validation Criteria
- All 15+ routing cases pass deterministically
- No skill loads when it shouldn't (false positive rate = 0)
- Chaining works: spec-generator output found by next skill
- AGENTS.md < 60 lines
- Zero content duplication between skills/ and .kilo/commands/

## Open Questions (Remaining)
1. Artifact discovery: how does next skill find previous output? (convention: fixed paths vs. manifest file)
2. Skill versioning: when template changes, how to migrate existing skills?
3. Language: keep all skill content in PT-BR or English for descriptions?

## Risks
- Intent matching still has edge cases → mitigated by test cases + explicit override
- Context window: AGENTS.md + skill must fit → 60-line cap + load on demand
- Drift between skill and command pointer → mitigated by 3-line command files