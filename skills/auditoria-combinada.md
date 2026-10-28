---
name: auditoria-combinada
description: Auditoria completa dos 5 fundamentos (race condition, idempotência, confiança no cliente, separação de responsabilidades, testes de integração) sem alterar nenhum arquivo. Gera AUDITORIA.md na raiz.
---

## Quando usar
- Auditoria completa de app construído com IA
- Antes de iniciar qualquer correção, entender todos os riscos
- Gerar AUDITORIA.md com tabela de achados por etapa

## Quando NÃO usar
- Quando quiser alterar código (usar as skills individuais)
- Quando já existe AUDITORIA.md recente e não há mudanças no código

## Pré-condições
- **NÃO alterar nenhum arquivo do projeto**
- **Não rodar migration**
- **Não instalar nada**
- Somente leitura de código e comandos de leitura
- Se não conseguir verificar algo, escrever "não verificado" e o motivo, sem chutar

## Instruções
Atue como **engenheiro sênior fazendo uma auditoria completa**. Nesta tarefa você NÃO altera nenhum arquivo.

Siga esta ordem e, ao final de cada etapa, anote os achados antes de passar para a próxima:

### Etapa 1 — Testes de integração
- Existe ferramenta de teste configurada?
- Existe banco de teste separado do de produção?
- Qual o comando para rodar tudo?
- Rode (só se não tocar em produção) e diga quantos passam e quantos falham
- Liste os fluxos críticos (cadastro, login, checkout, assinatura, webhooks)
- Diga quais têm teste batendo na rota de verdade, quais só têm teste unitário com mock e quais não têm nada

### Etapa 2 — Confiança no cliente
- Regras de preço, desconto, permissão, papel de admin ou limite de plano que existem **só no front**
- Chaves e tokens em código de front ou em variáveis que vão para o navegador (`NEXT_PUBLIC_`, `VITE_`, `EXPO_PUBLIC_` ou equivalente). Classifique como pública por design ou secreta.
- Se houver Supabase (ou banco exposto por API): tabelas expostas com RLS desligado e policies permissivas demais (`USING (true)`, `WITH CHECK (true)`, regras que não comparam com `auth.uid()`). Explique cada policy em português.

### Etapa 3 — Race condition
- Todo trecho que lê, decide e depois grava sobre recurso limitado (estoque, cupom, saldo, crédito, vaga, convite)
- Para cada um, diga o que acontece se 2 requisições iguais chegarem juntas
- Se existe constraint única, operação atômica ou lock de linha no banco protegendo
- Aponte proteção que depende de lock em memória, lock no Redis com expiração ou leitura de cache, e diga se o banco sozinho resolveria

### Etapa 4 — Idempotência
- Webhooks recebidos: a assinatura é verificada com o corpo bruto?
- Existe registro de eventos processados com ID único?
- O que acontece se o mesmo evento chegar 2 vezes?
- Chamadas ao gateway de pagamento: usam idempotency key?

### Etapa 5 — Separação de responsabilidades
- Os arquivos mais longos do projeto
- Em cada um, se mistura tela, regra de negócio e acesso a banco ou serviço externo
- Aponte o candidato número 1 para refatorar

## Entrega — AUDITORIA.md na raiz

Crie o arquivo `AUDITORIA.md` com:

**Topo: 5 achados de maior risco em ordem**
1. [Achado] — Risco: alto/médio/baixo
2. ...

**Tabela por etapa (achado, risco, arquivo e linha, correção sugerida)**

| Etapa | Achado | Risco | Arquivo:linha | Correção sugerida |
|-------|--------|-------|---------------|-------------------|
| 1 | ... | ... | ... | ... |
| 2 | ... | ... | ... | ... |
| 3 | ... | ... | ... | ... |
| 4 | ... | ... | ... | ... |
| 5 | ... | ... | ... | ... |

**Final: qual dos 5 prompts de correção rodar primeiro e por quê**

## Regras rígidas
- Não alterar nenhum arquivo (exceto criar AUDITORIA.md)
- Não rodar migration
- Não instalar nada
- Se não conseguir verificar algo, escrever "não verificado" e o motivo, sem chutar
- Termine dizendo qual dos 5 prompts de correção rodar primeiro e por quê

## Formato de saída
O agente escreve o conteúdo do AUDITORIA.md e informa que o arquivo foi criado na raiz.

## Entrega para
- race-condition-auditor (se achados de race condition)
- idempotency-auditor (se achados de idempotência)
- client-trust-auditor (se achados de confiança no cliente / RLS)
- separation-of-concerns-refactorer (se achados de separação de responsabilidades)
- integration-test-generator (se achados de testes de integração)

## Exemplo de entrada
"Faça uma auditoria completa dos 5 fundamentos do meu app e gere o AUDITORIA.md"

## Exemplo de saída
AUDITORIA.md criado na raiz com 5 achados de maior risco, tabela detalhada por etapa, e recomendação de qual prompt de correção rodar primeiro.