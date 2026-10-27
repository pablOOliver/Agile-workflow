#!/usr/bin/env python3
"""
OpenHands Hook: post_edit
Executado após edit/write em arquivos de código.
Roda validação mínima no arquivo alterado, tenta auto-fix, reporta falha estruturada.
"""

import json
import subprocess
import sys
from pathlib import Path


VALIDATORS = {
    "py": ["ruff check", "mypy --strict"],
    "md": ["markdownlint"],
    "sh": ["shellcheck"],
    "yaml": ["yamllint"],
    "yml": ["yamllint"],
    "json": ["python -m json.tool"],
}


def run_cmd(cmd: str, filepath: str) -> tuple[int, str, str]:
    full_cmd = f"{cmd} {filepath}"
    result = subprocess.run(full_cmd, shell=True, capture_output=True, text=True, timeout=30)
    return result.returncode, result.stdout, result.stderr


def try_auto_fix(filepath: str, ext: str) -> bool:
    """Tenta auto-fix se for Python (ruff)"""
    if ext == "py":
        code, _, _ = run_cmd("ruff check --fix", filepath)
        return code == 0
    return False


def validate_file(filepath: str) -> dict:
    path = Path(filepath)
    ext = path.suffix.lstrip(".")

    validators = VALIDATORS.get(ext, [])
    if not validators:
        return {"status": "skipped", "reason": f"Sem validador para .{ext}"}

    for validator in validators:
        code, stdout, stderr = run_cmd(validator, filepath)
        if code != 0:
            # Tentar auto-fix para ruff
            auto_fixed = False
            if "ruff" in validator:
                auto_fixed = try_auto_fix(filepath, ext)
                if auto_fixed:
                    # Re-validar após fix
                    code, stdout, stderr = run_cmd(validator, filepath)
                    if code == 0:
                        return {
                            "status": "pass",
                            "stage": "lint",
                            "file": filepath,
                            "auto_fix_applied": True,
                            "message": "Auto-fix aplicado com sucesso"
                        }

            # Extrair linha/coluna se possível (ruff/mypy)
            line, column = 0, 0
            for line_text in stdout.split('\n'):
                if ':' in line_text and filepath in line_text:
                    parts = line_text.split(':')
                    if len(parts) >= 3:
                        try:
                            line = int(parts[1])
                            column = int(parts[2])
                        except ValueError:
                            pass
                    break

            return {
                "status": "fail",
                "stage": "lint",
                "file": filepath,
                "line": line,
                "column": column,
                "rule": validator.split()[0],
                "message": stdout.strip() or stderr.strip(),
                "auto_fix_applied": auto_fixed,
                "suggestion": "Corrija o erro acima; rode o validador manualmente para detalhes"
            }

    return {"status": "pass", "stage": "lint", "file": filepath}


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"status": "error", "message": "Uso: post_edit.py <filepath>"}))
        sys.exit(1)

    filepath = sys.argv[1]

    # Verificar se arquivo existe
    if not Path(filepath).exists():
        print(json.dumps({"status": "error", "message": f"Arquivo não encontrado: {filepath}"}))
        sys.exit(1)

    result = validate_file(filepath)
    print(json.dumps(result, ensure_ascii=False))

    # Exit code não-zero para falha (para que OpenHands saiba)
    if result.get("status") == "fail":
        sys.exit(1)


if __name__ == "__main__":
    main()