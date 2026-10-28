# Planejamento de Update — AI Dev Framework (OpenHands Harness)

> Roadmap para fechar gaps identificados e levar o framework a maturidade de produção.

---

## Resumo Executivo

O framework possui a base funcional (router, skills, hooks, validação determinística) mas apresenta lacunas críticas em: **testes de skills**, **segurança**, **CI/CD**, **gerenciamento de secrets**, **auditoria de agente** e **rollback**. Este plano organiza as correções em 6 fases prioritárias.

---

## Fase 0 — Assimilação dos 5 Fundamentos de Segurança (@manodeyvin) (Semana 0, paralela à Fase 1)

**Objetivo:** Implementar as 6 skills baseadas nos prompts de @manodeyvin para fechar lacunas críticas de segurança e qualidade.

### 0.1 Skill race-condition-auditor (Prompt 1 — Race Condition)
- [ ] Criar `skills/race-condition-auditor.md` ✅ FEITO
- [ ] Executar auditoria de race conditions nos endpoints de escrita
- [ ] Aplicar correções por ordem: unique index > operação atômica > SELECT FOR UPDATE
- [ ] Criar testes de concorrência (2 requisições simultâneas → 1 efeito)
- **Regra:** Não propor Redis, fila ou lock em memória se o banco resolve

### 0.2 Skill idempotency-auditor (Prompt 2 — Idempotência)
- [ ] Criar `skills/idempotency-auditor.md` ✅ FEITO
- [ ] Mapear todos os webhooks recebidos e endpoints de pagamento
- [ ] Criar tabela de eventos processados com ID único
- [ ] Implementar verificação de assinatura com corpo bruto
- [ ] Implementar idempotency key (UUID v4) para chamadas ao gateway
- [ ] Aceitar header Idempotency-Key em endpoints de entrada
- **Regra:** Não usar dado pessoal (e-mail, CPF) como chave de idempotência

### 0.3 Skill client-trust-auditor (Prompt 3 — Nunca Confie no Cliente)
- [ ] Criar `skills/client-trust-auditor.md` ✅ FEITO
- [ ] Mover regras de negócio do front para o servidor (preço, desconto, permissão, plano)
- [ ] Remover segredos do front (service_role, chaves de terceiros)
- [ ] Auditar RLS e policies do Supabase/banco exposto
- [ ] Gerar relatório de segurança primeiro (sem alterar nada)
- **Regra:** Aplicar correções uma por vez, com OK do usuário em cada uma

### 0.4 Skill separation-of-concerns-refactorer (Prompt 4 — Separação de Responsabilidades)
- [ ] Criar `skills/separation-of-concerns-refactorer.md` ✅ FEITO
- [ ] Identificar arquivos grandes para refatorar
- [ ] Escrever testes de caracterização antes do primeiro passo
- [ ] Dividir em 3 camadas: UI, regra de negócio, acesso a dados
- **Regra:** Não corrigir bugs nem mudar regra de negócio durante a refatoração

### 0.5 Skill integration-test-generator (Prompt 5 — Testes de Integração)
- [ ] Criar `skills/integration-test-generator.md` ✅ FEITO
- [ ] Listar fluxos críticos (cadastro, login, checkout, webhooks)
- [ ] Escrever frases describe/it em português (aguardar confirmação do usuário)
- [ ] Configurar banco de teste separado (nunca produção)
- [ ] Mock apenas de serviços externos
- **Regra:** Não apagar, pular ou afrouxar teste para fazê-lo passar

### 0.6 Skill auditoria-combinada (Gerador AUDITORIA.md)
- [ ] Criar `skills/auditoria-combinada.md` ✅ FEITO
- [ ] Executar auditoria completa dos 5 fundamentos
- [ ] Gerar `AUDITORIA.md` na raiz com 5 achados de maior risco
- [ ] Tabela por etapa (achado, risco, arquivo:linha, correção)
- **Regra:** Não alterar nenhum arquivo (exceto criar AUDITORIA.md)

---

## Fase 1 — Fundamentos Críticos (Semana 1)

**Objetivo:** Desbloquear o uso das skills e estabelecer validação mínima de segurança.

### 1.1 Testes de skills (obrigatório para `post_skill_load`)
- [ ] Criar `tests/skills/spec-generator_test.py`
- [ ] Criar `tests/skills/commit-architect_test.py`
- [ ] Criar `tests/skills/agile-orchestrator_test.py`
- [ ] Criar `tests/skills/deterministic-validator_test.py`
- **Critério de aceite:** `python .openhands/hooks/post_skill_load.py <skill>` retorna PASS para cada skill

