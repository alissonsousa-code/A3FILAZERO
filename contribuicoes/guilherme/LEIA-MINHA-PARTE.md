# Guilherme — Três novos casos Cypress; cinco com os existentes

## Procedimento

Este pacote prepara a mudança. O responsável revisa, aplica e verifica antes de enviar. Cada commit deve usar o nome/e-mail do próprio membro e a conta autenticada correta.

Instalar Git para Windows. Clonar uma vez (quem já clonou entra na pasta existente):

```bat
git clone https://github.com/alissonsousa-code/A3FILAZERO.git
cd A3FILAZERO
```

Configurar seus dados reais:

```bat
git config user.name "SEU NOME COMPLETO"
git config user.email "SEU EMAIL DO GITHUB"
git status
```

Com a árvore de trabalho limpa, atualizar, criar branch e aplicar:

```bat
git switch main
git pull --ff-only origin main
git switch -c guilherme/cypress-acesso
git apply --check contribuicoes/guilherme/alteracoes.patch
git apply contribuicoes/guilherme/alteracoes.patch
git diff
```

Se --check falhar, pare e confira com a equipe se a mudança já foi integrada ou se houve alteração no trecho; não force nem substitua app.py inteiro. Os patches de Cláudio e Arthur foram preparados para trechos diferentes e verificados em conjunto. Não reaplique o mesmo patch.

Instalar dependências Python na venv e verificar a alteração:

```bat
python -m pip install -r requirements-dev.txt
npm run cy:run
```

Para Cypress, instalar Node.js LTS, executar npm install e manter python app.py em outro CMD. O teste original continua com dois casos; acesso.cy.js adiciona três. O usuário inexistente do cenário inválido evita bloqueio da conta de demonstração. Cypress precisa ser executado no computador do grupo.

Arquivos afetados (após aplicar):

- `cypress/e2e/acesso.cy.js`

Após revisar e testar:

```bat
git add cypress/e2e/acesso.cy.js
git diff --cached
git commit -m "test: ampliar Cypress para cinco cenarios de acesso"
git push -u origin guilherme/cypress-acesso
```

No GitHub, abrir Pull Request para main e pedir revisão a colega diferente. Guardar URL, diff e resultado do teste. Não adicionar as alterações de outros membros junto com sua tarefa. Os patches já versionados em contribuicoes são material de preparação; o commit individual é a aplicação revisada no código e seus testes.

## Como explicar depois de executar

“Revisei e ampliei os cenarios de acesso no Cypress. Executei e conferi as assercoes de pagina inicial, credenciais e protecao da gestao.”

Use essa fala só depois de executar e conferir o resultado. Diga o que realmente mudou e explique o apoio recebido quando pertinente.

## Estudar para responder

O que fazem visit, get, type, click e should? Por que isso nao comprova concorrencia de reservas?

## Verificação disponível

A preparação combinada passou em 16 testes Python, Ruff e Bandit. A sintaxe do novo arquivo JavaScript foi verificada com Node. Isso não substitui a validação individual; Cypress e GitHub Actions desta proposta ainda não foram executados nesta preparação. As demais lacunas do protótipo, inclusive nova reserva após cancelamento, continuam pendentes.
