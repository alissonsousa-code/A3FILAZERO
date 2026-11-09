# FilaZero — execução da equipe e parte do Alisson, do zero à apresentação

**Guia operacional para Windows / Prompt de Comando (CMD)**  
UNIFACS · Gestão e Qualidade de Software · Trabalho A3  
Repositório: <https://github.com/alissonsousa-code/A3FILAZERO>

Este documento explica como realizar as tarefas, identificar falhas, produzir evidências e preparar a apresentação. O ponto de partida informado por Alisson é: ainda não clonou o repositório pelo Git. As contribuições foram preparadas com apoio de IA; cada responsável precisa entender, aplicar e verificar sua parte antes de apresentá-la como trabalho executado.

## 1. O que já está pronto e o que você ainda precisa fazer

O código-base está publicado. Os pacotes de alterações estão em `contribuicoes/`, separados por integrante. Eles não alteram a aplicação apenas por estarem nessa pasta: cada integrante aplica seu patch em uma branch e propõe a integração pelo Pull Request.

Na conferência feita para este guia, `main` ainda tinha o título genérico em `templates/error.html`, e `tests/test_error_pages.py` ainda não estava integrado. Portanto, a parte de Alisson estava pendente de aplicação. Se o repositório mudar depois, confira novamente antes de aplicar o patch.

A contribuição de Alisson é melhorar mensagens da interface de erro e verificar dois comportamentos por testes Python. É uma parte concreta e delimitada; não corresponde a ter desenvolvido sozinho todo o site. Sua coordenação e documentação continuam conforme o plano da equipe.

### Entenda os cinco passos

1. Clonar: trazer o repositório e seu histórico para o computador.
2. Aplicar e estudar: incorporar a alteração preparada e entender a diferença.
3. Testar: verificar o comportamento e guardar o resultado real.
4. Commit/push/PR: registrar, enviar e pedir revisão.
5. Integrar e apresentar: verificar a versão final e explicar com evidências.

## 2. Abrir o documento e os arquivos

O .docx abre no Word, Word online, LibreOffice Writer ou Google Documentos. A versão publicada no GitHub pode ser lida diretamente no navegador. Você não precisa de Cypress para ler este guia.

O código pode ser lido no GitHub ou no Visual Studio Code. No VS Code, usar Arquivo → Abrir Pasta → pasta A3FILAZERO. Arquivos `.py` são Python, `.html` são templates de tela e `.cy.js` são testes Cypress. Arquivos `.patch` representam diferenças que o Git aplica; não editar esses arquivos no Word.

Os comandos deste guia são para CMD. Copie somente as linhas do bloco, uma de cada vez, e pressione Enter. Não copie o nome do bloco ou as marcas de formatação. Um terminal executando Flask não aceita outro comando até o servidor parar: para outras ações, abra um segundo CMD.

## 3. Alisson: instalar Git e Python

### 3.1 Git

Baixe Git para Windows em <https://git-scm.com/downloads/win>. Instale e mantenha a opção que permite usar Git no terminal. Feche/reabra o CMD e execute:

```bat
git --version
```

Esperado: uma versão como `git version ...`. Se aparecer “não é reconhecido”, a instalação ou o PATH ainda não está correto; não avance para clone.

### 3.2 Python

Se já usou `python app.py` com sucesso, provavelmente já possui Python. Confira:

```bat
python --version
```

O projeto requer Python 3.10 ou superior. Se ausente, instalar pelo site oficial <https://www.python.org/downloads/> e marcar “Add Python to PATH”. Se Windows abrir a Microsoft Store ao digitar python, conferir instalação e aliases de execução. O comando `py --version` pode ajudar a identificar uma instalação disponível; caso use py, mantenha coerência na criação da venv.

Node.js não é necessário para os dois testes da sua parte. Ele será necessário para Guilherme executar Cypress e para a demonstração final de navegador.

## 4. Alisson: clonar em uma pasta nova

Abra o CMD pelo menu Iniciar e execute:

```bat
mkdir "%USERPROFILE%\FilaZero-Trabalho"
cd /d "%USERPROFILE%\FilaZero-Trabalho"
git clone https://github.com/alissonsousa-code/A3FILAZERO.git
cd A3FILAZERO
```

