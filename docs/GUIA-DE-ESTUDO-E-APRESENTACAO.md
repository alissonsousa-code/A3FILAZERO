# FilaZero — guia de estudo, contribuições e demonstração

**UNIFACS · Gestão e Qualidade de Software · Trabalho A3**  
Material único de estudo para os seis integrantes · Preparação com apoio de IA

Repositório: <https://github.com/alissonsousa-code/A3FILAZERO>

## 1. Como usar e abrir este material

O documento reúne a base que todos precisam conhecer, a parte de cada integrante, os cenários de teste, um roteiro completo do Cypress e o processo de apresentação dos commits. Cada pessoa deve estudar a parte comum e sua seção individual. Ler o material não substitui aplicar, testar e entender a alteração.

**Arquivo .docx:** abrir com Microsoft Word no computador/celular, LibreOffice Writer ou enviar ao Google Drive e escolher “Abrir com Documentos Google”. Não precisa instalar Python ou Cypress para ler o documento. O Word online também pode abrir o arquivo enviado à própria conta.

**Código no GitHub:** clicar no nome do arquivo para ler diretamente no navegador. Depois de clonar o repositório, é possível abrir a pasta no Visual Studio Code: Arquivo → Abrir Pasta → A3FILAZERO. VS Code é um editor; não executa os testes automaticamente ao abrir o arquivo.

**Arquivos .py:** código Python do servidor ou dos testes pytest. **Arquivos .cy.js:** código JavaScript dos testes Cypress; ler no GitHub/VS Code e executar pelo Cypress. **Arquivos .patch:** alterações preparadas; aplicam diferenças sobre a base com `git apply`. Não abrir esses arquivos no Word para editá-los.

**Situação importante:** a base está na branch main. As seis contribuições foram preparadas como patches na pasta `contribuicoes/`; os arquivos novos e as correções só entram efetivamente no código quando o integrante aplica o pacote e o Pull Request é integrado. Depois de cada integração, conferir a versão usada na apresentação. Não aplicar de novo um patch que já entrou.

### Caminho de leitura

1. Todos: seções 2, 3, 10, 11 e 12.
2. Cada integrante: sua seção entre 4 e 9.
3. Guilherme e operador da demonstração: estudar e executar toda a seção 10.
4. Todos: abrir seu diff, explicar uma mudança concreta e relacioná-la ao resultado de um teste.

## 2. O que é o FilaZero e como funciona

O FilaZero é um protótipo web para organizar filas e agendamentos em UBS. O cidadão consulta unidades, entra na fila, acompanha posição e reserva horário. A recepção confirma presença e conduz chamada, início e conclusão. O gestor administra horários e consulta indicadores. Dados das unidades e contas do pacote são demonstrativos.

| Tecnologia | Função no projeto | Onde aparece |
|---|---|---|
| Python | Linguagem do servidor e de testes auxiliares | app.py e tests/ |
| Flask | Recebe requisições, controla rotas e monta respostas | create_app e funções de rota |
| SQLite | Persiste usuários, fila, reservas e avisos | arquivo local criado em instance/ |
| HTML/Jinja | Estrutura as telas e injeta dados do servidor | templates/ |
| CSS | Define aparência e layout | static/css/ |
| JavaScript | Máscara de CPF, confirmações e consulta periódica da fila | static/js/app.js |
| Cypress | Automatiza ações e verificações no navegador | cypress/e2e/ |
| pytest | Executa testes Python de unidade e integração | tests/ |
| coverage | Mede instruções/linhas Python exercitadas pelos testes | comandos locais e pipeline proposto |
| Git/GitHub | Histórico local e compartilhamento/revisão das alterações | commits, branches e Pull Requests |

### Exemplo: do clique ao banco

O cidadão preenche um formulário e clica em entrar na fila. O navegador envia um POST para `/fila/entrar`. Flask confere sessão, perfil, token CSRF, unidade e regras. O banco grava `queue_entries`. O servidor redireciona para a tela de acompanhamento. A posição permanece no servidor, não só no navegador.

GET normalmente consulta dados; POST envia uma ação. O controle precisa existir no servidor: esconder um botão não impede alguém de enviar uma requisição diretamente.

### Banco de dados

