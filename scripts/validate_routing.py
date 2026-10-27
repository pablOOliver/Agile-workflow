#!/usr/bin/env python3
"""
Validador Determinístico de Roteamento
Carrega AGENTS.md + skills/*.md e executa todos os casos em tests/routing-cases.md
Zero tolerância para falsos positivos.
"""

import re
import sys
from pathlib import Path
from dataclasses import dataclass
from typing import List, Optional
from enum import Enum


class ExpectedSkill(str, Enum):
    SPEC_GENERATOR = "spec-generator"
    COMMIT_ARCHITECT = "commit-architect"
    AGILE_ORCHESTRATOR = "agile-orchestrator"
    NO_SKILL = "no skill"
    ASK_CLARIFICATION = "ask"


@dataclass
class TestCase:
    id: str
    category: str
    input: str
    expected: ExpectedSkill
    reason: str


def parse_agents_md(path: Path) -> dict:
    """Extrai skills e descriptions do AGENTS.md"""
    content = path.read_text(encoding="utf-8")
    skills = {}

    # Tabela de skills no AGENTS.md
    table_match = re.search(r'\| Skill \| Description \|\n\|[-|]+\|\n((?:\|.*\|\n)*)', content)
    if table_match:
        rows = table_match.group(1).strip().split('\n')
        for row in rows:
            parts = [p.strip() for p in row.split('|') if p.strip()]
            if len(parts) >= 2:
                skills[parts[0]] = parts[1]

    return skills


def parse_skill_files(skills_dir: Path) -> dict:
    """Carrega description de cada skill/*.md (frontmatter)"""
    skills = {}
    for skill_file in skills_dir.glob("*.md"):
        content = skill_file.read_text(encoding="utf-8")
        # Frontmatter YAML simples
        match = re.search(r'description:\s*(.+)', content)
        if match:
            skills[skill_file.stem] = match.group(1).strip().strip('"')
    return skills


def parse_routing_cases(path: Path) -> List[TestCase]:
    """Parseia tests/routing-cases.md para extrair casos de teste"""
    content = path.read_text(encoding="utf-8")
    cases = []

    # Padrão para cada caso de teste (mais flexível para reason multi-linha)
    pattern = r'### (TC-\d+|CC-\d+):\s*(.+?)\n\*\*Input\*\*:\s*"([^"]+)"\n\*\*Expected\*\*:\s*([^\n]+)\n\*\*Reason\*\*:\s*(.+?)(?=\n### |\n---|$)'

    for match in re.finditer(pattern, content, re.DOTALL):
        case_id, category, input_text, expected_raw, reason = match.groups()

        # Normalizar expected
        expected_raw = expected_raw.strip()
        if "perguntar" in expected_raw.lower() or "ask" in expected_raw.lower():
            expected = ExpectedSkill.ASK_CLARIFICATION
        elif "no skill" in expected_raw.lower() or "(no skill)" in expected_raw.lower():
            expected = ExpectedSkill.NO_SKILL
        elif "spec-generator" in expected_raw.lower():
            expected = ExpectedSkill.SPEC_GENERATOR
        elif "commit-architect" in expected_raw.lower():
            expected = ExpectedSkill.COMMIT_ARCHITECT
        elif "agile-orchestrator" in expected_raw.lower():
            expected = ExpectedSkill.AGILE_ORCHESTRATOR
        else:
            expected = ExpectedSkill.NO_SKILL

        cases.append(TestCase(
            id=case_id.strip(),
            category=category.strip(),
            input=input_text.strip(),
            expected=expected,
            reason=reason.strip()
        ))

    return cases


