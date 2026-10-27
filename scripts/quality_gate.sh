#!/usr/bin/env bash
# Quality Gate Completo — lint → typecheck → testes → coverage → routing
# Exit code: 0 = PASS, 1 = FAIL

set -euo pipefail

echo "========================================"
echo "QUALITY GATE — Iniciando pipeline"
echo "========================================"

FAILED=0

# 1. Lint / Static Analysis
echo ""
echo "[1/5] Lint & Static Analysis"
echo "----------------------------"

# Python (ruff)
if command -v ruff &> /dev/null; then
    echo "  → ruff check ."
    if ! ruff check .; then
        echo "  ✗ ruff falhou"
        FAILED=1
    else
        echo "  ✓ ruff passou"
    fi
else
    echo "  ⚠ ruff não instalado (pip install ruff)"
fi

# Markdown (markdownlint)
if command -v markdownlint &> /dev/null; then
    echo "  → markdownlint **/*.md"
    if ! markdownlint **/*.md 2>/dev/null; then
        echo "  ✗ markdownlint falhou"
        FAILED=1
    else
        echo "  ✓ markdownlint passou"
    fi
else
    echo "  ⚠ markdownlint não instalado (npm i -g markdownlint-cli)"
fi

# Shell (shellcheck)
if command -v shellcheck &> /dev/null; then
    echo "  → shellcheck scripts/*.sh"
    if ! shellcheck scripts/*.sh 2>/dev/null; then
        echo "  ✗ shellcheck falhou"
        FAILED=1
    else
        echo "  ✓ shellcheck passou"
    fi
else
    echo "  ⚠ shellcheck não instalado"
fi

# 2. Type Checking
echo ""
echo "[2/5] Type Checking"
echo "-------------------"

if command -v mypy &> /dev/null; then
    echo "  → mypy --strict scripts/"
    if ! mypy --strict scripts/ 2>/dev/null; then
        echo "  ✗ mypy falhou"
        FAILED=1
    else
        echo "  ✓ mypy passou"
    fi
else
    echo "  ⚠ mypy não instalado (pip install mypy)"
fi

# 3. Testes (TDD)
echo ""
echo "[3/5] Testes (TDD)"
echo "------------------"

if command -v pytest &> /dev/null; then
    echo "  → pytest tests/ -v --tb=short"
    if ! pytest tests/ -v --tb=short; then
        echo "  ✗ Testes falharam"
        FAILED=1
    else
        echo "  ✓ Testes passaram"
    fi
else
    echo "  ⚠ pytest não instalado (pip install pytest)"
    FAILED=1
fi

# 4. Coverage Gate
echo ""
echo "[4/5] Coverage Gate (≥80%)"
echo "--------------------------"

if command -v pytest &> /dev/null; then
    echo "  → pytest tests/ --cov=. --cov-fail-under=80"
    if ! pytest tests/ --cov=. --cov-fail-under=80 --tb=short -q; then
        echo "  ✗ Coverage abaixo de 80%"
        FAILED=1
    else
        echo "  ✓ Coverage ≥ 80%"
    fi
fi

# 5. Validação de Roteamento
echo ""
echo "[5/5] Validação de Roteamento (Determinística)"
echo "----------------------------------------------"

if [ -f "scripts/validate_routing.py" ]; then
    echo "  → python scripts/validate_routing.py"
    if ! python scripts/validate_routing.py; then
        echo "  ✗ Validação de roteamento falhou"
        FAILED=1
    else
        echo "  ✓ Roteamento válido (100% acurácia)"
    fi
else
    echo "  ⚠ validate_routing.py não encontrado"
fi

echo ""
echo "========================================"
if [ $FAILED -eq 0 ]; then
    echo "QUALITY GATE: PASS ✓"
    echo "========================================"
    exit 0
else
    echo "QUALITY GATE: FAIL ✗"
    echo "========================================"
    exit 1
fi