# AI Dev Framework — AGENTS.md (Router + Guia Root OpenHands)

> **Harness Engineering Configuration for OpenHands**
> Este arquivo define as convenções, regras de arquitetura, comandos e contexto do sistema para agentes IA.
> Carregado automaticamente pelo OpenHands como guia feed-forward.

---

## Router de Skills

| Skill | Descrição |
|-------|-----------|
| spec-generator | Transforma ideia vaga em PRD (docs/prd.md) + Spec técnica (docs/spec.md) |
| commit-architect | Gera commits Conventional Commits organizados a partir de alterações feitas |
| agile-orchestrator | Orquestra fluxo completo: architect → coder → qa-auditor |
| deterministic-validator | Validação determinística (lint, typecheck, testes, coverage) e auto-correção pós-edição |
| race-condition-auditor | Detecta e corrige condições de corrida em operações ler-decisão-grava no banco |
| idempotency-auditor | Garante que webhooks e endpoints de pagamento aceitem repetição sem efeito duplicado |
| client-trust-auditor | Auditoria de segurança: nunca confia no cliente, move regras para servidor, valida RLS |
| separation-of-concerns-refactorer | Refatoração segura — divide arquivo grande em camadas (UI, negócio, dados) sem mudar comportamento |
| integration-test-generator | Gera testes de integração que batem nas rotas de verdade com banco de teste separado |
| auditoria-combinada | Auditoria completa dos 5 fundamentos sem alterar nada; gera AUDITORIA.md na raiz |

### Router Rules

1. Compare user intent against skill `description` fields
2. Load at most one skill per turn
3. If no match → respond normally (no skill, no question)
4. If two match with similar strength → ask which
5. `use skill X` forces; `no skill` disables

### Skill Chaining

spec-generator → commit-architect
- spec-generator output: `docs/spec.md` + `docs/prd.md`
- commit-architect reads spec for context, produces commit messages

agile-orchestrator coordinates: @agent-architect → @agent-coder → @agent-qa-auditor

### Skill Chaining Adicional (auditoria e qualidade)

auditoria-combinada → [race-condition-auditor | idempotency-auditor | client-trust-auditor | separation-of-concerns-refactorer | integration-test-generator]
- auditoria-combinada produz: AUDITORIA.md na raiz com 5 achados de maior risco e tabela por etapa
- Cada skill de correção lê AUDITORIA.md para contexto, produz o plano de correção
- Só altera código após OK explícito do usuário em cada etapa

deterministic-validator roda automaticamente via hook OpenHands (post_edit, pre_commit, post_skill_load)

---

## 1. Contexto do Sistema

| Item | Valor |
|------|-------|
| **Projeto** | AI Dev Framework — Agentes com skills compostas e roteamento por intenção |
| **Repositório** | `https://github.com/pablOOliver/Agile-workflow` |
| **Stack Principal** | Markdown (skills, specs, docs), Python (scripts de validação), Git |
| **Harness** | **OpenHands** (orquestração de agentes, sandbox, terminal, memória) |
| **Protocolo de Qualidade** | TDD obrigatório, testes imutáveis, gates (testes + lint + coverage), failure loop QA→Coder, modification reports |
| **Protocolo de Banco** | Matriz A–E (`docs/database-decisions.md`): Relacional (A), Key-Value (B), Document (C), Vetorial (D), Filas (E) |
| **Artefatos** | `docs/prd.md`, `docs/spec.md`, commits Conventional, reports em `.kilo/reports/` |

---

## 2. Regras de Arquitetura Invioláveis

1. **Single Skill per Turn** — Carregar no máximo 1 skill por turno (router em `AGENTS.md`)
2. **TDD First** — Testes escritos/atualizados **antes** da implementação; demonstrar falha primeiro
3. **Quality Gates** — Testes + lint/static analysis + coverage **devem passar** antes de qualquer commit
4. **Immutable Tests** — Testes existentes não mudam sem override explícito e rastreável
5. **Database Decision Gate** — Toda entidade classificada A–E **antes** de modelar schema
5. **Deterministic Validation** — Para cada regra de negócio crítica, existir validador automático (lint, typecheck, script)
6. **Auto-Correction Loop** — OpenHands executa sensores após cada alteração; falhas viram feedback para auto-correção
7. **Conventional Commits** — `<tipo>(escopo): descrição` — verbo infinitivo, sem genéricos
8. **Modification Reports** — Toda mudança de código gera relatório em `.kilo/reports/`

---

## 3. Comandos de Build, Testes e Validação

```bash
# Validar roteamento (determinístico)
python scripts/validate_routing.py

# Lint / Static Analysis
ruff check .                    # Python
markdownlint **/*.md            # Markdown
shellcheck scripts/*.sh         # Shell (se houver)

# Type Checking (se Python com type hints)
mypy --strict scripts/

# Testes (TDD)
pytest tests/ -v --tb=short

# Coverage Gate
pytest tests/ --cov=. --cov-fail-under=80

# Quality Gate Completo (CI local)
./scripts/quality_gate.sh       # Executa: lint → typecheck → testes → coverage → relatório

# Gerar Modification Report
python scripts/modification_report.py
```

> **Nota:** Scripts em `scripts/` são a fonte da verdade para validações determinísticas.

---

## 4. Estrutura de Pastas e Convenções