### 1.2 Segurança básica
- [ ] Instalar e configurar `bandit` (Python security linter)
- [ ] Instalar e configurar `safety` ou `pip-audit` (vulnerabilidades de dependência)
- [ ] Adicionar `bandit` ao `quality_gate.sh`
- [ ] Criar `.gitignore` para excluir `.env`, `*.key`, `*.pem`, `secrets/`

### 1.3 Diretório de reports
- [ ] Criar `.kilo/reports/` com `.gitkeep`
- [ ] Verificar que `modification_report.py` gera relatórios corretamente

---

## Fase 2 — CI/CD e Qualidade Automatizada (Semana 2)

**Objetivo:** Executar quality gate em cada PR e bloquear merges que falharem.

### 2.1 Pipeline CI (GitHub Actions)
- [ ] Criar `.github/workflows/quality-gate.yml`
  - Rodar `ruff check .`
  - Rodar `markdownlint **/*.md`
  - Rodar `mypy --strict scripts/`
  - Rodar `pytest tests/ --cov=. --cov-fail-under=80`
  - Rodar `python scripts/validate_routing.py`
  - Rodar `bandit -r .`
  - Bloquear PR se qualquer etapa falhar

### 2.2 Husky + lint-staged (pre-commit local)
- [ ] Instalar `husky` e `lint-staged`
- [ ] Configurar `.husky/pre-commit` executando `quality_gate.sh`
- [ ] Configurar `lint-staged` para rodar `ruff check --fix` e `markdownlint` em arquivos staged

### 2.3 Coverage reporting
- [ ] Configurar upload de coverage para Codecov ou similar
- [ ] Adicionar badge de coverage ao README

---

## Fase 3 — Agent Manager e Ambiente (Semana 3)

**Objetivo:** Habilitar sessões paralelas isoladas e ambiente reprodutível.

### 3.1 Agent Manager worktrees
- [ ] Configurar `.kilo/agent-manager.json` com seções de trabalho
- [ ] Criar worktree para desenvolvimento principal
- [ ] Criar worktree para homologação/QA
- [ ] Testar prompt e move de sessões entre seções

### 3.2 Docker para sandbox OpenHands
- [ ] Criar `Dockerfile` para ambiente OpenHands (Python + ruff + mypy + pytest + shellcheck + markdownlint)
- [ ] Criar `docker-compose.yml` para orquestração local
- [ ] Documentar variáveis de ambiente necessárias

### 3.3 Gerenciamento de secrets
- [ ] Criar template `.env.example`
- [ ] Adicionar `.env` ao `.gitignore`
- [ ] Documentar uso de variáveis de ambiente para credenciais

---

## Fase 4 — Auditoria, Rollback e Observabilidade (Semana 4)

**Objetivo:** Rastrear decisões do agente, permitir reversão e monitorar performance.

### 4.1 Auditoria de agente
- [ ] Estender `session_log.md` com registro automático de:
  - Arquivos editados/criados/removidos
  - Skills carregadas
  - Resultados de validação (pass/fail)
  - Tempo de execução por tarefa
- [ ] Criar script `scripts/audit_log.py` para consolidar logs

### 4.2 Rollback de mudanças
- [ ] Criar `scripts/rollback.sh` que:
  - Lista últimos commits
  - Reverte commit específico com `git revert`
  - Gera modification report do rollback
- [ ] Documentar procedimento de rollback em `docs/rollback.md`

### 4.3 Performance e custo de IA
- [ ] Adicionar métricas de tempo de execução por hook
- [ ] Rastrear uso de tokens (se disponível via OpenHands)
- [ ] Criar dashboard simples em `.kilo/reports/metrics.md`

---

## Fase 5 — Testes Avançados e Contratos (Semana 5-6)

**Objetivo:** Garantir integridade de interfaces e comportamento entre módulos.

### 5.1 Testes de integração
- [ ] Criar `tests/integration/` com testes de fluxo ponta-a-ponta
- [ ] Teste: spec-generator → docs/prd.md + docs/spec.md
- [ ] Teste: commit-architect → conventional commits válidos
- [ ] Teste: quality gate bloqueia commit com falha

### 5.2 Contract testing / Schema validation
- [ ] Criar schema JSON para skills (`skills/schema.json`)
- [ ] Validar que cada skill segue o formato esperado
- [ ] Adicionar validação ao `post_skill_load.py`

