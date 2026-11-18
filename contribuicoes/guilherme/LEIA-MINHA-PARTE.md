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

## Ampliação dos fluxos críticos

A branch `guilherme/cypress-fluxos-criticos` parte da `main` com a contribuição
anterior já integrada. A suíte usa o navegador, o Flask e o SQLite reais, com contas
demonstrativas e um cadastro fictício.

| Arquivo | Cenários verificados |
| --- | --- |
| `cypress/e2e/fila.cy.js` | Entrada com posição inicial, bloqueio de segunda fila ativa, cancelamento da fila e nova entrada. Sem presença, ninguém é chamado. A prioridade declarada mantém a posição inicial; depois de confirmada pela recepção, o cidadão prioritário é chamado antes do cidadão que chegou primeiro. A recepção inicia e conclui os atendimentos. |
| `cypress/e2e/agendamentos.cy.js` | Reserva com código de confirmação, recusa de reserva duplicada, cancelamento com reposição da vaga e nova reserva no mesmo horário. |
| `cypress/e2e/acesso.cy.js` | Página pública, credenciais inválidas e redirecionamento de visitante. O cidadão recebe 403 ao abrir recepção ou gestão, a recepção recebe 403 ao abrir gestão e o logout volta a exigir autenticação. |
| `cypress/e2e/filazero.cy.js` | Login da recepção e abertura do painel. Login do gestor e abertura da gestão. |

### Execução local

Instale Python 3.10+ e Node.js 22 (versão usada no CI), depois rode
`python -m pip install -r requirements.txt` e `npm ci` na raiz do clone.
No Linux, o Cypress também requer as bibliotecas do navegador e o Xvfb.

Inicie o Flask com um banco temporário novo a cada execução da suíte. Os testes
criam registros que persistem no SQLite durante a execução. Deixe a porta 5000
livre e mantenha o servidor aberto enquanto roda o Cypress.

Linux/macOS:

```bash
e2e_dir=$(mktemp -d)
FILAZERO_DATABASE="$e2e_dir/filazero-e2e.sqlite3" python app.py
```

Windows PowerShell:

```powershell
$env:FILAZERO_DATABASE = Join-Path ([System.IO.Path]::GetTempPath()) "filazero-e2e-$([guid]::NewGuid()).sqlite3"
python app.py
```

Em outro terminal na raiz do clone, execute `npm run cy:run`. Para executar apenas
um arquivo, use, por exemplo, `npm run cy:run -- --spec cypress/e2e/fila.cy.js`.
Ao terminar, pare o Flask e descarte o banco temporário.

### GitHub Actions

Em pushes e PRs, o job `cypress-e2e` de `Quality checks` instala as dependências
com `npm ci`, inicia o Flask com SQLite temporário, aguarda uma resposta de
`/entrar` e executa a suíte em modo headless. Se o job falhar, o artefato
`diagnostico-cypress` contém o log do Flask e as capturas de falha disponíveis.
Os testes Cypress cobrem interações sequenciais e permissões de navegação.
Concorrência de reservas, check-in de agendamento e integrações externas ficam
fora desses cenários de navegador.
