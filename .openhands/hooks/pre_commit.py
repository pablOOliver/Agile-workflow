#!/usr/bin/env python3
"""
OpenHands Hook: pre_commit
Executado antes de git commit.
Roda quality gate completo; bloqueia commit se falhar.
"""

import json
import subprocess
import sys
from pathlib import Path


def run_cmd(cmd: str) -> tuple[int, str, str]:
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=120)
    return result.returncode, result.stdout, result.stderr


def check_staged_changes() -> bool:
    """Verifica se há mudanças staged"""
    code, stdout, _ = run_cmd("git diff --cached --name-only")
    return bool(stdout.strip())


def run_quality_gate() -> dict:
    """Executa quality gate completo"""
    stages = [
        ("lint:ruff", "ruff check ."),
        ("lint:markdown", "markdownlint **/*.md 2>/dev/null || true"),
        ("lint:shell", "shellcheck scripts/*.sh 2>/dev/null || true"),
        ("typecheck", "mypy --strict scripts/ 2>/dev/null || true"),
        ("tests", "pytest tests/ -v --tb=short 2>/dev/null || true"),
        ("coverage", "pytest tests/ --cov=. --cov-fail-under=80 -q 2>/dev/null || true"),
        ("routing", "python scripts/validate_routing.py 2>/dev/null || true"),
    ]

    results = {}
    for stage, cmd in stages:
        code, stdout, stderr = run_cmd(cmd)
        results[stage] = {
            "passed": code == 0,
            "output": (stdout or stderr)[-1000:]
        }
    return results


def main():
    # Verificar se há mudanças staged
    if not check_staged_changes():
        print(json.dumps({"status": "skipped", "reason": "Nenhuma mudança staged"}))
        sys.exit(0)

    print(json.dumps({"status": "running", "message": "Executando quality gate pré-commit..."}))

    results = run_quality_gate()

    # Verificar resultados
    failed_stages = [s for s, r in results.items() if not r["passed"]]

    if failed_stages:
        report = {
            "status": "fail",
            "message": "Quality gate falhou — commit bloqueado",
            "failed_stages": failed_stages,
            "details": {s: results[s]["output"] for s in failed_stages}
        }
        print(json.dumps(report, ensure_ascii=False))

        # Gerar relatório QA
        from datetime import datetime
        report_dir = Path(".kilo/reports")
        report_dir.mkdir(parents=True, exist_ok=True)
        report_file = report_dir / f"qa_precommit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"

        with open(report_file, "w", encoding="utf-8") as f:
            f.write(f"# QA Pre-Commit Report\n\n")
            f.write(f"**Timestamp:** {datetime.now().isoformat()}\n\n")
            f.write("## Falhas\n\n")
            for stage in failed_stages:
                f.write(f"### {stage}\n```\n{results[stage]['output']}\n```\n\n")

        sys.exit(1)

    print(json.dumps({"status": "pass", "message": "Quality gate passou — commit autorizado"}))
    sys.exit(0)


if __name__ == "__main__":
    main()