Se a pasta FilaZero-Trabalho já existir, mkdir pode avisar; entrar nela continua válido. Se A3FILAZERO já existir e contiver um clone, não clonar por cima. Entre nele e confira `git remote -v` antes de usar. Não apague uma pasta existente para contornar o aviso.

O clone cria uma pasta A3FILAZERO. Agora o CMD deve terminar com esse nome no caminho. Execute:

```bat
dir
git remote -v
git status
```

Em dir devem aparecer app.py, package.json, templates, tests e contribuicoes. O remote deve apontar para a conta alissonsousa-code e o repositório A3FILAZERO. O status de um clone novo normalmente informa branch main e árvore limpa.

**Não usar o diretório antigo extraído do ZIP para estes passos.** Ele pode não conter o histórico Git nem os pacotes atuais. No clone, o histórico já existe: não executar `git init` novamente.

### 4.1 Sua identidade

```bat
git config user.name "Alisson Sousa Santos"
git config user.email "SEU EMAIL VERIFICADO NO GITHUB"
git config --get user.name
git config --get user.email
```

Troque o texto do e-mail pelo endereço verificado da sua conta GitHub ou pelo noreply fornecido nas configurações dela. As aspas fazem parte do comando. Não configure o nome de outro integrante. A conta autenticada no push também deve ser a sua; e-mail de autoria e autenticação são configurações diferentes.

### Ponto de conferência A

Você consegue ver os arquivos, o remote é o correto e o status não mostra mudanças inesperadas. Se algum resultado for diferente, guarde a mensagem e resolva antes de aplicar o pacote.

## 5. Alisson: preparar o ambiente Python

Na raiz A3FILAZERO:

```bat
python -m venv .venv
.venv\Scripts\activate.bat
python -m pip install -r requirements-dev.txt
```

A venv separa as dependências do projeto. O CMD normalmente mostra `(.venv)` após ativar. requirements-dev inclui as ferramentas de teste e as dependências da aplicação.

Confira:

```bat
python -m pytest --version
```

Se aparecer a versão de pytest, a ferramenta está disponível nesse Python. Se aparecer “No module named pytest”, confira se ativou a venv e se a instalação terminou sem erro. Não é necessário atualizar pip só por uma notificação de versão.

Execute a suíte antes da sua alteração:

```bat
python -m pytest -q
```

Registre o total real de testes. A base inicial tinha oito, mas outros PRs podem ampliar o número. Um erro aqui é um problema de base/ambiente a investigar, não um erro causado pela sua alteração ainda não aplicada.

Crie fora do clone uma pasta para evidências, pelo Explorador de Arquivos: Documentos → Evidencias-FilaZero → Alisson. Guarde print desse resultado como `01-base-antes.png`.

## 6. Alisson: identificar o problema antes da correção

### 6.1 Ver a tela 404

No CMD do projeto com venv ativa:

```bat
python app.py
```

Deixe esse terminal aberto. No navegador, visite:

```text
http://127.0.0.1:5000/pagina-inexistente
```

O servidor deve responder com uma página de erro. Antes da contribuição, o título central é genérico: “Não foi possível concluir”. A alteração não corrige uma rota ausente: ela melhora a explicação da resposta que já existe. Guarde `02-404-antes.png`.

### 6.2 O significado de cada código

| Código | Significado no contexto | Exemplo |
|---|---|---|
| 400 | Solicitação recusada por validação da requisição | POST sem token CSRF |
| 403 | Usuário não tem autorização para a ação | Cidadão acessa gestão |
| 404 | Caminho/recurso não encontrado | /pagina-inexistente |
| 500 | Erro interno não tratado no servidor | Não é corrigido por trocar o título da tela |

Uma resposta 400/403/404 pode ser o comportamento correto. O teste negativo passa se a recusa e a mensagem forem as esperadas. Não chamar todo código diferente de 200 de defeito.

### 6.3 Distinguir problema de interface e de negócio

Sua parte trata clareza das mensagens. O defeito da capacidade após check-in é de Arthur; a chamada sem presença é de Cláudio. Não alterar essas regras junto no seu commit. Se descobrir outra falha, registrar reprodução e encaminhar ao responsável, sem afirmar que seu template a resolve.

## 7. Alisson: aplicar a alteração preparada

Abra outro CMD na raiz do clone. Se fechou o servidor, também pode usar o primeiro terminal. Confira:

```bat
git status
git switch main
git pull --ff-only origin main
git switch -c alisson/mensagens-erros
git apply --check contribuicoes/alisson/alteracoes.patch
```

