# FilaZero — Sistema web demonstrativo para filas e agendamentos em UBS

Projeto acadêmico da UC **Gestão e Qualidade de Software — UNIFACS**, elaborado a partir da especificação da 1ª entrega, com apoio de IA.

Organização: [LEIA-PRIMEIRO.md](LEIA-PRIMEIRO.md). Contribuições: [pacotes da equipe](contribuicoes/README.md).

## 1. O que está implementado

- Cadastro do cidadão com validação matemática do CPF, aceite de consentimento e senha armazenada como hash.
- Login por CPF ou e-mail, perfis de cidadão/recepção/gestor, bloqueio após cinco tentativas incorretas e expiração por inatividade.
- Consulta de unidades demonstrativas por bairro/nome.
- Entrada na fila virtual, bloqueio de segunda fila ativa, acompanhamento de posição e previsão de espera.
- Ordem de chamada por prioridade confirmada e, dentro do grupo, horário de entrada.
- Registro de presença, confirmação de prioridade, chamada do próximo, início/conclusão e marcação de ausência.
- Agendamento de consultas, vacinação e exames, confirmação por código, cancelamento e controle de capacidade com transação.
- Check-in de agendamento pela recepção na data marcada.
- Notificações internas no painel do cidadão. O envio real por SMS/e-mail ainda depende de integração externa.
- Gestão de horários, bloqueio de vagas sem reservas e abertura/encerramento da fila da unidade.
- Indicadores de fila/agendamento e exportação CSV.
- Interface responsiva, fonte-base de 16 px, navegação por teclado e elementos de toque com altura adequada.
- Log básico de auditoria para ações operacionais e administrativas.

## 2. Requisitos para executar

- Python 3.10 ou superior.
- Navegador atualizado.
- Acesso à internet durante a instalação das dependências. A interface usa recursos locais, incluindo a fonte Rawline.

## 3. Instalação no Windows

Abra o PowerShell na raiz do clone `A3FILAZERO` e execute:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

Acesse: http://127.0.0.1:5000

No Windows, caso a ativação do ambiente virtual seja bloqueada pela política do PowerShell, use o Prompt de Comando:

```bat
.venv\Scripts\activate.bat
```

## 4. Acessos de demonstração

| Perfil | Usuário | Senha |
|---|---|---|
| Recepção | `recepcao@filazero.local` | `Recepcao@123` |
| Gestor | `gestor@filazero.local` | `Gestor@123` |
| Cidadão | `cidadao@filazero.local` | `Cidadao@123` |

As contas de demonstração são criadas automaticamente quando o banco é inicializado. Você também pode criar uma conta de cidadão pela interface.

## 5. Roteiro rápido para demonstrar ao professor

1. Abra o site e use a conta de demonstração do cidadão ou crie uma conta com dados fictícios e um CPF de teste válido.
2. Entre como cidadão, abra **Unidades**, selecione um serviço e entre na fila.
3. Em outra janela/anônima, entre como recepção e abra **Painel da recepção**.
4. Busque o cidadão pelo nome ou CPF, registre a presença e confirme a prioridade somente se o cenário de teste exigir.
5. Clique em **Chamar próximo paciente**; volte à janela do cidadão e mostre a notificação e a atualização da posição.
6. Na recepção, inicie e conclua o atendimento.
7. Como cidadão, reserve um horário em **Agendamentos** e demonstre o cancelamento.
8. Como gestor, crie um horário, bloqueie um horário sem reservas, abra/encerre a fila e consulte **Relatórios**; exporte o CSV.

## 6. Testes e qualidade

Testes automatizados de unidade e integração:

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
coverage run -m pytest
coverage report -m
ruff check .
bandit -r app.py
```

Testes E2E com Cypress (requer Node.js):

```bash
npm install
npm run cy:run
```

Plano e critérios detalhados: `docs/PLANO_DE_QUALIDADE.md` e `CODE_REVIEW_CHECKLIST.md`.

## 7. Dados de demonstração e limitações importantes

- Nomes de unidades, endereços, vagas e horários são **fictícios**. Não representam a agenda nem a operação de UBS real.
- A previsão de espera usa uma regra inicial de 15 minutos por posição; deve ser calibrada com dados reais.
- Notificações aparecem no próprio site; não são enviados SMS, WhatsApp ou e-mails.
- A busca por localização é demonstrada por nome/bairro digitado; não há geolocalização de produção.
- O relatório é exportado em CSV. Exportação PDF pode ser adicionada em evolução futura.
- O sistema é um **protótipo acadêmico executável**, não está liberado para produção ou para tratar dados reais de saúde. Antes de produção são necessários HTTPS real, gestão segura de segredos, criptografia/gestão de chaves para dados pessoais, política de retenção e exclusão, adequação LGPD, revisão jurídica, backups, monitoramento, testes de invasão, disponibilidade, integração validada com a UBS e avaliação formal de acessibilidade.
- Para publicação, configure `FLASK_SECRET_KEY` com segredo forte e `COOKIE_SECURE=1` atrás de HTTPS. Remova ou altere as contas demonstrativas no trecho de seed de `app.py`, troque as senhas e conclua as medidas de produção antes de qualquer uso real.

## 8. Estrutura do projeto

```text
filazero_project/
├── app.py
├── requirements.txt
├── requirements-dev.txt
├── package.json
├── cypress.config.js
├── templates/                 # layout, páginas e componentes HTML/Jinja
├── static/css/                # base, componentes e estilos de página
├── static/fonts/              # Rawline e licença SIL Open Font License
├── static/icons.svg           # ícones compartilhados
├── static/js/app.js           # máscara CPF, confirmação e atualização da fila
├── tests/                     # testes pytest
├── cypress/e2e/               # testes ponta a ponta
├── docs/                      # plano de qualidade
└── CODE_REVIEW_CHECKLIST.md
```

## 9. Banco de dados

O SQLite é criado automaticamente em `instance/filazero.sqlite3` no primeiro acesso. Para reiniciar os dados demonstrativos, pare o servidor e apague esse arquivo; ele será recriado no próximo início.

## 10. Manutenção da interface

- `templates/base.html` define o cabeçalho, a navegação por perfil e o rodapé. `templates/index.html` reúne as seções da página inicial.
- `templates/ui.html` concentra os componentes Jinja reutilizados em formulários e painéis.
- `static/css/style.css` reúne as variáveis de cor, tipo, espaçamento e o layout compartilhado. `components.css` define botões, formulários, avisos e painéis. `pages.css` contém as composições específicas de cada tela.
- A tipografia Rawline é distribuída com a licença em `static/fonts/OFL.txt`. Os arquivos originais estão no [repositório Rawline](https://github.com/h-ibaldo/Raleway_Fixed_Numerals).
