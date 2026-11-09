# Plano de qualidade e verificação do código — FilaZero

## 1. Objetivo

Verificar se o software atende aos requisitos funcionais e não funcionais definidos na 1ª entrega, com foco nos atributos priorizados: segurança, confiabilidade, usabilidade, eficiência, portabilidade e manutenibilidade.

## 2. Metodologias e técnicas

| Prática | Como será aplicada | Evidência / ferramenta |
|---|---|---|
| Revisão por pares (Code Review) | Pull Request revisado por integrante que não implementou a alteração; checklist obrigatório. | GitHub/GitLab e `CODE_REVIEW_CHECKLIST.md` |
| Análise estática | Identificar estilo inconsistente, imports não usados, erros comuns e padrões de risco sem executar o programa. | Ruff e Bandit |
| Teste unitário | Testar isoladamente CPF, cálculo da posição, prioridade, tolerância, validação e regras de reserva. | pytest; técnica caixa-branca; cobertura por cobertura.py |
| Teste de integração | Verificar interação entre rotas, banco SQLite, autenticação, fila, agendamento e notificações internas. | pytest + Flask test client + banco temporário |
| Teste de sistema / E2E | Executar fluxos completos no navegador, simulando cidadão, recepção e gestor. | Cypress; técnica caixa-preta |
| Teste de aceitação | Validar cenários Dado/Quando/Então associados aos CA01–CA15, com roteiro de usuário. | Checklist de aceitação e registro de evidências |
| Teste baseado em risco | Priorizar concorrência de vagas, perda de posição, acesso indevido e erro na ordem prioritária. | Matriz de risco R01–R07 da 1ª entrega |
| Segurança | Verificar bloqueio de login, expiração de sessão, CSRF, autorização por perfil e acesso a dados alheios. | pytest, Bandit e checklist manual |
| Desempenho | Simular carga até 200 usuários e medir p95 dos fluxos principais. | k6 ou Locust; ambiente controlado |
| Usabilidade/acessibilidade | Testar contraste AA, teclado, labels, tamanho da fonte/botões e tarefas com participantes 60+. | Lighthouse, axe DevTools e roteiro manual |
| Regressão | Reexecutar os testes automatizados sempre que uma funcionalidade existente for alterada. | pytest + Cypress no pipeline |

## 3. Critérios quantitativos de saída

- 100% dos casos críticos executados e aprovados.
- Pelo menos 90% dos casos de teste executados com sucesso.
- Cobertura de testes de pelo menos 70% no módulo de fila.
- Nenhum defeito crítico em aberto.
- Operações concorrentes para a mesma vaga: exatamente uma reserva por vaga/capacidade disponível.
- Reconexão: estado recuperado em até 10 segundos, sem perda da posição.
- Atualização da posição: até 5 segundos.
- Desempenho de referência: p95 de até 2 segundos com 200 usuários simultâneos, a ser medido em ambiente de teste.

Os valores acima são metas de verificação do trabalho, não resultados já medidos. Resultados reais deverão ser anotados após a execução dos testes.

## 4. Fluxo de trabalho sugerido

1. Criar branch `feature/nome-da-funcionalidade`.
2. Relacionar a tarefa a RF/RNF/UC/CA.
3. Implementar e criar/atualizar testes.
4. Executar `pytest`, `ruff` e `bandit` localmente.
5. Abrir Pull Request com evidências e descrição da alteração.
6. Outro integrante revisar o código com o checklist.
7. Executar regressão E2E no Cypress.
8. Aprovar e integrar somente se os critérios forem atendidos; registrar defeitos restantes.

## 5. Rastreabilidade inicial de testes

| Requisito/risco | Cenário principal | Nível |
|---|---|---|
| RF01 / CA01 | Cadastro, CPF inválido/duplicado, consentimento e hash de senha | Unidade + Sistema |
| RF02 | Filtrar unidade por bairro ou nome; unidade sem resultado | Integração + Sistema |
| RF03/RF04 / CA02/CA03 | Entrar na fila, impedir fila duplicada e priorizar somente após confirmação | Unidade + Sistema + Aceitação |
| RF05 / CA06 / R01 | Duas sessões disputando a última vaga; uma confirmação por capacidade | Integração + Sistema |
| RF06 / CA04 / RNF11 | Atualizar posição em até 5 segundos após chamada | Sistema + Desempenho |
| RNF01 / CA05 / R02 | Perder e restabelecer conexão sem perder estado no servidor | Integração + Sistema |
| RF07 / CA07 / R06 | Criar aviso de proximidade/chamada e registrar notificação interna | Integração + Sistema |
| RF08/RF09 / CA08 | Recepção confirma presença, inicia e conclui atendimento | Sistema + Aceitação |
| RF10/RF11 / CA09/CA10 | Gestão altera disponibilidade e relatório confere com registros | Integração + Sistema |
| RNF05 / CA11 / R03 | Cidadão tenta acessar dado de outro cidadão ou área restrita | Segurança + Sistema |
| RNF06 / CA12 | Cinco falhas bloqueiam por 15 minutos; sessão expira por inatividade | Unidade + Sistema |
| RNF08/RNF09 / CA13 / R05 | Participantes 60+ completam tarefa; avaliar contraste e teclado | Aceitação + Usabilidade |
| RNF12 / CA14 / R07 | Carga simulada e medição do p95 | Desempenho |
| RNF15/RNF16 / CA15 | Navegadores atuais e largura a partir de 360 px | Sistema + Compatibilidade |

## 6. Limitações do protótipo atual

Notificação externa por SMS/e-mail, TLS de produção, criptografia de dados pessoais em repouso, geolocalização real, disponibilidade 99%, teste com 200 usuários e avaliação com pessoas 60+ exigem infraestrutura, integrações ou usuários externos e não são comprovados apenas pelo protótipo local. Devem ser apresentados como atividades planejadas/pendentes, nunca como testes aprovados.
