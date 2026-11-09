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

## Continuidade

O repositório está publicado. Cada pessoa segue [CONTRIBUTING](../../CONTRIBUTING.md) e [sua tarefa](../../contribuicoes/README.md). Atualizar status e evidência no quadro; tarefas sem confirmação não são marcadas concluídas.

Alisson aplicou a contribuição de mensagens, confirmou dois testes específicos e dez na suíte local, conferiu 404/403 e enviou commit f03ba61 com evidências no PR #1. Na conferência em 09/11/2026, o PR permanecia aberto, com revisão solicitada a Filipe. Não marcar merge ou testes da main integrada como concluídos antes de ocorrerem.

Os demais responsáveis mantêm as atividades do quadro. Integrar mudanças em app.py uma de cada vez. A revisão e o reteste são parte do critério de conclusão.

## Resultado mínimo antes de apresentar

Cypress escolhido e autorizado; pelo menos cinco casos automatizados distintos executados; protótipo que inicia conforme README; histórico GitHub com ao menos dois integrantes reais e prints (meta do grupo: os seis); métricas com método e versão; slides e demonstração. Cumprir orientações do template e do professor. Funcionalidades pendentes devem ser explicadas, sem afirmar produção ou conformidade completa com LGPD.

## Métricas e limites

Cobertura de instruções Python: instruções executadas ÷ instruções mensuráveis, na versão e recorte do coverage. A linha de base atual foi 567 instruções mensuráveis, 221 não executadas e 61% exibido. A meta original de 70% no módulo de fila ainda não é comprovada por esse número global.

Aprovação de testes: aprovados ÷ executados × 100, apresentando não executados à parte. Taxa de correção: defeitos corrigidos e retestados ÷ defeitos encontrados × 100 no mesmo conjunto. Densidade: defeitos distintos ÷ casos de uso analisados, declarando recorte e critério de contagem. Não somar defeitos repetidos por cenário como se fossem problemas diferentes.

Cypress não substitui teste de carga com 200 usuários, avaliação com participantes 60+ ou garantia de disponibilidade. Medições de desempenho e acessibilidade exigem seus próprios procedimentos. A presença do workflow não comprova que ele executou no GitHub; o atual ainda não roda Cypress.

## Responsabilidades

| Integrante | Frente |
|---|---|
| Alisson | Coordenação, escopo e mensagens de erro |
| Cláudio | Ambiente, backend e presença |
| Arthur | Reservas e integridade |
| Guilherme | Automação Cypress |
| Miguel | Regressão e segurança |
| Filipe | Revisão, métricas e apresentação |

Arquivos, branches e verificações estão nos [roteiros individuais](../../contribuicoes/README.md); prazos e critérios estão no [quadro](QUADRO-EQUIPE.csv).

## Plano da apresentação final

Alisson explica problema e escopo; Cláudio mostra a ligação formulário → Flask → SQLite e permissões; Arthur mostra uma regra e a correção/reteste; Guilherme executa Cypress e explica comandos/asserções; Miguel mostra como resultados se vinculam a requisitos e riscos; Filipe apresenta revisão, métricas e limites. Ajustar ao tempo informado pelo professor. Cada pessoa deve mostrar a diferença real do próprio commit e entender um fluxo completo, além de sua fala.