`users` guarda contas, perfis e hash de senha; `units`, as UBS; `queue_entries`, participações e etapas da fila; `slots`, serviço/data/hora/capacidade; `appointments`, reservas dos cidadãos; `notifications`, avisos; `audit_logs`, ações registradas. Chaves como user_id e slot_id ligam os registros. Hash de senha não é a mesma coisa que criptografar todo o banco.

### Fila e atualização

A prioridade declarada depende de confirmação na recepção. A ordem usa prioridade confirmada, horário de entrada e ID para desempate. A previsão é uma regra fixa: `(pessoas à frente + 1) × 15 minutos`; não é previsão por IA nem dado clínico real. O JavaScript consulta a API periodicamente — polling. O próximo ciclo é agendado cinco segundos após o anterior terminar; isso sozinho não comprova atualização em até cinco segundos.

## 3. Termos de teste que todos devem saber

| Termo | Significado | Exemplo do FilaZero |
|---|---|---|
| Cenário | Situação verificável com condições e resultado esperado | Gestor autentica e abre a gestão |
| Asserção | Verificação que precisa ser satisfeita | URL inclui /gestao; título está visível |
| Caixa-preta | Escolha do teste a partir do comportamento esperado | Credencial inválida deve ser recusada |
| Caixa-branca | Escolha conhecendo decisões e caminhos internos | Entradas que exercitam os dígitos do CPF |
| Unidade | Verificação de lógica pequena e isolada | Função valid_cpf |
| Integração | Verificação de partes trabalhando juntas | Rota, sessão e banco em teste Flask |
| E2E/sistema | Fluxo pelo navegador com aplicação funcionando | Cypress preenche login e abre painel |
| Regressão | Reexecutar verificações após mudanças | Conferir login e reservas depois de uma correção |
| Teste negativo | Verifica recusa correta de entrada/ação inválida | POST sem token deve retornar 400 |
| Fixture | Preparação reutilizável de teste | Aplicação e banco temporário do pytest |
| Mock/interceptação | Controle de uma interação para um cenário | Não equivale automaticamente a uma queda real de rede |

Ferramenta, técnica e nível são conceitos diferentes. Cypress é ferramenta, caixa-preta é técnica e sistema é nível. Um cenário negativo passa quando o sistema recusa corretamente; “entrada inválida” não significa “teste falhou”.

Os testes Python usam cliente HTTP Flask sem abrir um navegador real. Isso facilita preparar banco e verificar estados, mas não comprova layout ou funcionamento de JavaScript. Cypress exercita o navegador, mas cinco testes não demonstram todas as regras do sistema.

## 4. Alisson — mensagens de erro e orientação ao usuário

**Pacote:** `contribuicoes/alisson/`. **Branch proposta:** `alisson/mensagens-erros`.

**Arquivos após aplicar:** `templates/error.html` e `tests/test_error_pages.py`.

### Problema e alteração

A tela compartilhada usava um único título genérico para diferentes erros. O pacote associa títulos aos códigos HTTP e mantém o detalhe enviado pelo servidor. O parágrafo da mensagem recebe `role="alert"`, informação semântica para tecnologias assistivas. Esse atributo sozinho não comprova acessibilidade completa.

```html
{% set titles = {400: 'Confira os dados enviados',
                 403: 'Acesso não permitido',
                 404: 'Página não encontrada'} %}
<h1>{{ titles.get(code, 'Não foi possível concluir') }}</h1>
<p role="alert">{{ message }}</p>
```

Jinja avalia o dicionário no servidor. `code` e `message` são fornecidos pelo tratamento do erro no Flask. `get` seleciona o título e oferece uma alternativa para códigos não mapeados. O link “Voltar ao início” continua permitindo recuperação.

### Dois cenários de teste

1. **Página inexistente:** acessar `/pagina-inexistente`. Esperado: HTTP 404, título “Página não encontrada”, mensagem com papel de alerta e link de retorno. Isso verifica tanto o status quanto a orientação da tela.
2. **Envio sem CSRF:** abrir login e enviar POST sem o token. Esperado: HTTP 400 e título “Confira os dados enviados”. Não é teste de senha incorreta: a requisição é bloqueada antes da autenticação.

Executar na raiz do projeto:

```bat
python -m pytest -q tests/test_error_pages.py
```

### Como demonstrar e explicar

