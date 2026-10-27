#!/usr/bin/env python3
"""
OpenHands Hook: post_skill_load
Executado ao carregar uma skill.
Verifica se a skill tem testes correspondentes em tests/skills/
"""

import json
import sys
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"status": "error", "message": "Uso: post_skill_load.py <skill_name>"}))
        sys.exit(1)

    skill_name = sys.argv[1]
    skill_file = Path(f"skills/{skill_name}.md")
    test_file = Path(f"tests/skills/{skill_name}_test.py")

    if not skill_file.exists():
        print(json.dumps({
            "status": "fail",
            "message": f"Skill não encontrada: {skill_file}"
        }))
        sys.exit(1)

    # Verificar se tem testes
    if not test_file.exists():
        print(json.dumps({
            "status": "fail",
            "message": f"Skill '{skill_name}' carregada mas NÃO TEM TESTES em {test_file}",
            "action_required": "Criar testes em tests/skills/ antes de usar a skill",
            "skill": skill_name
        }))
        sys.exit(1)

    print(json.dumps({
        "status": "pass",
        "message": f"Skill '{skill_name}' validada — testes encontrados em {test_file}",
        "skill": skill_name
    }))
    sys.exit(0)


if __name__ == "__main__":
    main()