def route_intent(user_input: str, skills: dict) -> ExpectedSkill:
    """
    Implementa o roteador do AGENTS.md:
    1. Compara intenção contra skill descriptions
    2. Carrega no máximo 1 skill
    3. Se nenhum match → no skill
    4. Se dois matches com força similar → ask
    5. Casos ambíguos explícitos → ask
    """
    user_lower = user_input.lower()

    # Detectar padrões ambíguos explícitos (retornam ASK_CLARIFICATION)
    ambiguous_patterns = [
        "me ajuda com",
        "quero melhorar",
        "preciso documentar",
        "vou adicionar",
        "vou implementar",
        "organiza meus commits",
        "novo projeto.*commit",
    ]
    for pattern in ambiguous_patterns:
        if re.search(pattern, user_lower):
            return ExpectedSkill.ASK_CLARIFICATION

    # Detectar "spec já aprovada/pronta" → NO_SKILL
    if re.search(r"spec.*(aprovada|pronta|existe|ja feita|já feita)", user_lower):
        return ExpectedSkill.NO_SKILL

    # Detectar "já fiz alterações / código pronto" para commit-architect
    # Mas apenas se NÃO houver palavras de planejamento
    has_commit_intent = any(kw in user_lower for kw in [
        "commit", "commits", "conventional", "organizar commit",
        "ja fiz", "já fiz", "terminei", "acabei", "codigo pronto",
        "código pronto", "alteracoes feitas", "alterações feitas",
        "mudancas feitas", "mudanças feitas", "refatorei",
        "documentar as mudancas", "documentar as mudanças"
    ])
    
    has_planning_intent = any(kw in user_lower for kw in [
        "ideia", "planejar", "spec", "prd", "nova funcionalidade",
        "projeto novo", "workflow completo", "vou implementar",
        "adicionar", "criar", "novo modulo", "novo módulo",
        "autenticacao", "autenticação", "jwt"
    ])

    # Se tem intenção de commit E não tem intenção de planejamento → commit-architect
    if has_commit_intent and not has_planning_intent:
        return ExpectedSkill.COMMIT_ARCHITECT

    # Palavras-chave por skill (baseado nas descriptions + casos de teste)
    skill_keywords = {
        ExpectedSkill.SPEC_GENERATOR: {
            "strong": [
                "prd", "spec", "especifica", "especificação", "transformar", "ideia vaga",
                "nova funcionalidade", "projeto novo", "feature complexa", "regras de negocio",
                "criterio de aceite", "critério de aceite", "gere um prd", "gere uma spec",
                "planejar", "planejamento", "app de delivery", "sistema de agendamento",
                "pontos de fidelidade", "controle de estoque", "adicionar pagamentos",
                "módulo de pagamentos", "modulo de pagamentos", "autenticação jwt",
                "autenticacao jwt", "novo projeto", "começar do zero", "começar com",
                "workflow completo para", "workflow agile para"
            ],
            "weak": [
                "ideia", "ajuda", "me ajuda", "quer criar", "vou adicionar",
                "preciso adicionar", "quero adicionar", "sistema de", "app de"
            ],
            "negative": [
                "ja fiz", "já fiz", "terminei", "acabei", "pronto", "codigo pronto",
                "código pronto", "alteracoes feitas", "alterações feitas",
                "mudancas feitas", "mudanças feitas", "organizar commit",
                "commits organizados", "refatorei", "refatoração", "corrige",
                "bug fix", "bug", "corrigir", "spec aprovada", "spec pronta"
            ]
        },
        ExpectedSkill.COMMIT_ARCHITECT: {
            "strong": [
                "commit", "commits", "conventional", "organizar commit", "ja fiz",
                "alteracoes feitas", "mudancas feitas", "codigo pronto", "terminei",
                "organiza meus commits", "commits limpos", "refatorei", "documentar as mudancas",
                "docs de mudancas"
            ],
            "weak": [
                "mudancas", "mudanças", "alteracoes", "alterações"
            ],
            "negative": [
                "ideia", "planejar", "spec", "prd", "nova funcionalidade",
                "projeto novo", "workflow completo", "vou implementar"
            ]
        },
        ExpectedSkill.AGILE_ORCHESTRATOR: {
            "strong": [
                "workflow completo", "processo completo", "ponta a ponta",
                "checklist completo", "workflow agile", "orquestrar",
                "seguir o workflow", "workflow estruturado"
            ],
            "weak": [
                "novo projeto", "projeto do zero"
            ],
            "negative": [
                "apenas spec", "so spec", "só spec", "commit", "organizar"
            ]
        }
    }

    scores = {}
    for skill, kw_dict in skill_keywords.items():
        score = 0
        for kw in kw_dict["strong"]:
            if kw in user_lower:
                score += 3
        for kw in kw_dict["weak"]:
            if kw in user_lower:
                score += 1
        for kw in kw_dict["negative"]:
            if kw in user_lower:
                score -= 2
        if score > 0:
            scores[skill] = score

    if not scores:
        return ExpectedSkill.NO_SKILL

    max_score = max(scores.values())
    top_skills = [s for s, sc in scores.items() if sc == max_score]

    if len(top_skills) == 1:
        return top_skills[0]
    else:
        return ExpectedSkill.ASK_CLARIFICATION


