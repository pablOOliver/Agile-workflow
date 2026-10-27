#!/usr/bin/env python3
"""
Modification Report Generator
Gera relatório de alterações para .kilo/reports/
"""

import subprocess
import sys
from datetime import datetime
from pathlib import Path


def run_cmd(cmd: str) -> tuple[int, str, str]:
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr


def get_git_status() -> dict:
    """Coleta status do git"""
    code, stdout, _ = run_cmd("git status --porcelain")
    files = []
    for line in stdout.strip().split('\n'):
        if line:
            status = line[:2]
            filepath = line[3:]
            files.append({"status": status.strip(), "file": filepath})
    return {"files": files}


def get_git_diff_stat() -> str:
    """Estatísticas do diff"""
    code, stdout, _ = run_cmd("git diff --stat")
    return stdout.strip()


def get_git_diff() -> str:
    """Diff completo"""
    code, stdout, _ = run_cmd("git diff")
    return stdout.strip()


def get_current_branch() -> str:
    code, stdout, _ = run_cmd("git branch --show-current")
    return stdout.strip()


def get_last_commit() -> str:
    code, stdout, _ = run_cmd("git log -1 --oneline")
    return stdout.strip()


def run_quality_gate() -> dict:
    """Executa quality gate e retorna status por etapa"""
    stages = {
        "lint": "ruff check .",
        "markdownlint": "markdownlint **/*.md 2>/dev/null || true",
        "typecheck": "mypy --strict scripts/ 2>/dev/null || true",
        "tests": "pytest tests/ -v --tb=short 2>/dev/null || true",
        "coverage": "pytest tests/ --cov=. --cov-fail-under=80 -q 2>/dev/null || true",
        "routing": "python scripts/validate_routing.py 2>/dev/null || true",
    }

    results = {}
    for stage, cmd in stages.items():
        code, stdout, stderr = run_cmd(cmd)
        results[stage] = {
            "passed": code == 0,
            "output": stdout[-500:] if stdout else stderr[-500:]
        }
    return results


def main():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_dir = Path(".kilo/reports")
    report_dir.mkdir(parents=True, exist_ok=True)

    report_file = report_dir / f"modification_{timestamp}.md"

    # Coletar dados
    git_status = get_git_status()
    diff_stat = get_git_diff_stat()
    diff_full = get_git_diff()
    branch = get_current_branch()
    last_commit = get_last_commit()
    quality_results = run_quality_gate()

    # Gerar relatório
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(f"# Modification Report\n\n")
        f.write(f"**Timestamp:** {datetime.now().isoformat()}\n")
        f.write(f"**Branch:** {branch}\n")
        f.write(f"**Last Commit:** {last_commit}\n\n")

        f.write("## Arquivos Alterados\n\n")
        if git_status["files"]:
            f.write("| Status | Arquivo |\n")
            f.write("|--------|---------|\n")
            for item in git_status["files"]:
                f.write(f"| {item['status']} | {item['file']} |\n")
        else:
            f.write("_Nenhum arquivo alterado no working tree_\n")
        f.write("\n")

        f.write("## Diff Estatístico\n\n")
        f.write("```\n")
        f.write(diff_stat or "_sem alterações_")
        f.write("\n```\n\n")

        f.write("## Quality Gate Results\n\n")
        f.write("| Etapa | Status |\n")
        f.write("|-------|--------|\n")
        all_passed = True
        for stage, result in quality_results.items():
            status = "✅ PASS" if result["passed"] else "❌ FAIL"
            if not result["passed"]:
                all_passed = False
            f.write(f"| {stage} | {status} |\n")
        f.write("\n")

        f.write("## Quality Gate Overall\n\n")
        f.write(f"**{'PASS ✅' if all_passed else 'FAIL ❌'}**\n\n")

        if not all_passed:
            f.write("### Falhas Detalhadas\n\n")
            for stage, result in quality_results.items():
                if not result["passed"]:
                    f.write(f"#### {stage}\n")
                    f.write("```\n")
                    f.write(result["output"])
                    f.write("\n```\n\n")

        f.write("---\n")
        f.write("*Gerado automaticamente por scripts/modification_report.py*\n")

    print(f"Relatório gerado: {report_file}")
    print(f"Quality Gate: {'PASS' if all_passed else 'FAIL'}")

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())