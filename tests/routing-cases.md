# Routing Test Cases

## Positive Cases (should trigger spec-generator)

### TC-01: Nova funcionalidade vaga
**Input**: "Quero um sistema de controle de estoque para minha loja"
**Expected**: spec-generator
**Reason**: Ideia vaga, precisa de PRD e Spec

### TC-02: Projeto novo do zero
**Input**: "Tenho uma ideia de app de delivery de comida, me ajuda a planejar"
**Expected**: spec-generator
**Reason**: Projeto novo sem especificação

### TC-03: Feature complexa sem detalhes técnicos
**Input**: "Preciso adicionar pagamentos via PIX no meu e-commerce"
**Expected**: spec-generator
**Reason**: Funcionalidade complexa, precisa de spec técnica

### TC-04: Solicitação explícita de PRD/Spec
**Input**: "Gere um PRD e uma spec para um sistema de agendamento de consultas"
**Expected**: spec-generator
**Reason**: Pedido explícito dos artefatos que a skill produz

### TC-05: Ideia com regras de negócio não definidas
**Input**: "Sistema de pontos de fidelidade que expira em 12 meses e pode ser transferido entre contas"
**Expected**: spec-generator
**Reason**: Regras de negócio complexas precisam ser documentadas no PRD

---

## Negative Cases (should trigger NO skill)

### TC-06: Já tem spec aprovada, quer implementar
**Input**: "A spec está aprovada em docs/spec.md, vamos codificar"
**Expected**: (no skill)
**Reason**: spec-generator não deve rodar; próximo passo é implementação

### TC-07: Apenas quer commit para mudanças feitas
**Input**: "Fiz as alterações no código, gera os commits organizados"
**Expected**: (no skill) — commit-architect virá na Fase 2
**Reason**: Tarefa de commit, não de especificação

### TC-08: Bug fix pontual
**Input**: "Corrige o bug no login: senha não valida caracteres especiais"
**Expected**: (no skill)
**Reason**: Correção pontual não precisa de PRD/Spec

### TC-09: Refatoração pura
**Input": "Refatora o service de usuário para usar repository pattern"
**Expected**: (no skill)
**Reason**: Refatoração não precisa de nova especificação

### TC-10: Pergunta técnica geral
**Input**: "Qual a diferença entre Clean Architecture e Hexagonal?"
**Expected**: (no skill)
**Reason**: Pergunta de conhecimento, não pedido de especificação

---

## Ambiguous Cases (should ask clarification)

### TC-11: "Me ajuda com o projeto"
**Input**: "Me ajuda com o projeto"
**Expected**: Perguntar: "Você quer criar uma spec (spec-generator) ou organizar commits (commit-architect)?"
**Reason**: Muito vago, ambas skills poderiam se aplicar

### TC-12: "Quero melhorar o código"
**Input**: "Quero melhorar o código do meu projeto"
**Expected**: Perguntar: "É uma nova funcionalidade (spec-generator) ou refatoração/organização de commits (commit-architect)?"
**Reason**: "Melhorar" pode ser feature nova ou refatoração

### TC-13: "Preciso documentar"
**Input**: "Preciso documentar minha API"
**Expected**: Perguntar: "É documentação de spec técnica (spec-generator) ou atualização de docs existente?"
**Reason**: Documentação pode ser spec nova ou apenas atualização

### TC-14: "Novo módulo de pagamentos"
**Input**: "Vou adicionar um módulo de pagamentos"
**Expected**: Perguntar: "Já tem a spec pronta? Se não, uso spec-generator. Se sim, vamos para implementação."
**Reason**: Pode ser antes ou depois da spec

### TC-15: "Organiza meus commits"
**Input**: "Organiza meus commits por favor"
**Expected**: Perguntar: "As mudanças já estão feitas? Se sim, uso commit-architect. Se está planejando, uso spec-generator."
**Reason**: Ambiguidade entre planejamento (spec) e pós-implementação (commit)

---

## Collision Cases (spec-generator vs commit-architect)

### CC-01: "Vou implementar X" (ambíguo: planejar vs commit)
**Input**: "Vou implementar o módulo de pagamentos"
**Expected**: Perguntar: "Já escreveu o código? Se não, spec-generator para planejar. Se sim, commit-architect para commitar."
**Reason**: "Vou implementar" pode ser intenção futura ou anúncio de conclusão

### CC-02: "Nova feature pronta" (ambíguo: spec vs commit)
**Input**: "Terminei a feature de relatórios, o que faço agora?"
**Expected**: commit-architect (prioridade: código pronto → commit)
**Reason**: Código pronto indica fase de commit; spec-generator seria prematuro

### CC-03: "Quero adicionar X e commitar" (dupla intenção)
**Input**: "Quero adicionar autenticação JWT e fazer commits limpos"
**Expected**: spec-generator primeiro (planejar antes de codificar)
**Reason**: Sequência natural: spec → code → commit; não pular spec

### CC-04: "Refatorar e documentar" (overlap docs)
**Input**: "Refatorei o código e quero documentar as mudanças"
**Expected**: commit-architect (docs vão no commit separado: docs(refactor): ...)
**Reason**: Docs de mudanças feitas pertencem ao commit, não a spec nova

### CC-05: "Começar do zero com commits organizados" (ordem)
**Input**: "Novo projeto, quero começar com commits organizados desde o início"
**Expected**: spec-generator primeiro (spec → code → commit)
**Reason**: Commits organizados pressupõem código; spec define o que codificar

---

## Positive Cases (should trigger agile-orchestrator)

### TC-16: Workflow completo do zero
**Input**: "Quero criar um novo projeto seguindo o workflow completo estruturado"
**Expected**: agile-orchestrator
**Reason**: Pedido explícito de workflow ponta-a-ponta

### TC-17: Iniciar projeto com checklist
**Input**: "Me dá o checklist completo para começar um projeto do zero"
**Expected**: agile-orchestrator
**Reason**: Quer o processo estruturado completo

### TC-18: "Siga o workflow agile"
**Input**: "Siga o workflow agile para meu novo sistema"
**Expected**: agile-orchestrator
**Reason**: Referência direta ao workflow

---

## Collision Cases (agile-orchestrator vs spec-generator)

### CC-06: "Novo projeto" (orchestrator vs spec)
**Input**: "Tenho uma ideia para um novo projeto"
**Expected**: spec-generator (mais específico: ideia → spec)
**Reason**: Orchestrator é para quando quer o processo TODO; spec-generator para quando tem a ideia e quer spec

### CC-07: "Workflow completo" vs "apenas spec"
**Input**: "Workflow completo para app de delivery"
**Expected**: agile-orchestrator
**Reason**: "Workflow completo" = orchestrator; "gere spec para app" = spec-generator