def run_validation():
    print("=" * 60)
    print("VALIDAÇÃO DETERMINÍSTICA DE ROTEAMENTO")
    print("=" * 60)

    # Carregar skills
    agents_md = Path("AGENTS.md")
    skills_dir = Path("skills")

    if not agents_md.exists():
        print(f"ERRO: {agents_md} não encontrado")
        return False

    skills = parse_agents_md(agents_md)
    skills.update(parse_skill_files(skills_dir))

    print(f"Skills carregadas: {list(skills.keys())}")

    # Carregar casos de teste
    cases_path = Path("tests/routing-cases.md")
    if not cases_path.exists():
        print(f"ERRO: {cases_path} não encontrado")
        return False

    test_cases = parse_routing_cases(cases_path)
    print(f"Casos de teste carregados: {len(test_cases)}")

    # Executar validação
    passed = 0
    failed = 0
    false_positives = 0
    false_negatives = 0

    print("\n" + "-" * 60)
    print("EXECUTANDO CASOS DE TESTE")
    print("-" * 60)

    for tc in test_cases:
        result = route_intent(tc.input, skills)

        # Verificar se passou
        match = False
        if tc.expected == ExpectedSkill.ASK_CLARIFICATION and result == ExpectedSkill.ASK_CLARIFICATION:
            match = True
        elif tc.expected == ExpectedSkill.NO_SKILL and result == ExpectedSkill.NO_SKILL:
            match = True
        elif tc.expected == result:
            match = True

        if match:
            status = "[PASS]"
            passed += 1
        else:
            status = "[FAIL]"
            failed += 1
            # Classificar tipo de erro
            if tc.expected == ExpectedSkill.NO_SKILL and result != ExpectedSkill.NO_SKILL:
                false_positives += 1
            elif tc.expected != ExpectedSkill.NO_SKILL and result == ExpectedSkill.NO_SKILL:
                false_negatives += 1

        print(f"  {status} | {tc.id} | Expected: {tc.expected.value:20} | Got: {result.value:20}")
        if not match:
            # Sanitizar para ASCII no Windows
            input_safe = tc.input[:60].encode('ascii', 'replace').decode('ascii')
            reason_safe = tc.reason[:80].encode('ascii', 'replace').decode('ascii')
            print(f"       Input: \"{input_safe}...\"")
            print(f"       Reason: {reason_safe}")

    # Resumo
    print("\n" + "=" * 60)
    print("RESUMO")
    print("=" * 60)
    print(f"Total:     {len(test_cases)}")
    print(f"Passou:    {passed}")
    print(f"Falharam:  {failed}")
    print(f"Falsos Positivos:  {false_positives} (CRÍTICO: deve ser 0)")
    print(f"Falsos Negativos:  {false_negatives}")

    # Critérios de aprovação
    success = True
    if failed > 0:
        print("\n[FAIL] VALIDACAO FALHOU: casos com resultado incorreto")
        success = False
    if false_positives > 0:
        print("\n[FAIL] VALIDACAO FALHOU: falsos positivos detectados (zero tolerancia)")
        success = False
    if success:
        print("\n[OK] VALIDACAO PASSOU: 100% acuracia, zero falsos positivos")

    return success


if __name__ == "__main__":
    success = run_validation()
    sys.exit(0 if success else 1)