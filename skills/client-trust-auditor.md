---
name: client-trust-auditor
description: Auditoria de segurança que nunca confia no cliente — move regras de negócio para o servidor, remove segredos do front, valida RLS no banco exposto.
---

## Quando usar
- Auditoria de segurança completa de app full-stack (frontend + backend + banco)
- Suspeita de preço/desconto/permissão calculado só no front
- Banco exposto por API (Supabase ou equivalente) com RLS

## Quando NÃO usar
- Apenas refatoração de código sem foco em segurança
- Projeto sem frontend ou sem banco exposto por API

## Pré-condições
- Código front e backend acessível para leitura
- Schema do banco acessível (para inspectar RLS e policies)
- **Primeiro só o relatório, sem alterar nada**
- **Aplicar correções uma por vez, com migration separada para policies**
- **Esperar OK do usuário em cada correção**

## Instruções
Atue como **auditor de segurança**. Parta do princípio de que **qualquer coisa que roda no navegador pode ser lida e alterada pelo usuário**.

### 1. Regras de negócio no front
Liste todo cálculo que existe **só no cliente**:
- Preço, desconto, frete
- Permissão, papel de admin
- Limite de plano
- Validação que só existe no cliente

Para cada um:
- Mova a regra para o servidor (API route, server action, edge function)
- O servidor **recalcula tudo e ignora valores vindos do cliente**

### 2. Segredos no front
Procure chaves e tokens:
- No código do front
- Em variáveis que vão para o navegador (`NEXT_PUBLIC_`, `VITE_`, `EXPO_PUBLIC_` ou equivalente)

Classifique cada uma:
- **Pública por design**: publishable/anon key do Supabase, publishable key do Stripe
- **Secreta**: service_role/secret key, chaves de OpenAI, Stripe secret, tokens de terceiros

Toda secreta **sai do front, vai para o servidor**. Indique quais precisam ser rotacionadas porque já foram publicadas.

### 3. Banco exposto por API (Supabase ou equivalente)
**a.** Liste todas as tabelas dos schemas expostos e diga quais estão com **RLS desligado**
**b.** Para cada policy existente, explique em português quem pode ler, inserir, alterar e apagar o quê
**c.** Aponte policies permissivas demais: `USING (true)`, `WITH CHECK (true)`, regras que não comparam com `auth.uid()`
**d.** Proponha policies mínimas:
- Cada usuário só acessa as próprias linhas
- Campos sensíveis (status de pagamento, papel, saldo) só mudam pelo servidor
**e.** Confirme que a chave secreta (service_role) **nunca** é usada no navegador

### 4. Relatório final
Gere relatório com:
- Achado
- Risco (alto, médio, baixo)
- Arquivo e linha
- Correção proposta

### 5. Regras de execução
- Primeiro: **só o relatório, sem alterar nada**
- Depois: aplicar correções uma por vez
- Migration separada para as policies do banco
- Esperar OK do usuário em cada uma
- Não desligar nenhuma proteção existente para "fazer funcionar"

## Formato de saída — AUDITORIA PRIMEIRO
```
# Relatório de Auditoria de Segurança

## 5 achados de maior risco (ordem)
1. [Achado] — Risco: alto/médio/baixo — Arquivo:linha — Correção

## Tabela detalhada por etapa
| Etapa | Achado | Risco | Arquivo:linha | Correção sugerida |

## Regras de negócio no front
| Regra | Localização | Ação |

## Segredos
| Chave | Tipo (pública/secreta) | Ação | Rotacionar? |

## Banco (RLS)
| Tabela | RLS ligado? | Policies permissivas | Policy mínima proposta |

### Próximas correções (uma por vez, aguardando OK)
1. ...
```

## Entrega para
- commit-architect (após correções aprovadas)
- deterministic-validator (para validar migrations de RLS)

## Exemplo de entrada
"Audita a segurança do meu app — não confio no que o front envia"

## Exemplo de saída
Relatório com 5 achados de maior risco, tabela detalhada por etapa, classificação de segredos, analysis de RLS, e plano de correções uma por vez.