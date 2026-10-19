# AI Dev Framework

Framework de desenvolvimento com agentes de IA baseados em skills compostas e roteamento por intenção.

## 🤖 Como a IA deve usar este framework (Onboarding)

> **Copie isto para o prompt da IA ao iniciar trabalho neste repositório:**

```
Atue como **engenheiro sênior** seguindo estritamente a cultura deste framework (repo: https://github.com/pablOOliver/Agile-workflow).

**Regras obrigatórias (AGENTS.md + skills/ + docs/database-decisions.md):**

1. **Router**: Compare intenção → carregue 1 skill por turno (spec-generator → commit-architect → agile-orchestrator)
2. **Quality Protocol**: TDD obrigatório (teste falha primeiro), testes imutáveis, gates (testes+lint+coverage) antes de qualquer commit, failure loop QA→coder, modification report em `.kilo/reports/`, override só com justificativa rastreável
3. **Database Decision Protocol**: Classifique toda entidade A–E antes de modelar schema; anti-patterns proibidos (Redis como source of truth, mono-repo de dados)
4. **Artifacts**: `docs/prd.md` + `docs/spec.md` (com matriz DB), commits Conventional, reports em `.kilo/reports/`

**Fluxo real:**
- Nova feature/ideia → **spec-generator** (PRD + Spec com matriz DB)
- Implementação → **@agent-coder** (TDD, segue spec, sync DB)
- QA → **@agent-qa-auditor** (testes, lint, coverage, edge cases, bloqueia se falhar)
- Commit → **commit-architect** (só após gates passarem, Conventional Commits)
- Projeto novo do zero → **agile-orchestrator** (orquestra: tools → spec → code → QA → deploy)

**Não faça:** commit sem gates, schema sem decisão DB, pular TDD, misturar responsabilidades num commit.
```

---

### ⚡ Quick Start (um comando)

**Se não tem o repo:**
```text
Clone https://github.com/pablOOliver/Agile-workflow.git, leia o README e atue como engenheiro sênior seguindo as regras obrigatórias da seção "Como a IA deve usar este framework".
```

**Se já tem o repo local:**
```text
Leia o README deste projeto e atue como engenheiro sênior seguindo as regras obrigatórias da seção "Como a IA deve usar este framework".
```

---

## Estrutura

```
ai-dev-framework/
├── AGENTS.md              # Router (~60 linhas)
├── skills/
│   ├── spec-generator.md      # Ideia vaga → PRD + Spec
│   ├── commit-architect.md    # Código pronto → Commits Conventional
│   └── agile-orchestrator.md  # Workflow completo ponta-a-ponta
├── .kilo/commands/       # Ponteiros de 3 linhas
│   ├── spec.md
│   ├── commit.md
│   └── agile.md
├── tests/
│   └── routing-cases.md  # 20+ casos de teste determinísticos
└── README.md
```

## Skills

| Skill | Descrição | Quando usar |
|-------|-----------|-------------|
| **spec-generator** | Transforma ideia vaga em PRD (`docs/prd.md`) + Spec técnica (`docs/spec.md`) | Nova funcionalidade/projeto sem especificação |
| **commit-architect** | Gera commits Conventional Commits organizados a partir de alterações feitas | Código alterado, precisa commitar limpo |
| **agile-orchestrator** | Orquestra workflow completo: ferramentas → planejamento → implementação → deploy/QA | Projeto novo do zero, quer processo estruturado |

## Roteamento

O `AGENTS.md` define as regras:
1. Compara intenção do usuário contra `description` das skills
2. Carrega no máximo 1 skill por turno
3. Sem match → responde normalmente (sem skill)
4. Dois matches com força similar → pergunta qual usar
5. `use skill X` força; `no skill` desabilita

## Encadeamento

```
spec-generator → commit-architect
```
- `spec-generator` produz: `docs/spec.md` + `docs/prd.md`
- `commit-architect` lê spec para contexto, produz mensagens de commit

`agile-orchestrator` coordena ambos: delega para `spec-generator` no planejamento e `commit-architect` no final.

## Artefatos

- **Specs** → `docs/spec.md` (markdown)
- **PRDs** → `docs/prd.md` (markdown)
- **Commits** → stdout (copiado pelo usuário) ou `.git/COMMIT_EDITMSG`

## Comandos Kilo

```bash
# Via .kilo/commands/
/spec "minha ideia de app"        # → spec-generator
/commit                           # → commit-architect
/agile "novo projeto"             # → agile-orchestrator
```

## Override

- `use skill spec-generator` — forçar geração de spec
- `use skill commit-architect` — forçar geração de commits
- `use skill agile-orchestrator` — forçar workflow completo
- `no skill` — desabilitar skills neste turno

## Testes

`tests/routing-cases.md` contém 20+ casos:
- 5 positivos por skill
- 5 negativos (sem skill)
- 5 ambíguos (pedem clarificação)
- 5+ colisão entre skills

## Validação

- Todos casos de roteamento passam deterministicamente
- Zero falsos positivos
- Encadeamento funciona: output de spec-generator encontrado por commit-architect
- AGENTS.md < 60 linhas
- Zero duplicação entre `skills/` e `.kilo/commands/`