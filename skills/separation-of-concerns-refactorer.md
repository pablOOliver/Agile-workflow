---
name: separation-of-concerns-refactorer
description: Refatoração segura de arquivos grandes — divide em camadas (UI, regra de negócio, acesso a dados) sem mudar comportamento, com testes de caracterização primeiro.
---

## Quando usar
- Arquivo grande demais onde toda alteração quebra outra coisa
- Mistura de tela, regra de negócio e acesso a banco/serviço externo no mesmo arquivo
- Medo de abrir o arquivo para editar

## Quando NÃO usar
- Correção de bug específico (sem refatoração)
- Mudança de regra de negócio ou rotas públicas
- Introdução de nova framework ou biblioteca

## Pré-condições
- Caminho do arquivo a refatorar informado
- **Não corrigir bugs nem mudar regra de negócio durante a refatoração**
- **Não renomear rotas, props públicas ou colunas do banco**
- **Mostrar o plano e esperar OK antes do passo 1**
- **Testes de caracterização antes do primeiro passo**

## Instruções
Atue como **engenheiro sênior especialista em refatoração segura**.

### 1. Mapeamento do arquivo
Liste cada função, componente e trecho, classificando em uma das camadas:
**a. UI** — o que aparece na tela e captura evento do usuário
**b. Regra de negócio** — cálculos, validações, decisões
**c. Acesso a dados e serviços externos** — banco, Supabase, Stripe, APIs externas

### 2. Problemas identificados
Aponte:
- Dependências cruzadas entre camadas
- Código duplicado
- Estado global que dificulta a separação

### 3. Nova estrutura de pastas e arquivos
Proponha a nova estrutura seguindo o padrão que o projeto já usa. Nada de framework ou biblioteca nova.

### 4. Plano em passos pequenos
Cada passo:
- Move **um pedaço só**
- Mantém os mesmos nomes públicos
- Deixa o app funcionando

### 5. Testes de caracterização (ANTES do primeiro passo)
Verificar se existem testes cobrindo o comportamento atual. Se não existirem:
- Escrever **testes de caracterização** (registram o comportamento de hoje, mesmo que pareça errado)
- Para os fluxos principais do arquivo

### 6. Execução
- Executar **um passo por vez**
- Rodar os testes ao final de cada passo

### 7. Regras rígidas
- Não corrigir bugs durante a refatoração — anotar numa lista separada
- Não mudar regra de negócio
- Não renomear rotas, props públicas ou colunas do banco
- Mostrar o plano e esperar OK antes do passo 1

## Formato de saída — PLANO PRIMEIRO
```
## Plano de Refatoração — [CAMINHO DO ARQUIVO]

### Mapeamento por camada
| Camada | Funções/trechos | Linhas |

### Problemas
- Dependências cruzadas: ...
- Código duplicado: ...
- Estado global: ...

### Nova estrutura proposta
[estrutura de pastas]

### Passos de refatoração
| Passo | O que move | Testes de caracterização |

### Bugs encontrados (não corrigidos)
- ...
```

## Entrega para
- commit-architect (após refatoração completa)
- deterministic-validator (para validar testes após cada passo)

## Exemplo de entrada
"Refatora [CAMINHO DO ARQUIVO] que ficou grande — separa UI, regra de negócio e acesso a dados"

## Exemplo de saída
Mapeamento em 3 camadas, nova estrutura de pastas, plano de passos pequenos, testes de caracterização, lista de bugs encontrados (não corrigidos).