```
ai-dev-framework/
├── AGENTS.md                 # Router + guia raiz para OpenHands (ESTE ARQUIVO)
├── skills/                   # Skills modulares (sob demanda)
│   ├── spec-generator.md
│   ├── commit-architect.md
│   ├── agile-orchestrator.md
│   ├── deterministic-validator.md    # ← NOVA: validação + auto-correção
│   ├── race-condition-auditor.md     # ← raça condição no banco
│   ├── idempotency-auditor.md        # ← idempotência de webhooks/pagamentos
│   ├── client-trust-auditor.md       # ← segurança: nunca confia no cliente
│   ├── separation-of-concerns-refactorer.md  # ← refatoração em camadas
│   ├── integration-test-generator.md # ← testes de integração
│   └── auditoria-combinada.md        # ← auditoria dos 5 fundamentos
├── .kilo/
│   ├── commands/             # Ponteiros de 3 linhas (spec, commit, agile)
│   ├── reports/              # Modification reports + QA reports
│   └── agent-manager.json    # Estado do Agent Manager (não editar manual)
├── docs/
│   ├── prd.md                # Product Requirements Document
│   ├── spec.md               # Spec técnica executável
│   └── database-decisions.md # Protocolo matriz A–E
├── tests/
│   ├── routing-cases.md      # 20+ casos determinísticos de roteamento
│   └── unit/                 # Testes unitários (pytest)
├── scripts/                  # Validadores determinísticos (Python/Shell)
│   ├── validate_routing.py
│   ├── quality_gate.sh
│   └── modification_report.py
└── .openhands/               # Configuração OpenHands (sandbox, memória, hooks)
    ├── config.yaml
    ├── hooks/
    │   └── post_edit.py      # Auto-correção após edição
    └── memory/
        └── context.md        # Contexto persistente entre sessões
```

---

## 5. Skills Disponíveis (Carregamento Sob Demanda)

| Skill | Arquivo | Descrição | Quando Carregar |
|-------|---------|-----------|-----------------|
| `spec-generator` | `skills/spec-generator.md` | Ideia vaga → PRD + Spec | Nova feature/projeto sem spec |
| `commit-architect` | `skills/commit-architect.md` | Código pronto → Commits Conventional | Alterações feitas, precisa commitar |
| `agile-orchestrator` | `skills/agile-orchestrator.md` | Workflow completo ponta-a-ponta | Projeto novo do zero |
| `deterministic-validator` | `skills/deterministic-validator.md` | **NOVA** — Validação, lint, gates, auto-correção | **SEMPRE** (hook pós-edição) |
| `race-condition-auditor` | `skills/race-condition-auditor.md` | Detecção e correção de condições de corrida no banco | Suspeita de dados duplicados/corrompidos por concorrência |
| `idempotency-auditor` | `skills/idempotency-auditor.md` | Idempotência de webhooks e endpoints de pagamento | Webhooks de pagamento, endpoints que cobram/creditam |
| `client-trust-auditor` | `skills/client-trust-auditor.md` | Segurança: nunca confia no cliente, RLS, segredos do front | Auditoria de segurança completa |
| `separation-of-concerns-refactorer` | `skills/separation-of-concerns-refactorer.md` | Refatoração segura em camadas sem mudar comportamento | Arquivo grande, medo de editar |
| `integration-test-generator` | `skills/integration-test-generator.md` | Testes de integração em rotas reais com banco de teste | Cobrir fluxos críticos com testes |
| `auditoria-combinada` | `skills/auditoria-combinada.md` | Auditoria dos 5 fundamentos, gera AUDITORIA.md na raiz | Antes de qualquer correção, sem alterar nada |

> **Regra:** Skills são carregadas **apenas quando necessárias** via router ou `use skill X`. A `deterministic-validator` roda automaticamente via hook OpenHands.

---

## 6. Integração OpenHands — Mapeamento

### Sandbox & Terminal
- **Working Dir:** `/workspace` (mapeado para `F:\CODE\Agile-workflow`)
- **Shell:** `bash` (Linux no sandbox) / `powershell` (host Windows)
- **Permissões:** Leitura/escrita no workspace; Git, Python, Node disponíveis

### Memória Persistente (`.openhands/memory/`)
- `context.md` — Contexto do projeto, decisões recentes, estado atual
- `session_log.md` — Log de ações da sessão para continuidade

### Hooks de Auto-Correção (`.openhands/hooks/`)
| Hook | Trigger | Ação |
|------|---------|------|
| `post_edit.py` | Após `edit`/`write` em `*.py`, `*.md`, `*.sh` | Executa `quality_gate.sh` no arquivo alterado; se falhar, propõe fix |
| `pre_commit.py` | Antes de `git commit` | Valida quality gate completo; bloqueia se falhar |
| `post_skill_load.py` | Ao carregar skill | Verifica se skill tem testes correspondentes em `tests/skills/` |

### Git & Commits
- **Branch Strategy:** `main` → `feature/*` → `main` (PR obrigatório)
- **Commit Format:** Conventional Commits (via `commit-architect`)
- **Pre-commit:** `quality_gate.sh` (via hook OpenHands + husky opcional)
- **Modification Report:** Gerado em `.kilo/reports/` a cada commit

---

## 7. Protocolo de Override (Exceções)

Qualquer desvio das regras acima requer:
1. Justificativa escrita no commit/PR
2. Tag `[OVERRIDE]` na mensagem de commit
3. Link para issue/discussão que autorizou
4. Registro em `.kilo/reports/override_<timestamp>.md`

---

## 8. Referências Rápidas

- **Router Rules:** `AGENTS.md:9-18`
- **Quality Protocol:** `AGENTS.md:26-37`
- **Database Decisions:** `docs/database-decisions.md`
- **Routing Tests:** `tests/routing-cases.md`
- **OpenHands Config:** `.openhands/config.yaml`
- **Validation Scripts:** `scripts/`