O `--check` só verifica, sem alterar os arquivos. Se terminar sem erro, execute:

```bat
git apply contribuicoes/alisson/alteracoes.patch
git status
git diff
```

Esperado: alteração em templates/error.html e arquivo novo tests/test_error_pages.py. git diff mostra arquivos rastreados; o arquivo novo ainda não rastreado pode não aparecer nele. Abra o arquivo novo no editor e use git status para confirmar sua presença. Após git add, git diff --cached mostrará ambos.

Se disser que a branch já existe, não recrie nem apague: confira `git branch` e `git status`; a tarefa pode já estar em andamento. Se o patch falhar, não use force e não substitua o arquivo inteiro por uma cópia antiga. Pode já estar aplicado ou haver mudança no mesmo trecho.

### Ponto de conferência B

A alteração está na sua branch, não diretamente na main, e não inclui arquivos de outros colegas. Não faça commit ainda: primeiro entenda e teste.

## 8. Alisson: entender o código linha por linha

### 8.1 Template templates/error.html

O trecho novo é equivalente a:

```html
{% set titles = {400: 'Confira os dados enviados',
                 403: 'Acesso não permitido',
                 404: 'Página não encontrada'} %}
<h1>{{ titles.get(code, 'Não foi possível concluir') }}</h1>
<p role="alert">{{ message }}</p>
```

- `{% set ... %}` cria uma variável no template Jinja, processado pelo servidor.
- O dicionário titles associa o número do erro a um título em português.
- `code` vem do tratamento do erro em app.py; não é um código digitado pelo usuário nessa tela.
- `titles.get(...)` busca o título. Se não existir uma chave, usa a frase genérica como fallback.
- `{{ ... }}` insere o resultado no HTML enviado ao navegador.
- `message` continua trazendo a orientação específica do servidor.
- `role="alert"` adiciona semântica de alerta; não comprova sozinho acessibilidade completa nem que todos os leitores de tela terão comportamento idêntico.
- O link “Voltar ao início” continua disponível para recuperação.

O código não altera a senha, autenticação, banco ou status HTTP. O status continua sendo definido pelas rotas/tratadores Flask.

### 8.2 Teste de página inexistente

```python
def test_not_found_shows_actionable_title_and_home_link(client):
    response = client.get('/pagina-inexistente')
    assert response.status_code == 404
    page = response.get_data(as_text=True)
    assert 'Página não encontrada' in page
    assert 'role="alert"' in page
    assert 'Voltar ao início' in page
```

client é um cliente Flask de testes; não é Chrome. get solicita uma rota. response contém a resposta. Cada assert define uma condição para aprovação. get_data(as_text=True) lê o HTML como texto. O teste confere código HTTP, título, atributo de alerta e orientação de retorno. Ele não verifica visualmente contraste, posição do botão ou todos os recursos WCAG.

### 8.3 Teste de POST sem CSRF

```python
def test_bad_csrf_shows_actionable_title(client):
    client.get('/entrar')
    response = client.post('/entrar', data={})
    assert response.status_code == 400
    assert 'Confira os dados enviados' in response.get_data(as_text=True)
```

Primeiro abre a página, depois envia um formulário vazio sem o token esperado. A proteção recusa a requisição. O teste verifica o título dessa recusa. Isso não é teste de “senha errada”: o bloqueio ocorre antes da validação de credenciais.

Os fixtures app/client são reutilizados de tests/test_app.py, com banco temporário. A nova suíte tem dois testes. O título 403 está mapeado no template, mas esses dois testes não verificam sua renderização: ele será conferido manualmente abaixo.

## 9. Alisson: executar e interpretar seus testes

Com venv ativa na raiz:

```bat
python -m pytest -q tests/test_error_pages.py
```

Resultado esperado: `2 passed`. Isso só se torna um resultado seu depois da execução real. Guarde `03-testes-alisson.png`, incluindo comando e resumo.

Se falhar, obtenha mais detalhes:

```bat
python -m pytest -v tests/test_error_pages.py
```

Leia o nome do teste, a linha de assert e o valor observado. Corrigir o comportamento/ambiente, não retirar uma asserção útil só para obter aprovação.

Depois execute regressão:

```bat
python -m pytest -q
python -m ruff check .
python -m bandit -r app.py
```

