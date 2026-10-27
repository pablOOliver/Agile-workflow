# Contexto Persistente — AI Dev Framework (OpenHands)

> Atualizado automaticamente pelo hook `post_edit.py` e pelo Agent Manager.
> Não edite manualmente — use para continuidade entre sessões.

---

## Estado Atual do Projeto

**Última Atualização:** 2026-10-20
**Branch Ativa:** main
**Último Commit:** (pendente)

### Arquivos Principais
- `agents.md` — Guia raiz Harness Engineering (CRIADO)
- `AGENTS.md` — Router de skills (EXISTENTE)
- `skills/deterministic-validator.md` — Nova skill de validação (CRIADA)
- `scripts/quality_gate.sh` — Pipeline qualidade (CRIADO)
- `scripts/validate_routing.py` — Validador roteamento (CRIADO)
- `scripts/modification_report.py` — Relatórios modificação (CRIADO)
- `.openhands/hooks/post_edit.py` — Hook auto-correção (CRIADO)
- `.openhands/hooks/pre_commit.py` — Hook pré-commit (CRIADO)
- `.openhands/hooks/post_skill_load.py` — Hook validação skill (CRIADO)
- `.openhands/config.yaml` — Config OpenHands (CRIADO)

### Skills Ativas
| Skill | Status | Testes |
|-------|--------|--------|
| spec-generator | ✅ Disponível | ❌ Falta `tests/skills/spec-generator_test.py` |
| commit-architect | ✅ Disponível | ❌ Falta `tests/skills/commit-architect_test.py` |
| agile-orchestrator | ✅ Disponível | ❌ Falta `tests/skills/agile-orchestrator_test.py` |
| deterministic-validator | ✅ NOVA (hooks) | ❌ Falta `tests/skills/deterministic-validator_test.py` |

---

## Decisões Recentes

1. **Adotado OpenHands como Harness principal** — sandbox, hooks, memória, Agent Manager
2. **Criado `agents.md` raiz** — consolida convenções, comandos, integração OpenHands
3. **Criada skill `deterministic-validator`** — espinha dorsal do feedback determinístico
4. **Implementados hooks OpenHands** — post_edit, pre_commit, post_skill_load
5. **Scripts de validação criados** — quality_gate.sh, validate_routing.py, modification_report.py

---

## Próximos Passos (Backlog)

- [ ] Criar testes para skills existentes em `tests/skills/`
- [ ] Instalar dependências: `ruff`, `markdownlint-cli`, `shellcheck`, `mypy`, `pytest`, `pytest-cov`
- [ ] Executar `quality_gate.sh` para validar pipeline
- [ ] Configurar Agent Manager com worktrees
- [ ] Testar hook `post_edit.py` com edição real
- [ ] Documentar fluxo de override em `.kilo/reports/`

---

## Log de Sessão (Auto-atualizado)

```
2026-10-20 13:38 — Iniciada estrutura Harness Engineering
2026-10-20 13:39 — Criado agents.md raiz
2026-10-20 13:40 — Criada skill deterministic-validator.md
2026-10-20 13:40 — Criados scripts: quality_gate.sh, validate_routing.py, modification_report.py
2026-10-20 13:41 — Criados hooks OpenHands: post_edit.py, pre_commit.py, post_skill_load.py
2026-10-20 13:41 — Criado .openhands/config.yaml
2026-10-20 13:42 — Criado context.md (este arquivo)
```