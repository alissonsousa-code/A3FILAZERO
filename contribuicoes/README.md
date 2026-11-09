# Contribuições da equipe

Os pacotes contêm mudanças propostas, ainda não aplicadas ao código da main. Cada responsável deve ler, aplicar, testar e enviar a mudança pela própria conta. As falas de apresentação descrevem a atividade somente depois de executada. Não é necessário alterar autoria ou reenviar a base original.

## Antes de começar

Alisson convida os cinco colegas em Settings → Collaborators. Cada um aceita, instala Git e clona o repositório. Configurar nome/e-mail próprios. Trabalhar em clone com alterações anteriores guardadas. Com o CMD na raiz do clone, seguir o guia individual.

| Integrante | Alteração proposta | Guia |
|---|---|---|
| Alisson | Mensagens de erro e testes de interface | [Abrir](./alisson/LEIA-MINHA-PARTE.md) |
| Cláudio | Chamada somente com presença confirmada | [Abrir](./claudio/LEIA-MINHA-PARTE.md) |
| Arthur | Capacidade ocupada após check-in | [Abrir](./arthur/LEIA-MINHA-PARTE.md) |
| Guilherme | Três novos casos Cypress; cinco com os existentes | [Abrir](./guilherme/LEIA-MINHA-PARTE.md) |
| Miguel | CSRF, sessão e reserva alheia | [Abrir](./miguel/LEIA-MINHA-PARTE.md) |
| Filipe | Cobertura Python no GitHub Actions | [Abrir](./filipe/LEIA-MINHA-PARTE.md) |

## Ordem e revisão

Os seis podem trabalhar em branches próprias. Integrar um PR por vez. Cláudio e Arthur mudam app.py em seções diferentes; atualizar main antes de aplicar cada pacote. Miguel, Alisson e Guilherme adicionam arquivos próprios. Filipe muda o workflow. Executar regressão após integrar.

## Situação dos testes da preparação

16 testes Python aprovados com os seis pacotes aplicados em conjunto; Ruff e Bandit sem apontamentos. JavaScript passou na checagem de sintaxe. Cypress e a execução GitHub Actions das mudanças propostas não foram executados nesta preparação. Não apresentar estes resultados como execução dos membros.

O código da main permanece como base até a integração dos PRs. Os pacotes não corrigem todos os defeitos: a nova reserva após cancelamento e os demais requisitos pendentes exigem tarefas adicionais do quadro.
