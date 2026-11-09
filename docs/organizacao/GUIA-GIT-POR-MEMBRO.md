# Git e GitHub — passo a passo da equipe

## Repositório publicado

https://github.com/alissonsousa-code/A3FILAZERO

A base e os guias foram importados com apoio de IA a pedido do titular em 09/11/2026. A autoria exibida pelo GitHub na publicação não demonstra quem implementou cada parte do código recebido. Não atribuir esses commits aos seis membros como contribuições individuais. O histórico começa na importação atual.

## Antes de trabalhar

Alisson convida os cinco colegas em Settings → Collaborators → Add people. Cada pessoa aceita com sua própria conta. Instalar Git para Windows em https://git-scm.com/downloads/win, reabrir CMD e conferir git --version. Clonar uma única vez:

```bat
git clone https://github.com/alissonsousa-code/A3FILAZERO.git
cd A3FILAZERO
```

Depois configurar a identidade abaixo e seguir o fluxo por branch. Não é necessário baixar bundle ou criar novo repositório. Quem já tiver um clone atualizado não clona novamente dentro dele. Se privado no futuro, dar acesso ao professor e aos membros.

## Cada integrante: configurar sua própria identidade

Cada membro abre CMD no clone e substitui os exemplos pelo SEU nome e e-mail verificado da conta GitHub (ou e-mail noreply disponibilizado pelo próprio GitHub).

```bat
git config user.name "SEU NOME COMPLETO"
git config user.email "SEU EMAIL DO GITHUB"
git config --get user.name
git config --get user.email
```

Essas configurações valem só neste repositório. E-mail de autoria e conta usada para autenticar/push são coisas diferentes; confira ambos. Ninguém configura a identidade de outra pessoa para simular contribuição. Documentação, testes, correções e revisão também são trabalho real, mas, como o professor enfatizou partes de código, cada membro deve combinar sua contribuição efetiva e não usar commits de README como substituição automática de código.

## Rotina de um commit real

Caso ainda não tenha clonado, usar a URL do grupo. Não clonar novamente se já estiver no clone. Exemplo:

```bat
git clone https://github.com/alissonsousa-code/A3FILAZERO.git
cd A3FILAZERO
```

No clone, configurar identidade e iniciar tarefa:

```bat
git switch main
git pull --ff-only origin main
git switch -c arthur/capacidade-checkin
```

O nome da branch acima é exemplo de Arthur; os demais usam suas branches do plano. Implementar/revisar a tarefa e executar os testes relacionados antes do commit. Depois conferir:

```bat
git status
git diff
```

Adicionar só os arquivos da tarefa, por exemplo, para a correção de reservas:

```bat
git add app.py tests/test_reservas.py
git diff --cached
git commit -m "fix: manter capacidade ocupada apos check-in"
git push -u origin arthur/capacidade-checkin
```

O arquivo tests/test_reservas.py é planejado: precisa ser criado e validado por quem faz a tarefa; o comando falha se ainda não existir. Não execute comandos de arquivos planejados sem produzi-los. Se app.py tiver mudanças de mais de uma tarefa, usar git add -p app.py para selecionar trechos ou separar as alterações antes de preparar o commit.

No GitHub, abrir Pull Request da branch para main, indicar tarefa, motivo, mudança, testes e resultado. Pedir revisão. Integrar PRs um de cada vez; manter commits de autores reais visíveis. Preferir merge normal no trabalho da equipe quando houver vários autores no PR. Após integrar, atualizar main antes de iniciar a próxima tarefa.

Se git pull --ff-only falhar ou aparecer conflito, parar e conferir o estado com git status; combinar com o responsável pelo arquivo. Não usar reset --hard ou force como tentativa genérica de resolver. Se já houver mudanças locais, salvá-las em branch/commit de trabalho antes de trocar de tarefa.

## Quem sobe o quê

Os arquivos originais já estão na importação. Os membros sobem mudanças próprias ou revisões reais verificadas, não cópias idênticas da base para preencher histórico. Reenviar o mesmo arquivo não gera novo commit quando o conteúdo não muda. Os exemplos de mensagens são sugestões para depois do trabalho, não comprovantes de trabalho realizado. A divisão por arquivo/seção aparece no plano e nos roteiros individuais. Cláudio e Arthur compartilham app.py: respeitar a ordem do quadro e atualizar main entre PRs.

## Provas para o professor

Guardar prints da página de commits e de cada PR, autoria, alteração e execução dos testes. Todos devem saber abrir o diff do seu commit e explicar o que alterou e por quê. Conferir localmente:

```bat
git log --format="%h %an <%ae> %s"
git shortlog -sne HEAD
```

O edital exige pelo menos dois integrantes com contribuições reais; o plano propõe envolver os seis. Não recriar datas, nomes, commits vazios ou autoria que não ocorreu. O Git registra o trabalho a partir da importação atual e da continuidade da equipe.

## O que não subir

.venv/, node_modules/, __pycache__/, banco instance/, .env, credenciais, caches e arquivos enormes de instalação. Subir requirements e package.json; package-lock.json deve ser criado pelo npm e versionado pelo responsável quando houver instalação. Guardar só evidências selecionadas, sem dados pessoais. Não habilitar upload indiscriminado da pasta A3.zip com o ambiente instalado.