Abrir o diff do template e o arquivo de testes. No navegador, mostrar uma URL inexistente. Após aplicar e verificar, pode dizer: “Ajustei a apresentação dos erros para orientar a recuperação do usuário e conferi o comportamento com dois testes.”

**Perguntas para estudar:** qual a diferença entre 400, 403 e 404? O que faz o fallback de `get`? Por que manter mensagem e título? O que o teste não comprova? Não afirmar que essa mudança certifica WCAG ou resolve todos os erros.

## 5. Cláudio — chamada exige presença confirmada

**Pacote:** `contribuicoes/claudio/`. **Branch:** `claudio/presenca-chamada`.

**Arquivos:** `app.py`, na função `call_next`, e `tests/test_presenca.py`.

### Problema e alteração

Na base, a seleção aceita estados waiting e present. A primeira entrega prevê chamada de paciente presente. O pacote restringe seleção e atualização a `present`, mantendo a ordenação por prioridade confirmada e chegada.

```sql
-- Antes
WHERE unit_id=? AND status IN ('waiting','present')
-- Depois
WHERE unit_id=? AND status='present'
```

`waiting` significa entrada na fila sem confirmação da chegada; `present` significa chegada registrada. Não é preciso remover o cidadão waiting da fila: ele permanece esperando confirmação. O filtro da seleção escolhe elegíveis; o filtro do UPDATE protege a transição de estado esperada. A transação existente continua na função.

### Dois cenários

1. **Somente cidadão waiting:** recepção solicita chamada. Esperado: ninguém é chamado; o estado continua waiting. O teste confere o banco.
2. **Waiting entrou antes de um present:** criar os dois estados, com o waiting mais antigo. Esperado: o present é chamado, mesmo tendo entrado depois; o waiting permanece waiting. Isso mostra que presença é pré-condição da chamada, sem mudar a regra de prioridade entre elegíveis.

```bat
python -m pytest -q tests/test_presenca.py
```

### Como demonstrar e explicar

Entrar como cidadão e aderir à fila. Como recepção, tentar chamar antes da presença e depois confirmar a presença e repetir. Usar massa conhecida para não chamar outro paciente por engano. Após verificar: “Ajustei a regra para chamar somente pacientes presentes e testei a fila sem presentes e a fila mista.”

**Estudar:** diferença de estado e prioridade; por que alterar SELECT e UPDATE; função da transação; por que uma chamada não deve depender apenas do botão da tela. Essa contribuição não implementa o aviso de proximidade nem todos os fluxos de atendimento.

## 6. Arthur — capacidade preservada após check-in

**Pacote:** `contribuicoes/arthur/`. **Branch:** `arthur/capacidade-checkin`.

**Arquivos:** `app.py` em quatro consultas de capacidade e `tests/test_capacidade_checkin.py`.

### Problema e causa

Uma reserva começa `booked` e muda para `checked_in` quando a recepção confirma a chegada. A base conta apenas booked. Assim, uma vaga de capacidade 1 pode parecer vazia depois da chegada e permitir uma segunda reserva. A chegada não significa cancelamento ou liberação da capacidade do horário.

```sql
-- Antes
COUNT(*) ... WHERE slot_id=? AND status='booked'
-- Depois
COUNT(*) ... WHERE slot_id=?
  AND status IN ('booked','checked_in')
```

A mesma regra é usada na listagem da agenda, validação da reserva, listagem da gestão e decisão de bloquear horário. Corrigir só a tela deixaria a rota vulnerável a requisição direta; corrigir só a rota deixaria a interface inconsistente.

### Cenário de regressão, passo a passo

1. Criar um horário do dia às 23h50 com capacidade 1 em banco temporário.
2. Cidadão A reserva esse horário.
3. Recepção confirma a chegada; a reserva de A vira checked_in.
4. Cidadão B tenta reservar o mesmo slot.
5. Esperado: mensagem de vaga ocupada; banco mantém apenas a reserva checked_in.
6. Gestor tenta bloquear o horário.
7. Esperado: bloqueio recusado e horário continua ativo, pois há ocupação.

```bat
python -m pytest -q tests/test_capacidade_checkin.py
```

O horário e os perfis são preparação de teste, não regra de negócio para operar UBS às 23h50. As sessões são separadas para não confundir permissões. O teste verifica resultado e banco, não só HTTP 200.

