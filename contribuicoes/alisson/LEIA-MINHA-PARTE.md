# Alisson — Mensagens de erro e dois testes

## Preparação

Seguir [CONTRIBUTING](../../CONTRIBUTING.md) e começar no clone com main atualizada e trabalho anterior guardado. Se esta alteração já estiver integrada, não reaplicar. Branch proposta: `alisson/mensagens-erros`.

## Aplicação

```bat
git switch -c alisson/mensagens-erros
git apply --check contribuicoes/alisson/alteracoes.patch
git apply contribuicoes/alisson/alteracoes.patch
git diff
```

Se a verificação falhar, parar e conferir o estado do arquivo e da branch; não forçar. O teste usa os arquivos após aplicação.

## Verificação

```bat
python -m pytest -q tests/test_error_pages.py
```

Arquivos da tarefa:

- `templates/error.html`
- `tests/test_error_pages.py`

## Registro

Somente após revisar a mudança e os resultados:

```bat
git add templates/error.html tests/test_error_pages.py
git diff --cached
git commit -m "feat: orientar usuario nas paginas de erro"
git push -u origin alisson/mensagens-erros
```

Abrir PR e seguir o fluxo de revisão em CONTRIBUTING. Guardar os resultados reais; não declarar aprovação antes da execução.

## Estudo

Após executar, pode explicar: “Revisei e apliquei mensagens de erro especificas para cada situacao e verifiquei o retorno para o inicio.”

Saber responder: Por que 400, 403 e 404 sao diferentes? Como a pagina recebe code e message?

A explicação detalhada das alterações e seus limites está no [guia da equipe](../../docs/GUIA-DE-ESTUDO-E-APRESENTACAO.md).

Registro em 09/11/2026: commit [f03ba61](https://github.com/alissonsousa-code/A3FILAZERO/commit/f03ba61aa6782559ef2c41f0f1495f76b0098587) enviado e [PR #1](https://github.com/alissonsousa-code/A3FILAZERO/pull/1) aberto, aguardando revisão. A aplicação local já foi realizada; próximos passos são aprovação, merge e verificação integrada. Não reaplicar o patch na mesma cópia.
