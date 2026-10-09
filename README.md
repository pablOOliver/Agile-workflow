# AI Dev Framework

Framework de desenvolvimento com agentes de IA baseados em skills compostas e roteamento por intenção.

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