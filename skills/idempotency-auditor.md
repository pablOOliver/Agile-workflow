---
name: idempotency-auditor
description: Garante que webhooks e endpoints de pagamento aceitem repetição sem efeito duplicado (idempotência).
---

## Quando usar
- Webhooks de pagamento (Stripe ou outro gateway)
- Endpoints que cobram, liberam plano, creditam saldo ou enviam e-mail transacional
- Chamadas ao gateway de pagamento (criar cobrança, assinatura, reembolso)

## Quando NÃO usar
- Endpoints apenas de leitura (GET sem efeito colateral)
- Operações que não envolvam pagamento, crédito ou envio de e-mail transacional

## Pré-condições
- Código dos webhooks e endpoints de pagamento acessível
- Schema do banco acessível para criar tabela de eventos processados
- **Não alterar valores, preços nem regras de cobrança**
- **Mostrar o plano antes de alterar código**

## Instruções
Atue como **engenheiro sênior especialista em pagamentos**.

### 1. Mapeamento (apenas leitura)
Liste:
- Todos os webhooks recebidos (Stripe ou outro gateway)
- Todos os endpoints que cobram, liberam plano, creditam saldo ou mandam e-mail transacional

### 2. Webhooks — regras obrigatórias
Para cada webhook:
**a.** Confirme que a assinatura do webhook é verificada com o **corpo bruto** da requisição antes de qualquer processamento
**b.** Crie uma **tabela de eventos processados** com o ID do evento como chave única
**c.** Ao receber um evento, tente gravar o ID primeiro; se já existir, responda **200** e não faça mais nada
**d.** Não dependa da ordem de chegada dos eventos: quando precisar do estado atual, busque o objeto na API do gateway
**e.** Responda **2xx rápido** e mande o trabalho pesado para uma fila ou processamento assíncrono (se o projeto já tiver essa estrutura)

### 3. Chamadas ao gateway (saída)
Para criar cobrança, assinatura, reembolso:
- Envie uma **idempotency key (UUID v4)** gerada uma vez por operação de negócio
- Reaproveite a mesma chave em caso de nova tentativa

### 4. Endpoints de entrada (criar pedido/pagamento)
- Aceite um header **Idempotency-Key** do cliente
- Devolva a **mesma resposta** se a chave se repetir

### 5. Testes de idempotência
Escrever testes que:
- Enviam o **mesmo evento 2 vezes** → efeito acontece só uma vez
- Enviam o **mesmo evento 2 vezes ao mesmo tempo** (concorrência) → efeito acontece só uma vez

### 6. Regras rígidas
- Mostrar o plano antes de alterar código
- Não mudar valores, preços nem regras de cobrança
- Não usar dado pessoal (e-mail, CPF, telefone) como chave de idempotência

## Formato de saída — PLANO PRIMEIRO
```
## Plano de Idempotência

### Webhooks recebidos
| Webhook | Assinatura verificada | Tabela de eventos | ID único | Comportamento duplicado |
|---------|----------------------|-------------------|----------|------------------------|

### Endpoints de pagamento/cobrança
| Endpoint | Idempotency-Key aceita | Resposta duplicada igual |

### Chamadas ao gateway (saída)
| Operação | Idempotency key UUID v4 |

### Migrations SQL
-- Tabela de eventos processados

### Testes
- Mesmo evento 2 vezes sequenciais
- Mesmo evento 2 vezes simultâneas
```

## Entrega para
- commit-architect (após correções aprovadas)
- deterministic-validator (para validar migrations e testes)

## Exemplo de entrada
"Torna meus webhooks do Stripe idempotentes — o mesmo evento não pode liberar o plano duas vezes"

## Exemplo de saída
Plano com tabela de eventos processados, verificação de assinatura com corpo bruto, idempotency keys para chamadas de saída, e testes de duplicação.