Guarde `04-regressao.png` e os resultados das ferramentas. Se outra contribuição ainda não estiver integrada, o total da suíte pode variar. Não usar “16 passed” de outro ambiente como resultado do seu computador.

### Se precisar corrigir algo

Abra o arquivo indicado na falha. Confira se o patch está aplicado, se o texto tem acentos iguais e se executou no clone/branch certo. Reexecute o teste que falhou; depois, se alterou código, reexecute a regressão pertinente. Se o erro estiver fora da sua parte, registre e combine com o responsável antes de mudar.

## 10. Alisson: conferir a interface depois

Se Flask já estava aberto durante a alteração, pare com Ctrl+C e inicie de novo com python app.py. Sem modo de recarga automática, o servidor pode continuar com uma versão antiga do template em memória.

### 10.1 Conferência 404

Abra novamente `/pagina-inexistente`. Agora o título deve ser “Página não encontrada”, com mensagem e link de retorno. Clique em Voltar ao início e confira que chega à home. Guarde `05-404-depois.png`.

### 10.2 Conferência 403

No navegador, faça login como cidadão usando a conta demonstrativa do README; na base preparada, `cidadao@filazero.local` e senha `Cidadao@123`. Depois navegue diretamente para `/gestao`.

Esperado: HTTP 403 e tela “Acesso não permitido”. Se estiver sem login, o sistema redireciona para login, e isso não é o cenário 403. Se estiver como gestor, a gestão abre, o que também não testa a recusa do cidadão. Use uma janela anônima para evitar misturar perfis. Guarde `06-403-cidadao.png`.

### 10.3 Conferência 400

O teste automatizado já cobre a renderização. Opcionalmente, com Flask ativo e em outro CMD:

```bat
curl.exe -i -X POST http://127.0.0.1:5000/entrar
```

Esse comando envia um POST sem token e mostra cabeçalhos/HTML. Esperado: status 400 e texto “Confira os dados enviados”. Não é necessário fazer essa demonstração ao vivo se ela confundir a apresentação. Se curl não estiver disponível, mantenha a evidência do teste pytest. Não digite esse comando no terminal ocupado pelo Flask.

### Registro simples da sua execução

Anote em um texto fora do clone: data; branch; ambiente; comando; resultado; nomes dos prints; qualquer falha; correção feita; teste repetido. Após criar o commit, acrescente seu identificador. Evidências produzidas antes dele devem corresponder aos mesmos arquivos registrados no commit; se mudar arquivos depois, reteste.

## 11. Alisson: registrar seu commit e abrir PR

Confira os arquivos antes:

```bat
git status
git diff
git add templates/error.html tests/test_error_pages.py
git diff --cached
```

O diff preparado deve conter só sua contribuição. Não incluir .venv, banco, node_modules ou alterações dos colegas. Então:

```bat
git commit -m "feat: orientar usuario nas paginas de erro"
git push -u origin alisson/mensagens-erros
```

No primeiro push, o gerenciador pode abrir o navegador para autenticação. Faça login na própria conta. Não digite senha/token em arquivos do projeto nem envie esses dados no chat.

Abra o repositório no GitHub → Compare & pull request. Base: main; comparação: alisson/mensagens-erros. Use uma descrição como esta, preenchendo resultado real:

> Problema: a tela compartilhada apresentava título genérico para erros diferentes. Mudança: títulos por status, mensagem com semântica de alerta e preservação do retorno ao início. Verificação: informar os dois testes, regressão e checagens manuais realmente executadas. Evidências: nomes/links dos registros. Limite: não representa certificação de acessibilidade nem correção de regras de negócio.

Peça revisão ao Filipe ou a outro colega diferente de você. Depois da revisão, integrar pelo merge. Guarde `07-commit.png`, link do PR e `08-pr-integrado.png`. Se o GitHub indicar conflito ou falha de Action, resolver/entender antes de declarar pronto.

Após integração:

```bat
git switch main
git pull --ff-only origin main
git log -1 --oneline
```

Confira se sua mudança está na main. Na versão integrada, execute novamente a verificação pertinente para confirmar que não foi perdida na junção. Antes da apresentação final, a equipe executa a suíte completa na main consolidada.

## 12. Diagnóstico: mensagens comuns e o que fazer

