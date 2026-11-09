# Guilherme — Três novos testes Cypress

## Preparação

Seguir [CONTRIBUTING](../../CONTRIBUTING.md) e começar no clone com main atualizada e trabalho anterior guardado. Se esta alteração já estiver integrada, não reaplicar. Branch proposta: `guilherme/cypress-acesso`.

## Aplicação

```bat
git switch -c guilherme/cypress-acesso
git apply --check contribuicoes/guilherme/alteracoes.patch
git apply contribuicoes/guilherme/alteracoes.patch
git diff
```

Se a verificação falhar, parar e conferir o estado do arquivo e da branch; não forçar. O teste usa os arquivos após aplicação.

## Verificação

```bat
npm run cy:run
```

Manter Flask iniciado, instalar Node.js LTS e executar npm install antes. O arquivo original tem dois casos; acesso.cy.js acrescenta três. Ver [o roteiro completo de Cypress](../../docs/GUIA-DE-ESTUDO-E-APRESENTACAO.md#10-guia-completo-do-cypress-para-a-demonstração).

Arquivos da tarefa:

- `cypress/e2e/acesso.cy.js`

## Registro

Somente após revisar a mudança e os resultados:

```bat
git add cypress/e2e/acesso.cy.js
git diff --cached
git commit -m "test: ampliar Cypress para cinco cenarios de acesso"
git push -u origin guilherme/cypress-acesso
```

Abrir PR e seguir o fluxo de revisão em CONTRIBUTING. Guardar os resultados reais; não declarar aprovação antes da execução.

## Estudo

Após executar, pode explicar: “Revisei e ampliei os cenarios de acesso no Cypress. Executei e conferi as assercoes de pagina inicial, credenciais e protecao da gestao.”

Saber responder: O que fazem visit, get, type, click e should? Por que isso nao comprova concorrencia de reservas?

A explicação detalhada das alterações e seus limites está no [guia da equipe](../../docs/GUIA-DE-ESTUDO-E-APRESENTACAO.md).
