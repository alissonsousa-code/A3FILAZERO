# Filipe — Cobertura Python no GitHub Actions

## Procedimento

Este pacote prepara a mudança. O responsável revisa, aplica e verifica antes de enviar. Cada commit deve usar o nome/e-mail do próprio membro e a conta autenticada correta.

Instalar Git para Windows. Clonar uma vez (quem já clonou entra na pasta existente):

```bat
git clone https://github.com/alissonsousa-code/A3FILAZERO.git
cd A3FILAZERO
```

Configurar seus dados reais:

```bat
git config user.name "SEU NOME COMPLETO"
git config user.email "SEU EMAIL DO GITHUB"
git status
```

Com a árvore de trabalho limpa, atualizar, criar branch e aplicar:

```bat
git switch main
git pull --ff-only origin main
git switch -c filipe/cobertura-ci
git apply --check contribuicoes/filipe/alteracoes.patch
git apply contribuicoes/filipe/alteracoes.patch
git diff
```

Se --check falhar, pare e confira com a equipe se a mudança já foi integrada ou se houve alteração no trecho; não force nem substitua app.py inteiro. Os patches de Cláudio e Arthur foram preparados para trechos diferentes e verificados em conjunto. Não reaplique o mesmo patch.

Instalar dependências Python na venv e verificar a alteração:

```bat
python -m pip install -r requirements-dev.txt
coverage run --source=app -m pytest -q
```

Arquivos afetados (após aplicar):

- `.github/workflows/quality.yml`
- `docs/metricas/COMO-MEDIR.md`

Após revisar e testar:

```bat
git add .github/workflows/quality.yml docs/metricas/COMO-MEDIR.md
git diff --cached
git commit -m "ci: publicar cobertura Python como artefato"
git push -u origin filipe/cobertura-ci
```

No GitHub, abrir Pull Request para main e pedir revisão a colega diferente. Guardar URL, diff e resultado do teste. Não adicionar as alterações de outros membros junto com sua tarefa. Os patches já versionados em contribuicoes são material de preparação; o commit individual é a aplicação revisada no código e seus testes.

## Como explicar depois de executar

“Revisei o pipeline para executar a suite com medicao e disponibilizar o arquivo de cobertura, explicando o recorte dessa metrica.”

Use essa fala só depois de executar e conferir o resultado. Diga o que realmente mudou e explique o apoio recebido quando pertinente.

## Estudar para responder

Qual diferenca entre cobertura e aprovacao? Onde aparece o artefato do workflow?

## Verificação disponível

A preparação combinada passou em 16 testes Python, Ruff e Bandit. A sintaxe do novo arquivo JavaScript foi verificada com Node. Isso não substitui a validação individual; Cypress e GitHub Actions desta proposta ainda não foram executados nesta preparação. As demais lacunas do protótipo, inclusive nova reserva após cancelamento, continuam pendentes.