| Mensagem/situação | Significado provável | Próximo passo |
|---|---|---|
| git não é reconhecido | Git/PATH indisponível | Instalar e reabrir CMD |
| not a git repository | Pasta errada ou cópia ZIP | Entrar no clone A3FILAZERO e conferir remote |
| destination path already exists | Tentou clonar numa pasta existente | Verificar clone existente; não apagar automaticamente |
| No module named pytest | Ambiente/dependências incorretos | Ativar venv e instalar requirements-dev |
| file or directory not found no teste | Pacote não aplicado ou pasta errada | Conferir git status, tests/ e branch |
| branch already exists | Tarefa/branch já criada | Conferir branch e mudanças antes de continuar |
| patch does not apply | Base alterada ou patch já aplicado | Parar, conferir arquivo/diff; não forçar |
| AssertionError | Resultado observado não bate com esperado | Ler assert e resposta; conferir código e versão |
| connection refused no navegador | Servidor não está disponível | Iniciar Flask, conferir endereço/porta |
| título antigo após alteração | Servidor/cópia antigos | Confirmar pasta e reiniciar Flask |
| 403 virou tela de login | Tentativa sem sessão autenticada | Entrar como cidadão e repetir o cenário |
| nothing to commit | Sem diferença nova preparada | Conferir se já commitou, não gerar commit vazio |
| push rejeitado / permission denied | Conta, permissão ou histórico | Conferir conta autenticada e acesso; não usar force |

Não publique prints com tokens, cookies, senhas ou dados reais. Mostre somente o necessário para o diagnóstico.

## 13. Checklist da sua parte pronta para a entrega 3

- Clone correto e identidade própria confirmados.
- Branch criada e patch aplicado sem sobrescrever colegas.
- Você entende o dicionário, o fallback e a mensagem do template.
- Os dois testes foram executados e o resultado real foi guardado.
- A regressão pertinente passou, ou as falhas restantes estão registradas e encaminhadas.
- 404 foi conferido; 403 foi conferido com perfil de cidadão.
- Commit e PR mostram sua diferença e têm revisão de colega.
- Após merge, sua alteração está na main.
- Você sabe explicar limites da sua parte.

Isso conclui sua contribuição de interface/testes; não conclui sozinho a entrega 3 de todo o grupo.

## 14. O que estudar e falar — Alisson

### Estudar nesta ordem

1. Seu diff: saiba apontar o que foi removido e acrescentado.
2. HTTP 400/403/404 e a diferença para 500.
3. Flask gera a resposta; Jinja monta o HTML; navegador exibe.
4. Dicionário e get com fallback.
5. assert, fixture e cliente Flask.
6. Teste negativo e regressão.
7. Commit, branch, push, PR e merge.

### Fala de aproximadamente um minuto, depois de executar

“Minha contribuição foi revisar e aplicar melhorias na tela compartilhada de erros. Antes, situações diferentes mostravam o mesmo título. Ajustei o template para orientar o usuário conforme os códigos 400, 403 e 404, mantendo o detalhe da mensagem e o retorno ao início. Acrescentei dois testes Python para verificar a página inexistente e a requisição sem token. Executei os testes e registrei os resultados no meu commit e Pull Request. A mudança melhora a orientação, mas não resolve todas as regras do sistema nem comprova acessibilidade completa.”

Adapte os verbos ao que você realmente fez e mostre os resultados do seu computador. A preparação recebeu apoio; seu papel inclui entender, revisar, aplicar e verificar a contribuição.

### Demonstração curta

Abrir seu commit no GitHub e mostrar o diff do template. Mostrar o teste 404 e as asserções. Mostrar print antes/depois ou abrir a página inexistente. Apresentar o resultado real dos dois testes. Finalizar explicando por que uma recusa 400 correta faz um teste negativo passar.

### Perguntas e respostas para treinar

**Você corrigiu todos os erros do site?** Não. Ajustei a orientação da tela e verifiquei o recorte descrito. Defeitos de reserva e fila são tarefas separadas.

**Por que não mostrar só “Erro”?** Porque a pessoa precisa entender a situação e ter uma forma de continuar.

**O código 403 significa que o servidor quebrou?** Não. É recusa de autorização para um usuário identificado.

**Como o teste sabe que passou?** Pelas asserções de código, conteúdo e atributos esperados.

**Você usou Cypress nessa parte?** Usei testes pytest com cliente Flask. A automação de navegador Cypress está na parte de Guilherme, como ferramenta escolhida pelo grupo.

