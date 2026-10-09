---
name: spec-generator
description: Use quando o usuário precisa transformar uma ideia vaga em PRD ou spec técnica antes de escrever código.
---

## Quando usar
- Usuário tem uma ideia de funcionalidade ou projeto, mas não tem clareza técnica
- Precisa definir "o quê" e "por quê" antes de codificar
- Quer evitar scope creep com critérios de aceite claros
- Necessita de especificação técnica executável para AI coder

## Quando NÃO usar
- Usuário já tem PRD/Spec pronto e só quer implementar → use commit-architect
- Apenas quer gerar commits para mudanças já feitas → use commit-architect
- Tarefa puramente de refatoração ou bug fix sem nova funcionalidade

## Pré-condições
- Ideia ou requisito de alto nível fornecido pelo usuário
- Contexto do projeto (stack, arquitetura existente) se disponível
- **Quality Protocol (AGENTS.md):** Testes e critérios de aceite verificáveis definidos antes da implementação (TDD obrigatório)

## Instruções
Atue como Product Manager e Tech Lead Sênior. Gere dois documentos:

### 1. PRD (docs/prd.md)
- **Visão Geral**: Qual problema estamos resolvendo?
- **Público-alvo**: Quem usará essa funcionalidade?
- **User Stories**: Formato "Como [usuário], eu quero [ação], para que [valor]"
- **Critérios de Aceite**: Lista clara de "Check ou Fail" — **devem ser testáveis e servir como base para testes (TDD)**
- **Escopo e Fora de Escopo**: O que não faremos agora
- **Métricas de Sucesso**: Como saberemos se funcionou?

### 2. SPEC (docs/spec.md)
- **Arquitetura**: Estrutura de pastas, padrões de design (Clean Architecture, MVC)
- **Stack Tecnológica**: Linguagens, frameworks, bibliotecas específicas
- **Data Schema**: Modelagem de dados (tabelas, campos, tipos)
- **Endpoints/API**: Rotas, inputs e outputs esperados
- **Fluxo de Dados**: Como a informação viaja do frontend para o banco
- **Segurança e Performance**: Autenticação, rate limits, otimizações

Itere: peça PRD primeiro, revise, depois gere SPEC baseada no PRD aprovado.
Peça estrutura de pastas atual se repositório existir.
Ofereça diagramas Mermaid para fluxo de dados.
**Referência:** Quality Protocol em AGENTS.md (TDD, testabilidade, gates de qualidade)

## Formato de saída
- `docs/prd.md` (markdown)
- `docs/spec.md` (markdown)

## Entrega para
commit-architect — quando usuário aprovar spec e quiser iniciar implementação com commits organizados

## Exemplos
**Entrada**: "Sistema de controle de estoque de peças de moto que alerta quando nível de segurança é atingido e gera PDF de pedido de compra"

**Saída PRD**: docs/prd.md com visão geral, user stories (ex: "Como gerente, quero alerta automático para evitar falta de peças"), critérios de aceite, métricas

**Saída SPEC**: docs/spec.md com arquitetura (Clean Architecture), stack (Python/FastAPI), schema (tabelas peças, alertas, pedidos), endpoints (POST /alertas, GET /estoque), fluxo de dados, segurança