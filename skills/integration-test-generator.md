---
name: integration-test-generator
description: Gera testes de integração que batem nas rotas de verdade com banco de teste separado, mockando apenas serviços externos.
---

## Quando usar
- Cobrir fluxos críticos com testes de integração (estilo RSpec request spec)
- Banco de teste separado do de produção
- Mock apenas de serviços externos (gateway de pagamento, e-mail, APIs de terceiros)

## Quando NÃO usar
- Apenas testes unitários com mock de tudo
- Testes E2E com Playwright (exceto opcional, aprovado separadamente)
- Banco de produção para teste

## Pré-condições
- Ferramenta de teste configurada ou a configurar
- Banco de teste separado (Supabase local, container ou projeto só de teste)
- **Nunca apontar para banco de produção**
- **Não apagar, pular (skip) ou afrouxar teste para fazê-lo passar**
- **Não mocke banco nem regra que está sendo testada**

## Instruções
Atue como **engenheiro de qualidade**.

### 1. Listar fluxos críticos
Liste todos os fluxos críticos do projeto:
- Cadastro
- Login
- Checkout
- Webhooks de pagamento
- Qualquer rota que mexa com dinheiro, permissão ou dado de outro usuário

### 2. Frases de comportamento (describe / it em português)
Para cada fluxo, escrever em português as frases no formato `describe / it` ("quando..., então..."), cobrindo:
**a.** Caminho feliz
**b.** Erros esperados (pagamento recusado, campo inválido, usuário sem permissão)
**c.** Repetição (clicar 2 vezes, webhook duplicado, 2 requisições ao mesmo tempo)
**d.** Limites (estoque zerado, plano expirado, valor zero ou negativo)
**e.** Acesso indevido (usuário A tentando ler ou alterar dado do usuário B)

### 3. Confirmação do usuário
Mostrar as frases e **esperar confirmação ou correção** antes de escrever testes. O usuário é a fonte da verdade sobre comportamento esperado.

### 4. Ambiente de teste
- Configurar com a ferramenta que o projeto já tem
- Se não tiver nenhuma, sugerir a mais simples para a stack e esperar OK
- Banco de teste separado: Supabase local, container ou projeto só de teste
- **Nunca banco de produção**

### 5. Escrever os testes
- Bater nas rotas de verdade (API routes, server actions, edge functions)
- Mock **só de serviço externo**; banco, regras de negócio e policies rodam de verdade
- Para repetição simultânea, disparar requisições ao mesmo tempo (`Promise.all` ou equivalente)

### 6. E2E opcional (apenas se aprovado)
- Um único teste E2E de fumaça (ex.: Playwright) para cadastro até checkout

### 7. Execução e relatório
- Rodar todos os testes
- Dizer o que passa e o que falha
- Teste que falha por **bug real fica falhando** e entra numa lista de bugs
- Não ajustar teste para passar

### 8. Comando único
Informar o comando único para rodar todos os testes, para o usuário rodar após toda alteração feita por IA

### 9. Regras rígidas
- Proibido apagar, pular (skip) ou afrouxar teste para fazê-lo passar
- Não mocke banco nem regra que está sendo testada
- Se um teste parecer errado, parar e perguntar

## Formato de saída — FRASES PRIMEIRO
```
## Testes de Integração — Plano

### Fluxos críticos identificados
1. Cadastro — tem teste de integração / só unitário / não tem
2. Login — tem teste de integração / só unitário / não tem
...

### Frases de comportamento (aguardando confirmação)
describe('fluxo X')
  it('quando [condição], então [resultado esperado]')
  it('quando [erro esperado], então [comportamento]')
  it('quando [repetição], então [resultado]')
  ...

### Ambiente de teste
- Ferramenta: ...
- Banco de teste: ... (separado da produção)

### Comando único para rodar todos os testes
npm test / pytest ... / etc.

### Testes E2E opcional (apenas se aprovado)
...
```

## Entrega para
- deterministic-validator (para rodar testes e validar cobertura)
- commit-architect (após testes aprovados)

## Exemplo de entrada
"Gera testes de integração para meus fluxos críticos — checkout e webhook de pagamento"

## Exemplo de saída
Frases describe/it em português para cada fluxo, configuração de banco de teste, testes que batem nas rotas reais com mock apenas de externas, comando único para rodar tudo.