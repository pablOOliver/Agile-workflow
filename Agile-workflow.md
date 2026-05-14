# 🚀 Agile Workflow v1.3 | Pablo Silva

Este documento define o fluxo de trabalho para automação, desenvolvimento de sistemas e manutenção de infraestrutura, otimizado para Windows 10/11.

---

## 🛠️ Variáveis de Ambiente & Configurações

**Bash Path:** `export CLAUDE_CODE_GIT_BASH_PATH="C:\Users\pablo.oliveira\AppData\Local\Programs\Git\usr\bin\bash.exe"`

**Idioma:** Português (PT-BR)

**Log Logic:** Prioridade Total ao Banco de Dados. O log local é secundário para garantir 100% de confiabilidade no status dos processos.

---

## 🏗️ Passo 0: Preparar Ferramentas (One-Time)

Executado apenas uma vez ao iniciar o projeto.

### ✅ Ambiente de IA

- [ ] Instalar antigravity-toolkit
- [ ] Instalar openclaude e opencode (fallback para limites)
- [ ] Instalar plugin Figma no OpenClaude (Tutorial)

### ✅ Skill Caveman (Essencial)

- [ ] `claude plugin marketplace add JuliusBrussee/caveman`
- [ ] `claude plugin install caveman@caveman`

### ✅ Padronização

- [ ] Definir regras de Conventional Commits
- [ ] Instalar standard-version para versionamento semântico
- [ ] Criar skill de IA focada em gerar mensagens de commit padronizadas

---

## 📋 Passo 1: Planejamento

Definição de documentos e tecnologias.

### 1.1 Arquivos Estruturais (.md)

- [ ] **Documentação:** Criar PRD e Spec usando a skill Spec_generator
- [ ] **Arquivos de Projeto IA:** Gerar agent.md, vision.md, manifesto.md e esquema do BD

### 1.2 Stack & Arquitetura

- [ ] **Viabilidade:** Avaliar se a aplicação pode ser Web (Node, Next, Astro) ou se permanece via automação local (Python)
- [ ] **Deploy:** Definir destino (Vercel, Cloudflare ou servidor local)
- [ ] **Versionamento:** Implementar Semantic Versioning

---

## 💻 Passo 2: Implementação

Desenvolvimento ativo seguindo as especificações.

- [ ] Codificação baseada nas Tech Specs
- [ ] Manter sincronia entre scripts e banco de dados (evitar logs órfãos)

---

## 🚀 Passo Final: Deployment & QA

Garantia de entrega e congelamento de estado funcional.

### 📸 Snapshots
- [ ] Realizar commits para congelar o estado funcional

### 📝 Plano de Teste
- [ ] Executar antes do Code Review (garantir o que já funciona)

### 📚 Documentação
- [ ] Criar/Usar skill para atualização automática de docs
- [ ] Atualizar Changelogs via standard-version

### ⚡ Qualidade
- [ ] **Code Review:** Antes do merge (foco em segurança e performance)
- [ ] **Teste Pós-Review:** Validar correções
- [ ] **Commits Pós-Review**

### 🔀 Fluxo de Branch
`main → branch(feature) & branch → main`

---

## 🔍 Melhoria & Visão Holística

Revisão cirúrgica e especialista (não faz parte da produção diária).

- [ ] **Testes:** Revisar cobertura total (Unitários/Integração). Usar skill antigravity
- [ ] **Performance:** Análise de notação Big-O e remoção de Over-Engineering
- [ ] **Segurança:** Revisar credenciais de banco e permissões de acesso
- [ ] **Experiência (UX):** Revisar a fluidez do software e outputs de log
- [ ] **Estética:** Refinar interface e organização do código
