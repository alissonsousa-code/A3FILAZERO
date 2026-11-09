# Como contribuir

## Preparar uma vez

Aceitar o convite de colaborador, instalar Git e clonar o projeto. Usar CMD no Windows:

```bat
git clone https://github.com/alissonsousa-code/A3FILAZERO.git
cd A3FILAZERO
git config user.name "SEU NOME COMPLETO"
git config user.email "SEU EMAIL VERIFICADO NO GITHUB"
python -m venv .venv
.venv\Scripts\activate.bat
python -m pip install -r requirements-dev.txt
```

Quem já tem clone usa a pasta existente. Identidade do commit e autenticação no push devem ser da própria pessoa. Não compartilhar senha/token. Conferir `git status` antes de trocar de branch; preservar alterações locais existentes.

## Realizar uma tarefa

1. Atualizar main com `git switch main` e `git pull --ff-only origin main`.
2. Seguir [o roteiro da sua parte](contribuicoes/README.md): branch, patch, arquivos e teste.
3. Se `git apply --check` falhar, conferir se a alteração já entrou ou se a base mudou. Não forçar nem substituir app.py inteiro.
4. Ler o diff e executar as verificações indicadas. Registrar versão, cenário, resultado real e evidência.
5. Preparar só os arquivos da tarefa, conferir `git diff --cached`, fazer commit e push na branch.
6. Abrir PR para main e pedir revisão a colega diferente do autor. Conferir testes e conflitos antes do merge.
7. Após integrar, atualizar main e verificar o comportamento na versão integrada. Integrar PRs de app.py um por vez.

## Evidências e revisão

Usar o [checklist técnico](CODE_REVIEW_CHECKLIST.md). Guardar comando/resultado, commit e PR. As evidências podem ser anexadas à conversa do PR, sem dados pessoais, senhas ou tokens. Não presumir aprovação de cenário não executado. Pacotes preparados precisam de revisão e teste pelo responsável.

Não versionar .venv, node_modules, banco local, caches ou credenciais. Versionar código, dependências declaradas, configurações e registros selecionados. Um commit deve representar mudança real; reenviar conteúdo idêntico não cria uma contribuição nova.