### Como demonstrar e explicar

Mostrar o filtro SQL antes/depois e a sequência do teste. Após verificar: “Corrigi a definição de ocupação para incluir quem já fez check-in e mantive essa regra consistente na agenda, reserva e gestão.”

**Estudar:** capacidade vs. número de reservas; diferença entre booked, checked_in e cancelled; por que BEGIN IMMEDIATE não corrige uma regra de contagem errada. Esse pacote não resolve o defeito separado de reservar novamente depois de cancelar; não afirmar que todos os problemas de reserva foram corrigidos.

## 7. Guilherme — cinco cenários Cypress

**Pacote:** `contribuicoes/guilherme/`. **Branch:** `guilherme/cypress-acesso`.

**Código:** `cypress/e2e/filazero.cy.js` já contém dois testes. O pacote acrescenta `cypress/e2e/acesso.cy.js`, com três. Manter os dois arquivos para totalizar cinco; não duplicar os dois originais em um terceiro arquivo.

### Configuração e comandos

`package.json` declara a dependência Cypress e os scripts `cy:open` e `cy:run`. `cypress.config.js` define `baseUrl: 'http://127.0.0.1:5000'`, padrão `cypress/e2e/**/*.cy.js` e `video: false`. Portanto, testes de ambos os arquivos são localizados; a gravação de vídeo não está habilitada nessa configuração.

| Comando | O que significa no teste |
|---|---|
| describe | Agrupa cenários relacionados |
| it | Define um cenário; o texto é seu nome no resultado |
| cy.visit('/entrar') | Abre a rota usando baseUrl |
| cy.get('input[name="identifier"]') | Localiza campo pelo seletor CSS |
| .type('...') | Digita no campo encontrado |
| .click() | Aciona o elemento |
| cy.contains('...') | Busca elemento contendo o texto |
| .should('be.visible') | Afirma que está visível |
| cy.url().should('include', '/equipe') | Verifica parte do endereço atual |

Cypress enfileira comandos e repete consultas/asserções aplicáveis até o timeout. Não confundir essa repetição com tentar corrigir automaticamente uma falha do sistema. Evitar `cy.wait(5000)` como solução genérica: preferir aguardar uma condição observável.

### Cenário 1 — recepção autentica e abre painel

**Arquivo:** filazero.cy.js. **Base existente.**

Pré-condições: Flask iniciado, banco inicializado e conta de recepção disponível. Abrir `/entrar`, preencher `recepcao@filazero.local` e senha de demonstração `Recepcao@123`, clicar em enviar.

Esperado: URL contém `/equipe`; “Painel da recepção” visível; botão/texto “Chamar próximo paciente” visível. Isso confirma acesso da conta e presença da ação, mas não executa uma chamada nem valida prioridade.

### Cenário 2 — gestor autentica e acessa gestão

**Arquivo:** filazero.cy.js. **Base existente.**

Abrir login, preencher `gestor@filazero.local` e `Gestor@123`, enviar. Conferir passagem para `/equipe`; navegar para `/gestao`.

Esperado: URL inclui `/gestao`; o fluxo deve mostrar “Gestão da unidade” e “Criar horário”. O teste existente verifica URL de equipe após login e, depois, conteúdo da gestão. Não testa criação de horário ou cancelamento: apenas acesso e elementos.

### Cenário 3 — página inicial pública

**Arquivo:** acesso.cy.js. **Novo pacote.**

Visitar `/`. Verificar “FilaZero” visível e primeiro link `a[href="/entrar"]` visível. O seletor usa o destino do link, e `first()` escolhe o primeiro quando há mais de um.

Esperado: página e acesso ao login disponíveis sem autenticação. Não comprova todos os links, responsividade ou acessibilidade completa.

### Cenário 4 — credenciais inexistentes não autenticam

**Arquivo:** acesso.cy.js. **Novo pacote.**

Abrir login, preencher `nao-cadastrado@example.test` e uma senha de teste, enviar. Conferir que permanece em `/entrar` e mostra “Não foi possível entrar.” Depois tentar `/gestao` e conferir retorno ao login.

Esperado: conta inexistente não gera sessão autenticada. O cenário usa uma conta que não deve existir na massa, evitando acumular erros na conta real da recepção. Ele não verifica especificamente o bloqueio após cinco senhas erradas de uma conta existente.

