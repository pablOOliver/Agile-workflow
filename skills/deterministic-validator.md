---
name: deterministic-validator
description: Skill obrigatória que executa validações determinísticas (lint, typecheck, testes, coverage) e auto-correção após cada alteração. Carregada automaticamente via hook OpenHands post_edit.
---

## Quando usar
- **SEMPRE** — executada automaticamente pelo hook `post_edit.py` do OpenHands
- Após qualquer `edit`/`write` em `*.py`, `*.md`, `*.sh`, `*.yaml`, `*.json`
- Antes de qualquer commit (via hook `pre_commit.py`)
- Ao carregar qualquer skill (via hook `post_skill_load.py`)

## Quando NÃO usar
- Nunca carregada manualmente pelo usuário
- Não substitui skills de domínio (spec-generator, commit-architect, agile-orchestrator)

## Pré-condições
- Scripts de validação em `scripts/` (quality_gate.sh, validate_routing.py, modification_report.py)
- OpenHands configurado com hooks em `.openhands/hooks/`
- Python 3.11+, ruff, pytest, markdownlint, shellcheck disponíveis no sandbox

## Instruções
Atue como **Quality Gate Engine** — validação determinística, feedback imediato, auto-correção.

### 1. Quality Gate Pipeline (Obrigatório — Ordem Estrita)

```bash
# Etapa 1: Lint / Static Analysis
ruff check .                    # Python
markdownlint **/*.md            # Markdown
shellcheck scripts/*.sh         # Shell

# Etapa 2: Type Checking
mypy --strict scripts/          # Python type hints

# Etapa 3: Testes (TDD)
pytest tests/ -v --tb=short

# Etapa 4: Coverage Gate
pytest tests/ --cov=. --cov-fail-under=80

# Etapa 5: Validação de Roteamento (determinística)
python scripts/validate_routing.py
```

**Regra:** Falha em **qualquer** etapa = **PARAR**. Reportar falha específica. Não prosseguir.

### 2. Auto-Correção Loop (Post-Edit Hook)

Após cada edição, o hook `post_edit.py` executa:

1. **Detectar arquivo alterado** → determinar validadores aplicáveis
2. **Executar validadores mínimos** para aquele arquivo (ex: `ruff check arquivo.py`)
3. **Se falhar:**
   - Capturar erro exato (linha, coluna, regra)
   - Tentar auto-fix: `ruff check --fix arquivo.py`
   - Se auto-fix falhar → gerar **feedback estruturado** para o agente:
     ```
     [VALIDATION FAIL] arquivo.py:42:5: E501 Line too long
     Sugestão: Quebrar linha em 88 chars ou refatorar expressão
     ```
   - Agente **deve** corrigir antes de continuar

### 3. Modification Report (Obrigatório)

Toda alteração de código gera relatório em `.kilo/reports/`:
```bash
python scripts/modification_report.py
```
**Conteúdo mínimo:**
- Arquivos alterados
- Resumo de mudanças (diff estatístico)
- Quality gate status (pass/fail por etapa)
- Testes novos/alterados
- Coverage delta

### 4. Validação de Roteamento (Determinística)

`scripts/validate_routing.py` deve:
- Carregar `AGENTS.md` + `skills/*.md`
- Executar todos os casos em `tests/routing-cases.md`
- **Zero falsos positivos** — tolerância = 0
- Reportar: acurácia, casos falhos, tempo de execução

### 5. Immutable Tests Enforcement

- Testes em `tests/` **não mudam** sem override rastreável
- Novos testes **sempre** acompanham nova funcionalidade (TDD)
- Cobertura não pode cair sem justificativa em override report

## Formato de Saída (Feedback para Agente)

```json
{
  "status": "pass|fail",
  "stage": "lint|typecheck|test|coverage|routing",
  "file": "caminho/arquivo.py",
  "line": 42,
  "column": 5,
  "rule": "E501",
  "message": "Line too long (120 > 88)",
  "auto_fix_applied": true|false,
  "suggestion": "Quebrar linha ou extrair variável"
}
```

## Entrega para
- **Agente executor** — recebe feedback e deve corrigir antes de prosseguir
- **commit-architect** — só recebe código se quality gate = PASS
- **agile-orchestrator** — usa no Passo 3 (QA) como validador final

## Exemplos

**Cenário 1: Edição em Python**
```
Agente edita src/service.py → hook roda ruff → E501 na linha 42
→ auto-fix falha → feedback JSON → agente quebra linha → re-valida → PASS
```

**Cenário 2: Nova skill sem testes**
```
Agente carrega skill-xyz.md → hook post_skill_load.py
→ verifica tests/skills/skill-xyz_test.py
→ NÃO EXISTE → bloqueia carregamento → exige teste primeiro
```

**Cenário 3: Commit bloqueado**
```
Agente tenta commit → hook pre_commit.py roda quality_gate.sh
→ coverage 78% (< 80%) → BLOQUEIA commit
→ relatório em .kilo/reports/qa_<timestamp>.md
→ agente deve adicionar testes ou justificar override
```

## Scripts Necessários (Criar em `scripts/`)

| Script | Função |
|--------|--------|
| `quality_gate.sh` | Pipeline completo lint→typecheck→test→coverage→routing |
| `validate_routing.py` | Valida router AGENTS.md contra tests/routing-cases.md |
| `modification_report.py` | Gera relatório de mudança pós-edição/commit |
| `post_edit.py` | Hook OpenHands: valida arquivo editado, tenta auto-fix |
| `pre_commit.py` | Hook OpenHands: quality gate completo antes de commit |
| `post_skill_load.py` | Hook OpenHands: verifica testes da skill carregada |

## Integração OpenHands (`.openhands/hooks/`)

```python
# post_edit.py — executado após edit/write
import subprocess, json, sys

def validate_file(filepath):
    ext = filepath.split('.')[-1]
    validators = {
        'py': ['ruff check', 'mypy --strict'],
        'md': ['markdownlint'],
        'sh': ['shellcheck'],
        'yaml': ['yamllint'],
        'json': ['python -m json.tool'],
    }
    for cmd in validators.get(ext, []):
        result = subprocess.run(f"{cmd} {filepath}", shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            # Tentar auto-fix se ruff
            if 'ruff' in cmd:
                subprocess.run(f"ruff check --fix {filepath}", shell=True)
                # Re-validar
                result = subprocess.run(f"{cmd} {filepath}", shell=True, capture_output=True, text=True)
            if result.returncode != 0:
                print(json.dumps({
                    "status": "fail",
                    "stage": "lint",
                    "file": filepath,
                    "message": result.stdout.strip(),
                    "auto_fix_applied": 'ruff' in cmd
                }))
                sys.exit(1)

if __name__ == "__main__":
    validate_file(sys.argv[1])
```

---

> **Nota:** Esta skill é a **espinha dorsal** do feedback determinístico. Sem ela, o Harness Engineering não tem travas — apenas intenção.