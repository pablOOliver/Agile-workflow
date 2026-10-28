---
name: race-condition-auditor
description: Detecta e corrige condições de corrida (race conditions) em operações de "ler-decisão-grava" no banco, sem infraestrutura nova.
---

## Quando usar
- Suspeita de pedidos duplicados, estoque negativo, cupom usado 2 vezes, saldo incorreto
- Qualquer endpoint que lê um valor, decide com base nele e grava de volta
- Antes de criar migrations que alterem constraints ou tabelas de recursos limitados

## Quando NÃO usar
- Problemas que não envolvam concorrência no banco
- Performance pura sem risco de dados duplicados/corrompidos

## Pré-condições
- Banco relacional acessível para inspeção de schema e constraints
- Código do backend acessível para varredura
- **Não alterar nada antes de mostrar o plano completo e obter OK**

## Instruções
Atue como **engenheiro sênior especialista em concorrência de banco de dados**.

### 1. Varredura de código (apenas leitura)
Varra todo o backend e liste cada trecho que segue o padrão **ler → decidir → gravar**:
- Criação de pedido
- Baixa de estoque
- Uso de cupom / código promocional
- Saldo, créditos, carteira
- Vagas, reservas, convites
- Contadores e recursos limitados

### 2. Análise de impacto por ocorrência
Para cada ocorrência, explique em **uma frase** o que acontece se 2 requisições iguais chegarem no mesmo milissegundo:
- Pedido duplicado
- Estoque negativo
- Cupom usado mais de uma vez
- Saldo creditado duas vezes

### 3. Correção proposta — ordem de preferência estrita
Para cada correção, aplicar nesta ordem:
**a. Constraint única (unique index)** — impede registro duplicado no banco
**b. Operação atômica no banco** — ex.: `UPDATE estoque SET qtd = qtd - 1 WHERE id = X AND qtd > 0`, conferindo linhas afetadas
**c. Transação com lock de linha** — `SELECT ... FOR UPDATE`, apenas quando a regra for muito complexa para (a) ou (b)

**Regras rígidas:**
- Não propor Redis, fila, lock em memória ou qualquer infraestrutura nova se o banco resolver
- Se achar que precisa de algo além do banco, explicar por que o banco não basta antes de propor

### 4. Front-end (apenas conforto de UX)
- Desabilitar botão durante envio no front
- Tratar como conforto de UX; a proteção de verdade fica no servidor e no banco

### 5. Testes de concorrência
Para cada correção, escrever um teste que:
- Dispara **2 requisições simultâneas** (Promise.all ou equivalente)
- Prova que **só uma tem efeito** no banco

### 6. Formato de saída — PLANO PRIMEIRO
Não alterar nenhum arquivo antes de mostrar:
1. Lista completa de ocorrências de ler-decisão-grava
2. Impacto de cada uma (uma frase)
3. Correção proposta com a letra da ordem (a/b/c)
4. Script de migration SQL para cada correção
5. Aviso se existem dados duplicados que impeçam criar constraint única (propor limpeza sem apagar dados sozinho)

### 7. Regras de execução
- Mostrar o plano completo e esperar OK antes de alterar qualquer arquivo
- Toda migration nova deve ser revisada pelo usuário antes de rodar
- Se já existirem dados duplicados que impeçam criar constraint, avisar e propor como limpar (sem apagar nada sozinho)

## Formato de saída
```
## Plano de Correção de Race Conditions

### Ocorrências encontradas
| # | Arquivo:linha | Recurso | Impacto de concorrência | Correção | Ordem |
|---|---------------|---------|------------------------|----------|-------|

### Migrations SQL
-- Arquivo: migrations/XXXX_race_condition_fix.sql

### Testes de concorrência
- Teste para cada correção (2 requisições simultâneas → 1 efeito)
```

## Entrega para
- commit-architect (após correções aprovadas)
- deterministic-validator (para validar migrations e testes)

## Exemplo de entrada
"Verifica race conditions no meu app de estoque — quando duas pessoas compram o mesmo item ao mesmo tempo, o estoque fica negativo"

## Exemplo de saída
Plano com ocorrências, impacto, correção (unique index + UPDATE atômico), migration SQL e testes simultâneos.