# Plan: Assimilar Protocolo de Qualidade e Governança ao AGENTS.md

## Objetivo

Integrar ao AGENTS.md um protocolo central de qualidade, TDD, governança de papéis e revisão automatizada, mantendo o arquivo conciso (<60 linhas).

AGENTS.md será a fonte única de verdade das regras do protocolo. As skills apenas referenciarão e operacionalizarão essas regras.

## Mudanças Necessárias

### 1. Adicionar seção "Quality Protocol" ao AGENTS.md

Incluir as regras obrigatórias:

- **Existing Tests Immutable by Default** — testes existentes não podem ser apagados, enfraquecidos, ignorados ou alterados apenas para fazer a implementação passar. Alterações exigem override explícito e rastreável.
- **TDD Obrigatório** — testes correspondentes devem ser criados/atualizados antes da implementação e, quando aplicável, demonstrar falha antes da correção.
- **Specialized Roles** — fluxo padrão: @agent-architect → @agent-coder → @agent-qa-auditor.
- **Quality Gate** — testes, lint/static analysis e cobertura devem passar antes da conclusão.
- **Coverage Policy** — respeitar os thresholds configurados pelo projeto e registrar regressões relevantes de cobertura.
- **Modification Report** — toda alteração de código deve gerar relatório em .kilo/reports/.
- **Failure Loop** — falhas detectadas pelo QA retornam ao @agent-coder; o fluxo só encerra após aprovação.
- **Explicit Override** — exceções ao protocolo devem ser explícitas, justificadas e rastreáveis.

### 2. Atualizar skills existentes para referenciar o protocolo

**spec-generator**
- Exigir critérios verificáveis e casos de teste antes da implementação.
- Referenciar a regra de TDD definida no AGENTS.md.

**commit-architect**
- Exigir testes, lint/static analysis e quality gates aprovados antes da criação do commit.
- Impedir geração de commit quando qualquer quality gate obrigatório falhar.

**agile-orchestrator**
- Coordenar o fluxo architect → coder → qa-auditor.
- Garantir conclusão de cada etapa antes da seguinte.
- Encaminhar falhas do QA de volta ao coder.
- Bloquear conclusão/commit enquanto o quality gate não passar.

### 3. Definir convenção de artefatos

- Testes: `tests/`
- Cobertura: `coverage/`
- Relatórios de modificação/QA: `.kilo/reports/`

Artefatos gerados automaticamente devem permanecer fora da lógica de negócio e respeitar a estrutura existente do projeto.

## Estrutura Final do AGENTS.md

```
# AI Dev Framework — Agent Router

## Skills
(table existente)

## Router Rules
(regras existentes)

## Skill Chaining
(spec-generator → commit-architect e demais encadeamentos)

## Quality Protocol
- Existing tests immutable by default
- TDD obrigatório
- Roles: architect → coder → qa-auditor
- Tests + static analysis + coverage gate
- QA failure → coder/fix loop
- Modification report required
- Explicit override required for exceptions

## Artifact Convention
(existing + tests/ + coverage/ + .kilo/reports/)

## Override Commands
(regras existentes)
```

## Validação

- AGENTS.md deve permanecer abaixo de 60 linhas.
- AGENTS.md deve ser a única fonte normativa do Quality Protocol (single source of truth).
- Skills devem referenciar o protocolo sem duplicar suas regras normativas.
- Testes de roteamento existentes devem continuar passando.
- Fluxo deve bloquear conclusão quando quality gates falharem.
- Fluxo deve permitir retorno qa-auditor → coder para correções.
- Alterações de código devem produzir o modification report esperado.
- Exceções ao protocolo devem ser explicitamente rastreáveis.

## Fora de Escopo

- Implementação interna de @agent-architect, @agent-coder e @agent-qa-auditor.
- Configuração específica de linters, frameworks de teste ou CI.
- Definição de thresholds específicos de cobertura quando já configuráveis pelo projeto.
- Alteração da lógica de negócio existente.