### Cenário 5 — visitante não acessa gestão

**Arquivo:** acesso.cy.js. **Novo pacote.**

Sem login, visitar `/gestao`. Esperado: redirecionamento para `/entrar` e mensagem “Entre na sua conta para continuar.” O isolamento padrão de testes Cypress ajuda cada cenário a começar sem a sessão do anterior; não desabilitá-lo sem preparar outra estratégia.

Esse cenário é diferente do quarto: o quarto testa a recusa do formulário e ausência de autenticação após credenciais inválidas; o quinto testa diretamente uma rota protegida como visitante.

### Exemplo de código e leitura

```javascript
it('exige autenticacao para abrir a gestao', () => {
  cy.visit('/gestao');
  cy.url().should('include', '/entrar');
  cy.contains('Entre na sua conta para continuar.')
    .should('be.visible');
});
```

O nome explica a regra. visit é a ação, e should define as verificações. Se a gestão abrir sem login, o teste precisa falhar. Um teste sem asserções úteis pode executar cliques sem comprovar o requisito.

### Como explicar a contribuição

Depois de aplicar e executar: “Ampliei a automação de dois para cinco cenários, acrescentando página pública, recusa de credenciais inexistentes e proteção de acesso à gestão. Usei asserções para verificar URL e conteúdo.” Mostrar os três novos testes no próprio diff; não dizer que criou os dois originais se não os alterou.

**Estudar:** baseUrl, seletor, ação, asserção, estado de sessão, falha de ambiente vs. aplicação. Esses cinco cenários são um recorte de acesso; não comprovam reserva concorrente, capacidade, fila completa nem todos os requisitos. A execução é detalhada na seção 10.

## 8. Miguel — segurança e regressão em três cenários

**Pacote:** `contribuicoes/miguel/`. **Branch:** `miguel/regressao-seguranca`.

**Arquivo:** `tests/test_protecao_sessao.py`. Não exige navegador: usa pytest, cliente Flask e banco temporário, reutilizando a preparação do arquivo test_app.py.

### Cenário 1 — POST sem token não altera fila

Cadastrar e autenticar um cidadão. Enviar POST para `/fila/entrar` sem csrf_token. Esperado: HTTP 400 e zero entradas em queue_entries. A segunda verificação importa: não basta exibir erro se o dado já tiver sido gravado.

CSRF é uma proteção contra requisições indevidas usando a sessão do navegador; não é substituto de autenticação, autorização ou defesa contra todos os ataques. O token precisa ser conferido pelo servidor.

### Cenário 2 — expiração por inatividade

Autenticar e ajustar last_seen da sessão de teste para dezesseis minutos atrás. Solicitar `/painel` seguindo redirecionamentos. Esperado: login, aviso de expiração e ausência de user_id na sessão.

O teste simula o tempo no estado da sessão para não aguardar dezesseis minutos reais. Isso verifica o caminho do timeout no servidor, não é uma medição cronometrada de inatividade em todos os navegadores. Guardar essa distinção ao explicar.

### Cenário 3 — reserva de outro cidadão não pode ser cancelada

A reserva um horário. B, em outro cliente/sessão, envia tentativa de cancelamento usando o ID da reserva de A e o próprio token válido. Esperado: reserva de A continua booked.

O token válido não dá a B propriedade do registro. A autorização precisa conferir o vínculo da reserva com o usuário autenticado. Verificar o banco prova que o estado foi preservado; o cenário não prova registro de auditoria da tentativa.

```bat
python -m pytest -q tests/test_protecao_sessao.py
```

### Como explicar

Após verificar: “Acrescentei regressões de segurança para conferir recusa sem CSRF, encerramento de sessão inativa e preservação de reserva alheia.” Mostrar uma asserção de status e outra de estado. Estudar a diferença entre autenticar (quem é) e autorizar (o que pode fazer).

## 9. Filipe — pipeline e cobertura

**Pacote:** `contribuicoes/filipe/`. **Branch:** `filipe/cobertura-ci`.

**Arquivos:** `.github/workflows/quality.yml` e `docs/metricas/COMO-MEDIR.md`.