**O role alert garante acessibilidade?** Não. É uma medida semântica pontual; avaliação completa exige outros testes.

## 15. Equipe — como executar as demais partes

Todos seguem o fluxo comum: aceitar convite, clonar, configurar identidade, atualizar main, criar branch, conferir/aplicar patch, ler diff, executar teste, guardar evidências, commit/push e PR revisado. Cada nome abaixo é o identificador usado nos caminhos do repositório. As instruções individuais completas também estão em contribuicoes/.

### Cláudio

```bat
git switch main
git pull --ff-only origin main
git switch -c claudio/presenca-chamada
git apply --check contribuicoes/claudio/alteracoes.patch
git apply contribuicoes/claudio/alteracoes.patch
python -m pytest -q tests/test_presenca.py
git add app.py tests/test_presenca.py
git diff --cached
git commit -m "fix: chamar apenas pacientes com presenca confirmada"
git push -u origin claudio/presenca-chamada
```

Executar linha a linha, conferindo sucesso antes de avançar. Estudar waiting/present, seleção e UPDATE. Esperado: dois testes aprovados. Guardar comando/resultado, diff e PR. Demonstrar que cidadão sem presença não é chamado. Não confundir com aviso de proximidade, que não faz parte desse pacote.

### Arthur

```bat
git switch main
git pull --ff-only origin main
git switch -c arthur/capacidade-checkin
git apply --check contribuicoes/arthur/alteracoes.patch
git apply contribuicoes/arthur/alteracoes.patch
python -m pytest -q tests/test_capacidade_checkin.py
git add app.py tests/test_capacidade_checkin.py
git diff --cached
git commit -m "fix: manter ocupacao da vaga apos check-in"
git push -u origin arthur/capacidade-checkin
```

O teste cria capacidade 1, reserva para A, faz check-in e tenta reservar para B. Verifica recusa e proteção de bloqueio pelo gestor. Guardar resultado e explicar as quatro consultas ajustadas. A nova reserva após cancelamento é outro defeito, ainda pendente. Cláudio e Arthur devem coordenar as alterações de app.py e integrar um PR por vez.

### Guilherme

```bat
git switch main
git pull --ff-only origin main
git switch -c guilherme/cypress-acesso
git apply --check contribuicoes/guilherme/alteracoes.patch
git apply contribuicoes/guilherme/alteracoes.patch
```

Instalar Node.js LTS e conferir node --version e npm --version. Na raiz: npm install e npx cypress verify; se executável ausente, npx cypress install. Manter Flask em outro CMD. Rodar npm run cy:open para execução visual dos dois specs e npm run cy:run para execução conjunta. Esperado: cinco cenários distintos, sem presumir aprovação. Depois:

```bat
git add cypress/e2e/acesso.cy.js
git diff --cached
git commit -m "test: ampliar Cypress para cinco cenarios de acesso"
git push -u origin guilherme/cypress-acesso
```

Os cinco são login da recepção, login/gestão, home pública, credenciais inexistentes e gestão sem autenticação. Guardar resumo dos dois specs, versões, commit e falhas quando houver. O arquivo novo acrescenta três; não duplica os dois existentes. O guia de estudo detalha ações e asserções de cada um.

### Miguel

```bat
git switch main
git pull --ff-only origin main
git switch -c miguel/regressao-seguranca
git apply --check contribuicoes/miguel/alteracoes.patch
git apply contribuicoes/miguel/alteracoes.patch
python -m pytest -q tests/test_protecao_sessao.py
git add tests/test_protecao_sessao.py
git diff --cached
git commit -m "test: verificar CSRF sessao e cancelamento alheio"
git push -u origin miguel/regressao-seguranca
```

Os três testes verificam POST sem CSRF, inatividade e reserva alheia. Guardar resultado e explicar por que a consulta ao banco complementa a resposta HTTP. A inatividade é simulada no estado da sessão de teste; não houve espera cronometrada real de dezesseis minutos.

### Filipe

```bat
git switch main
git pull --ff-only origin main
git switch -c filipe/cobertura-ci
git apply --check contribuicoes/filipe/alteracoes.patch
git apply contribuicoes/filipe/alteracoes.patch
python -m coverage run --source=app -m pytest -q
python -m coverage report -m
python -m coverage xml -o coverage.xml
git add .github/workflows/quality.yml docs/metricas/COMO-MEDIR.md
git diff --cached
git commit -m "ci: publicar cobertura Python como artefato"
git push -u origin filipe/cobertura-ci
```

