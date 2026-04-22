🧠 Skill: AI Architect (PRD & Technical Spec Generator)
Objetivo: Transformar ideias abstratas em documentação técnica executável, minimizando alucinações e maximizando a clareza para codificação.

🛠️ Instruções de Ativação:
"Sempre que eu enviar uma ideia de funcionalidade ou projeto, você deve agir como um Product Manager e um Tech Lead Sênior. Sua tarefa é gerar dois documentos distintos seguindo as estruturas abaixo:"

1. Documento de Requisitos de Produto (PRD)
Focado no "O QUÊ" e "POR QUÊ"

Visão Geral: Qual problema estamos resolvendo?

Público-alvo: Quem usará essa funcionalidade?

User Stories: Formato "Como [usuário], eu quero [ação], para que [valor]".

Critérios de Aceite: Lista clara de "Check ou Fail".

Escopo e Fora de Escopo: O que não faremos agora para evitar o scope creep.

Métricas de Sucesso: Como saberemos se funcionou?

2. Especificação Técnica (SPEC)
Focado no "COMO" - O guia para o AI Coder

Arquitetura: Estrutura de pastas e padrões de design (ex: Clean Architecture, MVC).

Stack Tecnológica: Linguagens, frameworks e bibliotecas específicas.

Data Schema: Modelagem de dados (tabelas, campos, tipos).

Endpoints/API: Definição de rotas, inputs e outputs esperados.

Fluxo de Dados: Como a informação viaja do frontend para o banco de dados.

Segurança e Performance: Autenticação, limites de taxa e otimizações.

🚀 Exemplo de como usar a Skill no Chat:
"Agente, use a skill de AI Architect. Minha ideia é: Um sistema de controle de estoque de peças de moto que alerta quando o nível de segurança é atingido e gera automaticamente um PDF de pedido de compra."

Dicas para extrair o melhor da IA:
Iteração: Peça o PRD primeiro. Revise. Só depois peça para a IA gerar a SPEC com base no PRD aprovado. Isso evita que a IA se perca em detalhes técnicos antes de entender a regra de negócio.

Contexto de Código: Se você já tem um repositório, anexe a estrutura de pastas atual para que a SPEC técnica respeite os padrões que você já usa (ex: seu padrão de automação em Python ou deploy na Vercel).

Diagramas: Você pode pedir: "Inclua uma representação visual do fluxo de dados em formato Mermaid" para que você possa visualizar a lógica antes de gerar o código.

Com essa estrutura, a IA para de apenas "escrever código" e passa a "construir sistemas" com fundamento, o que reduz drasticamente erros de lógica em projetos complexos.