O workflow é configuração executada no GitHub Actions, não código Flask. `on: push` e `pull_request` definem os eventos. O job usa Ubuntu, obtém o repositório com checkout, prepara Python 3.11 e instala requirements-dev.txt. O pacote troca execução pytest simples por execução com coverage e publica um arquivo XML.

```text
coverage run --source=app -m pytest -q
coverage report -m
coverage xml -o coverage.xml
```

A primeira linha executa a suíte e mede o módulo Python app. A segunda apresenta resumo e linhas não cobertas. A terceira gera XML. `actions/upload-artifact@v4` disponibiliza `coverage.xml` como artefato `cobertura-python` na execução do job. Não confundir esse artefato com arquivo-fonte adicionado ao Git; o arquivo gerado fica fora do versionamento pelo .gitignore.

### O que verificar no GitHub

Após integrar o PR: abrir Actions → Quality checks → execução do commit. Conferir cada etapa e o resultado; localizar o artefato na página da execução, com login se necessário. Se os testes falharem, as etapas seguintes podem não executar; ausência do artefato não deve ser apresentada como sucesso. Não foi acrescentado limite mínimo obrigatório de cobertura por esse pacote.

### Métricas sem confusão

- Cobertura: quanto do código Python foi exercitado, no recorte declarado.
- Aprovação: testes aprovados divididos pelos executados; não executados apresentados à parte.
- Taxa de correção: defeitos distintos corrigidos e retestados divididos pelos registrados no mesmo conjunto.
- Densidade: defeitos distintos por quantidade de casos de uso analisados, com recorte explícito.

O baseline anterior da base foi 61% de instruções de app.py. Não reutilizar esse percentual como resultado depois das mudanças: medir a versão apresentada. Cobertura alta não garante ausência de defeitos. Este workflow proposto não inclui a execução Cypress: esse é um avanço separado.

### Como explicar

Após validar a execução: “Ajustei o pipeline para medir cobertura durante os testes e guardar um relatório consultável. Separei cobertura de código e aprovação dos cenários.” Estudar o que é job, step, evento, log e artefato; saber abrir a execução correspondente ao commit exibido.

## 10. Guia completo do Cypress para a demonstração

### É necessário?

Sim, para a entrega final: o edital solicita automação e o professor autorizou Cypress. O grupo precisa demonstrar execução e entender os resultados. Não basta mostrar um arquivo com cinco blocos it. Na segunda entrega, o foco documental é distinto; aqui o objetivo é preparar a demonstração final.

### 10.1 Preparar o computador

Instalar Python 3.10 ou superior, Node.js LTS (inclui npm) e Git. No CMD:

```bat
python --version
node --version
npm --version
git --version
```

Cada comando deve mostrar uma versão. Se não for reconhecido, conferir instalação/PATH e reabrir o terminal. Instalar dependências com internet antes da aula. Recursos de interface são locais, mas a instalação precisa de acesso aos servidores de pacotes.

### 10.2 Conferir os cinco cenários disponíveis

Depois da aplicação do pacote de Guilherme e integração, conferir em `cypress/e2e/`:

```text
filazero.cy.js   → 2 testes de recepção e gestor
acesso.cy.js     → 3 testes de página e proteção
```

No GitHub, a branch do Guilherme mostra a mudança antes da integração; main só depois. Se aparece apenas o primeiro arquivo, ainda não há cinco cenários aplicados nessa cópia. Se há cópias antigas adicionais, conferir para não contar duplicações como testes novos. Não modificar nomes/arquivos só para atingir a quantidade.

### 10.3 Primeiro terminal — iniciar o site

Abrir a pasta A3FILAZERO no Explorador, clicar na barra de endereço, digitar cmd e Enter. Estar na pasta que contém app.py e package.json. Na primeira configuração:

```bat
python -m venv .venv
.venv\Scripts\activate.bat
python -m pip install -r requirements-dev.txt
python app.py
```

Em execuções seguintes, reutilizar a venv e iniciar o app. Manter esse terminal aberto. Visitar `http://127.0.0.1:5000` no navegador e confirmar que o site responde. O aviso de servidor de desenvolvimento é esperado para essa demonstração local. Não digitar comandos npm nesse terminal enquanto Flask está ocupando o processo.

### 10.4 Segundo terminal — instalar Cypress

Abrir outro CMD na mesma raiz A3FILAZERO. Executar:

