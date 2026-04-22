#v1.1
# variaveis 
export CLAUDE_CODE_GIT_BASH_PATH="C:\Users\pablo.oliveira\AppData\Local\Programs\Git\usr\bin\bash.exe" //caso der erro ao executar openclaude cli
sempre me responda em portugues brasil 
considere que estou em um SO win 10 ou 11 


Meu framework agile
//bloco produção
# passo 0 - preparar ferramentas  //esse bloco so sera visitado um vez ao iniciar o projeto
- instalar antigrtavity 
- instalar openclaude  e opencode (caso antigravity atinja limite)
- instalar plugin figma no openclaude 
	> tutorial: 'https://www.youtube.com/watch?v=VHESZ4GsoQk&t=188s'
- definir regras de convecional commits //criar tambem uma skil de commits
- instalar ferramenda stantard version 
- instalar skill caveman 
	claude plugin marketplace add JuliusBrussee/caveman
	claude plugin install caveman@caveman

# passo 1 - planejamento 
## arquivos.md
- crie prd, spec com a skill Spec_generator
- crie tambem agent, vision,  manifesto, bd etc... '''quando se cria um projeto com ia quais arquivos são necessrios ? 
## stacks
- essa aplicação pode ser criada para web? por que não ?
- node, next, vercel ou claudfare, vite(vinext) ou astro? 
# arquitetura
- semantic vesion

# passo 2 - implementação

# passo final (deployment) 
- faça commits (congelar estado funcional)
- Plan de teste (antes de qualquer code reviw - garantir o que ja funciona antes de melhorar)
- atualiza documentaçoes (congelar estado funcional)
	- criar uma skill para atualizar documentaçoes 
	- update changelogs (semantic version)
- code reviw (antes de qualquer merge - garantir melhor entrega)
- teste pos reviw 
- commits  pos reviw
- gera changelog a partir dos convencciol commit (standard version)

- merge = main -> branch(feature) & merge branch -> main



//bloco melhoria visão olistica (não faz parte do fluxo de produção, mas em momentos oportunos devo fazer uma revisão geral, especialista e cirurgica desses ponto)
# tarefas e principios
- revisar teste (unitarios e integração)total  do software 
	- criar uma skil de testes (ou  usar o do antigravity tool kit)
- revisar performace total do software
	- revisão de notação BIG-O
	- revisão de over engineering 
- revisar segurança total do software 
	- senhas e permissoes de acesso no banco
- revisar experiencia total do software 
- revisar estetica total do software 