Abrir Actions → Quality checks → execução do commit. Conferir etapas e artefato cobertura-python. Guardar logs e percentual real, com recorte Python. Não presumir sucesso se a execução estiver pendente ou falhar. O workflow proposto não executa Cypress nem impõe novo limite mínimo de cobertura.

## 16. Como reunir evidências sem confundir versões

Cada membro guarda inicialmente fora do clone: print de execução, registro de ambiente, commit, diff e PR. Depois, o grupo seleciona evidências sem dados pessoais para anexos/repositório. Um print precisa permitir identificar cenário e resultado; uma imagem só com “passed” e sem contexto é fraca.

Modelo de registro:

| Campo | O que preencher |
|---|---|
| Responsável | Quem realmente executou |
| Data e ambiente | Computador, sistema e versões relevantes |
| Teste/cenário | Nome do teste e regra verificada |
| Commit/branch | Versão usada; antes do commit, identificar a alteração local |
| Esperado | Condições para aprovação |
| Observado | Resposta e estado vistos |
| Situação | Aprovado, falhou, bloqueado ou não executado |
| Evidência | Arquivo/URL |
| Defeito/retorno | Falha associada e eventual reteste |

Se executar antes do commit, registrar o commit depois e confirmar que os arquivos testados são os mesmos. Se alterar o código após o print, produzir evidência nova. Não usar o resultado de preparação do assistente como se fosse execução do integrante.

Sugestão de nomes: Alisson_404_antes.png, Alisson_404_depois.png, Alisson_pytest.png, Arthur_capacidade_reteste.png, Guilherme_cypress_resumo.png. Não expor senha, token, cookie ou dados pessoais.

## 17. Versão final integrada — fechar resultados do grupo

Depois dos seis PRs revisados e integrados, escolher um computador para a verificação final:

```bat
git switch main
git pull --ff-only origin main
git status
git rev-parse HEAD
python -m pytest -q
python -m ruff check .
python -m bandit -r app.py
python -m coverage run --source=app -m pytest -q
python -m coverage report -m
```

Guardar o hash e os resultados. Na preparação combinada dos pacotes houve 16 testes Python aprovados; o grupo precisa confirmar o resultado real da sua versão. O total pode mudar se houver novos testes.

Com Flask aberto em outro CMD, executar npm run cy:run. Guardar os cinco cenários, falhas ou aprovações e versão do Cypress. Se só houver dois testes, verificar se acesso.cy.js está integrado e atualizado no clone.

Somente marcar um defeito corrigido depois de reteste aprovado. Os pacotes não resolvem todas as lacunas. A falha de nova reserva após cancelamento, proximidade e gestão completa de horários precisam de decisão/atividades próprias.

### Métricas

Aprovação: aprovados / executados × 100, apresentando não executados à parte. Separar Python e Cypress. Cobertura: usar o relatório da versão final e declarar recorte app.py/Python. Taxa de correção: defeitos distintos corrigidos e retestados / registrados, com conjunto definido. Densidade: defeitos distintos / casos de uso analisados, indicando quais. Não inventar valores nem apresentar cobertura como garantia de ausência de defeito.

## 18. Documento e slides da terceira entrega

Com resultados reais: identificação/objetivo; arquitetura; ferramenta Cypress; cinco cenários e suas evidências; versionamento/contribuições; correções/retestes; métricas e interpretação; limitações; responsabilidade profissional; conclusão e referências. Conferir o template oficial antes de fechar.

Slides sugeridos: problema/equipe; arquitetura; regra e correção; Cypress/cenários; demonstração; segurança/regressão; GitHub/contribuições; métricas; limites/conclusão. Cada integrante mostra sua diferença e resultado, sem ler código inteiro.

Antes da aula: instalar dependências, testar o computador principal, guardar evidências offline, ensaiar e conferir a versão. Se usar gravação/prints como contingência, informar que são registros anteriores. Não prometer vídeo Cypress automático: a configuração original está com vídeo desativado.

Sua parte fica pronta quando os itens da seção 13 estão verificados; a entrega do grupo depende também dos demais PRs, cinco E2E executados, evidências e métricas finais. Os guias organizam a execução, mas não substituem os resultados.
