---
name: agile-orchestrator
description: Meta-skill que orquestra o fluxo completo de desenvolvimento: planejamento (spec-generator) → implementação → commits (commit-architect) → deploy/QA. Use quando o usuário quer seguir o workflow estruturado ponta-a-ponta.
---

## Quando usar
- Usuário quer iniciar um projeto novo do zero com processo completo
- Precisa de checklist estruturado cobrindo: ferramentas, planejamento, implementação, deploy, qualidade
- Quer garantir que todas as etapas do workflow sejam seguidas em ordem

## Quando NÃO usar
- Apenas quer gerar PRD/Spec → use spec-generator
- Apenas quer organizar commits → use commit-architect
- Tarefa pontual (bug fix, refatoração, dúvida técnica)

## Pré-condições
- Nenhuma (é o ponto de entrada do framework)
- **Quality Protocol (AGENTS.md):** Fluxo architect → coder → qa-auditor com quality gates e failure loop
- **Database Decision Protocol (docs/database-decisions.md):** Decisão de storage por tipo de dado validada no Passo 1

## Instruções
Orquestre o fluxo conforme Quality Protocol (AGENTS.md):

### Quality Gate & Roles
- **@agent-architect**: Define estrutura, contratos, constraints (Passo 1 via spec-generator)
- **@agent-coder**: Implementa código alinhado à spec + testes (TDD) (Passo 2)
- **@agent-qa-auditor**: Verifica testes, lint, coverage, edge cases; gera relatório em `.kilo/reports/`
- **Failure Loop**: QA reprova → retorna ao @agent-coder; só encerra após aprovação
- **Override**: Exceções ao protocolo exigem justificativa explícita e rastreável

### Passo 0: Preparar Ferramentas (One-Time)
- Verificar/install: antigravity-toolkit, openclaude/opencode, plugin Figma
- Instalar skill Caveman
- Configurar: Conventional Commits, standard-version, commit-architect skill

### Passo 1: Planejamento (@agent-architect → spec-generator)
- **spec-generator**: Criar PRD (docs/prd.md) e Spec (docs/spec.md) com critérios testáveis
- **Database Decision Gate (obrigatório)**: Validar matriz de storage por entidade (docs/database-decisions.md) — cada entidade classificada A–E, tecnologia escolhida, justificativa registrada
- Gerar agent.md, vision.md, manifesto.md, esquema do BD
- Definir stack (Web vs automação local), deploy target, versionamento

### Passo 2: Implementação (@agent-coder)
- Codificar baseado nas Tech Specs (docs/spec.md)
- **TDD obrigatório**: testes criados/atualizados antes da implementação, demonstrar falha primeiro
- Manter sincronia scripts ↔ banco de dados

### Passo 3: Quality Assurance (@agent-qa-auditor)
- Executar testes, lint/static analysis, coverage
- Verificar edge cases e regressões
- Gerar Modification Report em `.kilo/reports/`
- **Se falhar**: retornar ao @agent-coder com detalhes; bloquear commit

### Passo Final: Deployment & QA (@agent-coder → commit-architect)
- **commit-architect**: Snapshots (chore(snapshot)), commits organizados (após gates passarem)
- Testes antes de Code Review
- Docs atualizadas, Changelog via standard-version
- Code Review (segurança, performance)
- Branch flow: main → feature → main

### Melhoria Contínua (não-diário)
- Testes: cobertura total (unit/integração)
- Performance: Big-O, remover over-engineering
- Segurança: credenciais, permissões
- UX: fluidez, logs
- Estética: interface, organização código

## Formato de saída
- Checklist executável por fase
- Delega para spec-generator (Passo 1), implementação (Passo 2), qa-auditor (Passo 3), commit-architect (Passo Final)
- Relatórios de QA em `.kilo/reports/`

## Entrega para
spec-generator (Passo 1) → implementação (Passo 2) → qa-auditor (Passo 3) → commit-architect (Passo Final)

## Exemplos
**Entrada**: "Quero criar um sistema de gestão de tarefas seguindo o workflow completo"
**Saída**: Checklist Passo 0 → delega spec-generator para Passo 1 → implementação com TDD → qa-auditor valida → commit-architect para Passo Final