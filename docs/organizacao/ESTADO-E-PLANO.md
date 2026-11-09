# FilaZero — Onde estamos e como seguir

Atualizado em 09/11/2026 (horário de Brasília). Plano de continuidade até a entrega final de 27/11/2026; não altera nem refaz o documento da segunda entrega. Datas intermediárias são metas propostas. Responsabilidades seguem o plano de organização enviado e precisam ser confirmadas pelo grupo.

## Etapa atual: protótipo implementado, em validação e preparação da entrega final

O código já existe. Agora a equipe precisa compreender a base, confirmar os testes, corrigir regras inconsistentes, registrar contribuições reais no GitHub e preparar evidências/métricas. Não há evidência suficiente para marcar automação E2E, GitHub ou apresentação como concluídos. O professor autorizou Cypress, conforme informado pela equipe.

## O que existe e o que falta

| Frente | Situação verificada | Próximo passo |
|---|---|---|
| Site | Flask, SQLite, templates, estilos e JavaScript; três perfis | Rodar em dois computadores e revisar os fluxos |
| Python | 8 testes aprovados nesta análise | Acrescentar regressões para as falhas não cobertas |
| Cobertura | 61% de instruções de app.py, por coverage com a suíte atual | Medir após correções; não confundir com cobertura E2E ou módulo de fila |
| Cypress | 2 casos no código dos ZIPs | Implementar e executar no mínimo 5 casos distintos |
| Defeitos de reserva | Código ainda contém os caminhos de DEF01/DEF02; reproduzidos na análise anterior | Equipe reproduz e corrige, com evidência antes/depois |
| Proximidade/presença/gestão | Lacunas apontadas por inspeção | Validar regras e corrigir ou alinhar escopo ao professor |
| Git | Dois ZIPs sem histórico Git; base organizada publicada no GitHub a pedido do titular | Convidar colegas e cada integrante enviar mudanças reais pela própria conta |
| Métricas e slides | Sem evidência final de consolidação | Gerar na versão integrada e ensaiar |

Não se conclui progresso apenas pelo nome de um arquivo ou pelo plano de tarefas. Instalação local relatada no chat não equivale a cinco testes Cypress aprovados. Nenhum percentual de conclusão geral foi estimado porque faltam confirmações da equipe.

## Base adotada e comparação dos ZIPs

Base: FilaZero-A3-Pacote-Completo.zip / FilaZero-A3/Projeto. A3.zip tem outro layout de interface e inclui .venv e instance/filazero.sqlite3. No backend comparado, o pacote completo acrescenta a conta cidadão de demonstração e tratamento de conflito no seed do usuário. Também contém componentes CSS, fonte local e arquivos de interface adicionais. A escolha é por esses recursos identificados, não por inferência de qual ZIP é cronologicamente mais recente. As versões não foram misturadas.

Foi preservado o código funcional da base, sem implementar as correções atribuídas aos integrantes. A pasta .venv e o banco local não foram incorporados. MANIFESTO-BASE.json registra SHA-256 dos arquivos importados. A decisão deve ser revista se o grupo tiver mudanças locais mais novas ainda não enviadas.

## Primeiras ações do grupo

1. Confirmar a distribuição dos seis nomes e aceitar convites do repositório https://github.com/alissonsousa-code/A3FILAZERO.
2. Usar o repositório A3FILAZERO já publicado; seguir o guia de Git atualizado.
3. Cada integrante clona, configura sua identidade e cria uma branch da sua tarefa.
4. Conferir instalação de Python, Node/npm e Cypress; registrar versões e manter o Flask aberto.
5. Reproduzir as falhas prioritárias e revisar a especificação para entender o comportamento esperado.
6. Trabalhar nas tarefas do QUADRO-EQUIPE.csv, atualizar status e vincular evidências.
7. Revisar PRs e integrar um de cada vez, sobretudo os que alteram app.py.

## Regras de colaboração

Status do quadro: A fazer → Em andamento → Em revisão → Concluído; usar Bloqueado com causa anotada. As tarefas começam A fazer por falta de confirmação de execução pela equipe. Uma tarefa de executar testes pode ser concluída com falhas se estas estiverem registradas; corrigir é outra tarefa. Não marcar correção concluída sem reteste.

Atualização diária curta: tarefa, o que mudou, evidência e impedimento. Revisão cruzada obrigatória antes de integrar: pessoa diferente do autor. Não sobrescrever o projeto inteiro com outra versão ZIP. Não editar app.py simultaneamente sem combinar seções e atualizar main. A sequência F06 → F07 → F08 → F09 → F11 serializa mudanças nesse arquivo.

O Git guarda snapshots de arquivos e diferenças; os membros não precisam subir pedaços soltos da aplicação. app.py já pertence à base: cada pessoa faz commit apenas da diferença correspondente à sua tarefa. Compartilhar arquivo não impede commits de autores diferentes em momentos distintos.

## Resultado mínimo antes de apresentar

Cypress escolhido e autorizado; pelo menos cinco casos automatizados distintos executados; protótipo que inicia conforme README; histórico GitHub com ao menos dois integrantes reais e prints (meta do grupo: os seis); métricas com método e versão; slides e demonstração. Cumprir orientações do template e do professor. Funcionalidades pendentes devem ser explicadas, sem afirmar produção ou conformidade completa com LGPD.