### 5.3 Skill lifecycle (versionamento e depreciação)
- [ ] Adicionar campo `version` ao frontmatter de cada skill
- [ ] Adicionar campo `deprecated` para skills obsoletas
- [ ] Criar `scripts/skill_lifecycle.py` para gerenciar versões

---

## Fase 6 — Maturidade e Governança (Semana 7-8)

**Objetivo:** Processos formais de governança, changelog e melhoria contínua.

### 6.1 Changelog automático
- [ ] Configurar `standard-version` ou `semantic-release`
- [ ] Gerar `CHANGELOG.md` automaticamente a partir de commits Conventional

### 6.2 PR review automation
- [ ] Configurar `github_request_copilot_review` em PRs
- [ ] Criar template de PR em `.github/PULL_REQUEST_TEMPLATE.md`
- [ ] Adicionar CODEOWNERS para revisão obrigatória

### 6.3 Documentação de governança
- [ ] Criar `docs/governance.md` com:
  - Processo de override e exceções
  - Critérios para criar novas skills
  - Fluxo de aprovação de mudanças arquiteturais
- [ ] Atualizar `AGENTS.md` com referências aos novos processos

---

## Matriz de Prioridade e Esforço

| Item | Fase | Prioridade | Esforço | Dependências |
|------|------|------------|---------|--------------|
| Testes de skills | 1 | Crítica | 1 dia | Nenhuma |
| Bandit + safety | 1 | Alta | 0.5 dia | Nenhuma |
| .kilo/reports/ | 1 | Média | 0.5 dia | Nenhuma |
| CI/CD pipeline | 2 | Crítica | 2 dias | Testes de skills |
| Husky pre-commit | 2 | Alta | 1 dia | Nenhuma |
| Agent Manager worktrees | 3 | Média | 1 dia | Nenhuma |
| Docker sandbox | 3 | Média | 1 dia | Nenhuma |
| Secrets management | 3 | Alta | 0.5 dia | Nenhuma |
| Auditoria de agente | 4 | Média | 1.5 dias | Session log existente |
| Rollback script | 4 | Média | 1 dia | Git |
| Testes de integração | 5 | Alta | 2 dias | Testes de skills |
| Contract testing | 5 | Média | 1.5 dias | Schema skills |
| Skill lifecycle | 5 | Baixa | 1 dia | Nenhuma |
| Changelog automático | 6 | Média | 1 dia | Conventional commits |
| PR review automation | 6 | Média | 1 dia | GitHub |
| Governance docs | 6 | Baixa | 1 dia | Nenhuma |

---

## Critérios de Sucesso por Fase

### Fase 1 — Concluída quando:
- [ ] `post_skill_load.py` retorna PASS para todas as 4 skills
- [ ] `bandit` executa sem vulnerabilidades críticas
- [ ] `.kilo/reports/` existe e recebe relatórios

### Fase 2 — Concluída quando:
- [ ] PR com falha de qualidade é bloqueado no CI
- [ ] Commit local falha se quality gate não passar
- [ ] Coverage report publicado externamente

### Fase 3 — Concluída quando:
- [ ] Duas worktrees Agent Manager funcionam simultaneamente
- [ ] Ambiente OpenHands sobe via Docker
- [ ] Nenhuma credencial commiteada

### Fase 4 — Concluída quando:
- [ ] Log de agente captura todas as edições
- [ ] Rollback reverte commit com sucesso
- [ ] Métricas de execução registradas

### Fase 5 — Concluída quando:
- [ ] Testes de integração passam em CI
- [ ] Schema de skills validado automaticamente
- [ ] Versão de skills rastreável

### Fase 6 — Concluída quando:
- [ ] Changelog gerado automaticamente
- [ ] PRs passam por review automatizado
- + Documentação de governança publicada

---

## Riscos e Mitigações

| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|-----------|
| Falha de skill em produção | Média | Alto | Testes de skills obrigatórios antes de carregar |
| Commit sem qualidade passa | Baixa | Alto | Husky + CI bloqueiam |
| Credencial exposta | Baixa | Crítico | `.gitignore` + secrets scan no CI |
| Ambiente não reproduzível | Média | Médio | Docker para sandbox |
| Perda de auditoria | Baixa | Médio | Logs versionados em `.kilo/reports/` |

---

## Próximos Passos Imediatos

1. **Esta semana:** Executar Fase 1 (testes de skills + segurança básica)
2. **Próxima semana:** Configurar CI/CD pipeline (Fase 2)
3. **Semana seguinte:** Agent Manager + Docker (Fase 3)

---

*Plano gerado em 2026-10-28 como parte da adoção do OpenHands como Harness principal.*