---
name: commit-architect
description: Use quando o usuário já fez alterações no código e precisa gerar commits organizados, previsíveis e auditáveis seguindo Conventional Commits.
---

## Quando usar
- Usuário já implementou mudanças e quer commitá-las
- Precisa separar alterações em commits lógicos (feat, fix, refactor, docs, etc.)
- Quer preparar commits para Semantic Versioning
- Histórico de commits está bagunçado e precisa de organização
- Mudanças envolvem múltiplas responsabilidades (feature + fix + docs)

## Quando NÃO usar
- Usuário tem apenas uma ideia vaga sem código escrito → use spec-generator
- Precisa criar PRD ou Spec técnica antes de codificar → use spec-generator
- Nenhuma alteração foi feita no repositório ainda

## Pré-condições
- Alterações já realizadas no working tree (staged ou unstaged)
- Repositório git inicializado
- Entendimento do que foi alterado (arquivos modificados)
- **Quality Protocol (AGENTS.md):** Testes, lint/static analysis e coverage gates devem passar antes de gerar commits

## Instruções
Atue como especialista em Conventional Commits e histórico limpo.

### Quality Gate (Obrigatório — AGENTS.md)
Antes de gerar qualquer commit, verifique:
- [ ] Testes passam
- [ ] Lint/static analysis passa
- [ ] Coverage threshold respeitado (não redução sem justificativa)
Se qualquer gate falhar: **PARAR** e reportar falhas — não gerar commit.

### Processo Obrigatório

**Passo 1 — Inspecionar Alterações**
Identifique: criados, alterados, removidos, impacto no banco, automações, docs, deploy.
Gere resumo interno: Mudança, Objetivo, Risco, Escopo.

**Passo 2 — Agrupar Alterações**
Separe em grupos independentes por responsabilidade:
- Commit A: Infraestrutura
- Commit B: Nova funcionalidade
- Commit C: Correção
- Commit D: Documentação
Se dependem, ordene commits.

### Conventional Commits (Obrigatório)
Formato: `<tipo>(escopo): descrição curta`
Corpo opcional: contexto, motivação, impacto
Rodapé: BREAKING CHANGE, Refs, Closes

**Tipos Permitidos**: feat, fix, refactor, perf, docs, style, test, build, ci, chore, revert

### Regras de Escrita
- Verbo no infinitivo: adicionar, corrigir, remover, otimizar, implementar, atualizar
- Evitar: feito, ajustado, coisas, várias mudanças
- Descrição clara: `feat(inventario): adicionar sincronização offline` (bom) vs `feat: mudanças` (ruim)

### Política de Granularidade
Separar quando: mudança funcional, mudança estrutural, alteração de schema, atualização de docs, melhoria de performance
Não separar apenas por arquivo.

### Regras Especiais
**Snapshots**: `chore(snapshot): congelar estado funcional após validação`
**Banco de Dados**: Commits separados para migrations, schema, queries, sincronização
**Automações Python**: Separar refactor(pyautogui), feat(automacao), fix(processamento)
**Documentação**: Sempre commit separado: `docs(spec): atualizar PRD e documentação técnica`
**Versionamento**: `chore(release): preparar versão X.Y.Z` + standard-version

### Modo Estrito
PARAR se: commit > 15 arquivos, múltiplas responsabilidades, mensagem genérica
Nunca gerar: update, ajustes, misc, final, teste, wip, temp

## Formato de saída
- stdout (copiado pelo usuário) ou `.git/COMMIT_EDITMSG`
- Um plano de commit com: arquivos, objetivo, mensagem por commit

## Entrega para
(nenhuma — fim da cadeia; próximo ciclo pode voltar a spec-generator para nova feature)

## Exemplos
**Entrada**: Usuário fez alterações em 3 arquivos: novo service de pagamento, correção no validador, atualização do README

**Saída**:
## Plano de Commit

1. feat(pagamento): implementar service de processamento PIX
   Arquivos: src/services/payment.ts, src/types/payment.ts
   Objetivo: Nova funcionalidade de pagamento via PIX

2. fix(validacao): corrigir validação de caracteres especiais no login
   Arquivos: src/utils/validator.ts
   Objetivo: Correção de bug reportado

3. docs(readme): atualizar instruções de configuração de pagamento
   Arquivos: README.md
   Objetivo: Documentação da nova feature