```bat
npm install
npx cypress verify
```

npm install instala a dependência declarada e normalmente baixa o aplicativo Cypress. Se informar que o executável não está instalado, executar:

```bat
npx cypress install
npx cypress verify
```

Verify verifica a instalação do programa, não testa o FilaZero. “Unzipping Cypress” é extração. Se ficar parado por muito tempo, conferir atividade CPU/disco e a mensagem exata; não apagar o projeto. Interromper com Ctrl+C somente se precisar tentar novamente; manter o terminal Flask separado. Não é necessário atualizar npm só por uma notificação de versão disponível.

### 10.5 Abrir a execução visual

```bat
npm run cy:open
```

No Cypress, escolher E2E Testing, um navegador disponível e iniciar. Na lista de specs, abrir `filazero.cy.js`, acompanhar os dois casos e salvar evidência. Voltar à lista de specs, abrir `acesso.cy.js`, acompanhar os três. A interface visual normalmente mostra um spec de cada vez; isso não significa que os outros testes desapareceram.

Verde indica aprovação do cenário executado; vermelho indica falha a investigar. Na coluna de comandos, selecionar passos para entender o que foi executado e onde a asserção falhou. O navegador mostra as ações do teste; não interferir clicando enquanto ele está executando.

### 10.6 Executar os dois arquivos pelo terminal

Para reunir os cinco casos em uma execução, sair/fechar a interface visual e, no segundo CMD, executar:

```bat
npm run cy:run
```

O script executa os specs conforme specPattern. A saída final deve listar os dois arquivos e, se os cinco passarem, cinco testes aprovados e zero falhos. Esse é o resultado esperado, não uma execução já comprovada. Se algo falhar, guardar a falha e investigar. O servidor Flask precisa continuar aberto no outro CMD.

### 10.7 Massa e isolamento

As contas de recepção e gestor do pacote são demonstrativas. O cenário inválido usa e-mail inexistente e pressupõe que ninguém o cadastrou. Se a equipe alterou senhas, removeu contas ou mudou títulos, revisar os testes e documentar a decisão. Não desabilitar verificação de autenticação só para obter verde.

O banco da demonstração é diferente do banco temporário de cada teste pytest. Cypress usa o servidor iniciado e seus dados reais de demonstração. Não executar contra uma UBS nem com dados pessoais reais. Se precisar reiniciar dados, usar exclusivamente uma cópia de demonstração conhecida, parar o servidor e preservar o que precisar antes de recriar o banco; não apagar banco de outro integrante sem combinar.

### 10.8 Evidências para guardar

1. Commit e branch usados na execução: `git rev-parse HEAD` e `git branch --show-current`.
2. Versões: Python, Node e Cypress (`npx cypress version`).
3. Print dos dois specs/resultados na execução visual, ou resumo terminal com os cinco.
4. Nome dos casos, resultado, data, ambiente e defeito, quando houver.
5. Opcional: gravar uma demonstração curta, identificando a versão e a data.

A configuração está com vídeo desativado. Não prometer que será criado vídeo automaticamente. Capturas de falha, quando geradas, ajudam a investigação; prints da execução bem-sucedida podem ser capturados manualmente. Evitar expor senhas e dados pessoais nas evidências.

### 10.9 Roteiro de 4 a 6 minutos para o professor

1. Abrir package.json e explicar cy:open/cy:run e dependência Cypress.
2. Abrir cypress.config.js e mostrar baseUrl, padrão dos specs e configuração de vídeo.
3. Abrir um teste de cada arquivo; identificar preparação/ação e asserção. Informar que havia dois casos e foram acrescentados três.
4. Com Flask iniciado, executar um spec visual para mostrar interação. Depois mostrar resultado real dos dois specs; se tempo permitir, executar os cinco por cy:run.
5. Explicar o que os cinco cenários comprovam e quais regras ainda não cobrem.
6. Mostrar commit/PR do Guilherme e o diff dos três cenários novos.

Não começar uma instalação pesada durante a apresentação. Se o ambiente falhar, mostrar evidências anteriores identificadas como tal, sem afirmar que foram produzidas ao vivo. Se o professor perguntar sobre fila/reserva, explicar que esses cinco casos focam acesso e que há regressões Python e tarefas adicionais para outros fluxos.