## Métricas e limites

Cobertura de instruções Python: instruções executadas ÷ instruções mensuráveis, na versão e recorte do coverage. A linha de base atual foi 567 instruções mensuráveis, 221 não executadas e 61% exibido. A meta original de 70% no módulo de fila ainda não é comprovada por esse número global.

Aprovação de testes: aprovados ÷ executados × 100, apresentando não executados à parte. Taxa de correção: defeitos corrigidos e retestados ÷ defeitos encontrados × 100 no mesmo conjunto. Densidade: defeitos distintos ÷ casos de uso analisados, declarando recorte e critério de contagem. Não somar defeitos repetidos por cenário como se fossem problemas diferentes.

Cypress não substitui teste de carga com 200 usuários, avaliação com participantes 60+ ou garantia de disponibilidade. Medições de desempenho e acessibilidade exigem seus próprios procedimentos. A presença do workflow não comprova que ele executou no GitHub; o atual ainda não roda Cypress.

## Alisson Sousa Santos

Papel: Coordenação e rastreabilidade. Revisor principal: Cláudio.

Arquivos/seções: docs/organizacao/, README.md, docs/escopo-final.md.

Contribuição esperada: Conferir o plano com a equipe, fechar escopo das funções pendentes e documentar decisões; atualizar instruções com o que realmente foi executado.

Branch sugerida: `alisson/escopo-final`. Commit sugerido depois de executar a mudança: `docs: revisar escopo final e mapa de requisitos`. A responsabilidade é de continuidade e revisão; não atribui autoria da base recebida.

## Cláudio Roberto Cruz Santiago Santos

Papel: Backend, ambiente e perfis. Revisor principal: Arthur.

Arquivos/seções: app.py: create_app, login, roles_required, call_next, notify; requirements*.txt; README.md.

Contribuição esperada: Documentar ambiente reproduzível e ajustar chamada/presença e avisos de proximidade em tarefas separadas, com testes correspondentes.

Branch sugerida: `claudio/presenca-chamada`. Commit sugerido depois de executar a mudança: `fix: exigir presenca na chamada de paciente`. A responsabilidade é de continuidade e revisão; não atribui autoria da base recebida.

## Arthur Cordeiro de Carvalho Cruz

Papel: Reservas e integridade. Revisor principal: Cláudio.

Arquivos/seções: app.py: init_db, appointments, book_slot, cancel_appointment, checkin_appointment, block_slot; templates/appointments.html; tests/test_reservas.py.

Contribuição esperada: Corrigir capacidade após check-in e nova reserva após cancelamento, preservando histórico e compatibilidade com banco existente.

Branch sugerida: `arthur/capacidade-checkin`. Commit sugerido depois de executar a mudança: `fix: manter capacidade ocupada apos check-in`. A responsabilidade é de continuidade e revisão; não atribui autoria da base recebida.

## Guilherme Cabral Teixeira

Papel: Cypress e integração contínua. Revisor principal: Miguel.

Arquivos/seções: cypress/e2e/, cypress.config.js, package.json, package-lock.json; .github/workflows/quality.yml.

Contribuição esperada: Adicionar ao menos três casos aos dois existentes, executar os cinco, estabilizar massa e automatizar execução no pipeline se possível.

Branch sugerida: `guilherme/cypress-cenarios`. Commit sugerido depois de executar a mudança: `test: adicionar cenarios E2E de acesso e autenticacao`. A responsabilidade é de continuidade e revisão; não atribui autoria da base recebida.

## Miguel Lima Quadros Gomes

Papel: Validação e regressão. Revisor principal: Guilherme.

Arquivos/seções: tests/test_seguranca.py, tests/test_fila.py; evidencias/regressao/; docs/validacao/.

Contribuição esperada: Criar verificações de permissões/fila, revisar os testes de reserva de Arthur e registrar execuções com versão e dados fictícios.

Branch sugerida: `miguel/regressao-fila`. Commit sugerido depois de executar a mudança: `test: verificar permissoes e transicoes da fila`. A responsabilidade é de continuidade e revisão; não atribui autoria da base recebida.

## Filipe Albuquerque Oliveira

Papel: Revisão, métricas e apresentação. Revisor principal: Alisson.

Arquivos/seções: CODE_REVIEW_CHECKLIST.md; docs/metricas/; docs/revisoes/; apresentacao/.

Contribuição esperada: Revisar mudanças com checklist, calcular métricas com recorte declarado e consolidar evidências e slides finais.

Branch sugerida: `filipe/metricas`. Commit sugerido depois de executar a mudança: `docs: registrar metricas e evidencias de qualidade`. A responsabilidade é de continuidade e revisão; não atribui autoria da base recebida.

## Plano da apresentação final

Alisson explica problema e escopo; Cláudio mostra a ligação formulário → Flask → SQLite e permissões; Arthur mostra uma regra e a correção/reteste; Guilherme executa Cypress e explica comandos/asserções; Miguel mostra como resultados se vinculam a requisitos e riscos; Filipe apresenta revisão, métricas e limites. Ajustar ao tempo informado pelo professor. Cada pessoa deve mostrar a diferença real do próprio commit e entender um fluxo completo, além de sua fala.