### 10.10 Falhas comuns

| Sintoma | O que conferir |
|---|---|
| npm não reconhecido | Node/PATH; reabrir terminal |
| package.json não encontrado | CMD na pasta errada; ir à raiz A3FILAZERO |
| Executável Cypress ausente | npx cypress install e depois verify |
| ECONNREFUSED / site indisponível | Flask ativo e porta 5000; abrir site manualmente |
| Apenas dois testes | acesso.cy.js ainda não aplicado/atualizado; conferir branch |
| Credenciais não autenticam | Contas/seed/senhas e bloqueio; não mudar asserção para ignorar erro |
| Texto não localizado | Conferir página, seletor e se houve alteração legítima na interface |
| Cypress passa, mas há falha na reserva | Os cinco casos não cobrem toda a reserva; ampliar testes |

## 11. Como apresentar o próprio versionamento

O procedimento operacional está em [CONTRIBUTING](../CONTRIBUTING.md) e nos [roteiros individuais](../contribuicoes/README.md). Para a apresentação, mostrar o diff, explicar a regra, a alteração, o teste e o resultado. Os commits da importação são a base compartilhada; cada integrante demonstra sua contribuição posterior.

Git registra alterações locais; push envia ao GitHub; PR propõe integração; revisão confere a mudança; merge integra. Branch de trabalho e main podem conter versões diferentes. A aprovação dos testes de uma branch não substitui a verificação da versão integrada.

## 12. Perguntas prováveis e ensaio da equipe

**O Cypress criou o site?** Não. Ele testa o site no navegador. Flask executa o servidor.

**O que comprova um teste?** A ação mais as asserções e o resultado, no cenário, versão e ambiente executados. O nome do teste sozinho não prova nada.

**Por que também há pytest?** Permite verificar lógica, rotas e banco com preparação controlada; Cypress verifica interação no navegador. As ferramentas se complementam.

**Por que 16 testes Python aprovados não significam 16 casos Cypress?** São suítes, níveis e cenários diferentes. O resultado não deve ser somado como se fosse uma única medida de cobertura.

**Cobertura de 100% significa zero defeitos?** Não. Cobertura indica execução de código segundo uma métrica; pode faltar uma asserção ou uma situação importante.

**O sistema está pronto para UBS real?** É protótipo acadêmico. Integrações oficiais, proteção/gestão de dados, disponibilidade, desempenho e avaliação de acessibilidade não são garantidos pelos testes apresentados.

**Qual foi o papel de cada pessoa?** Mostrar a contribuição real aplicada, seu diff, revisão e evidência. A divisão dos pacotes é proposta de trabalho, não histórico anterior reconstruído.

### Ensaiar com esta sequência

Alisson apresenta problema e orientação da interface; Cláudio explica presença e fluxo Flask; Arthur mostra capacidade e regressão; Guilherme demonstra Cypress; Miguel explica proteção e estado do banco; Filipe apresenta pipeline/métricas. Ajustar o tempo ao professor. Todos devem saber explicar um fluxo completo, não apenas decorar a fala individual.

### Checklist antes da aula

- Os pacotes apresentados foram aplicados e a versão está identificada.
- Cada integrante entende suas linhas alteradas e tem commit/PR real.
- Servidor inicia e contas de demonstração funcionam.
- Os dois arquivos Cypress aparecem e os cinco casos foram executados.
- Resultados falhos ou pendentes estão identificados; sem aprovação presumida.
- Há prints/logs e cópia de contingência, sem dados pessoais.
- A execução Actions e as métricas pertencem à versão apresentada.
- Cada pessoa sabe uma limitação do que está demonstrando.

## 13. Estado das verificações deste material

Na preparação dos seis pacotes aplicados em conjunto, passaram 16 testes Python; Ruff e Bandit não apontaram ocorrências. A sintaxe do novo spec JavaScript foi conferida com Node. Esses são resultados da preparação, não da execução dos integrantes.

Cypress e a execução do workflow proposto não foram executados nessa preparação. Os cinco cenários e os resultados esperados acima são instruções para a equipe executar e documentar. A aplicação dos pacotes à main e os PRs precisam ser conferidos no repositório antes da apresentação. A correção de capacidade não resolve a nova reserva após cancelamento nem todas as demais lacunas de requisitos.
