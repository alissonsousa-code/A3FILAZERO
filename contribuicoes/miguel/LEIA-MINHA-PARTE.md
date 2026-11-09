# Miguel — Regressão de segurança

## Preparação

Seguir [CONTRIBUTING](../../CONTRIBUTING.md) e começar no clone com main atualizada e trabalho anterior guardado. Se esta alteração já estiver integrada, não reaplicar. Branch proposta: `miguel/regressao-seguranca`.

## Aplicação

```bat
git switch -c miguel/regressao-seguranca
git apply --check contribuicoes/miguel/alteracoes.patch
git apply contribuicoes/miguel/alteracoes.patch
git diff
```

Se a verificação falhar, parar e conferir o estado do arquivo e da branch; não forçar. O teste usa os arquivos após aplicação.

## Verificação

```bat
python -m pytest -q tests/test_protecao_sessao.py
```

Arquivos da tarefa:

- `tests/test_protecao_sessao.py`

## Registro

Somente após revisar a mudança e os resultados:

```bat
git add tests/test_protecao_sessao.py
git diff --cached
git commit -m "test: verificar CSRF sessao e cancelamento alheio"
git push -u origin miguel/regressao-seguranca
```

Abrir PR e seguir o fluxo de revisão em CONTRIBUTING. Guardar os resultados reais; não declarar aprovação antes da execução.

## Estudo

Após executar, pode explicar: “Revisei e executei testes que verificam token CSRF, expiracao por inatividade e protecao da reserva de outro cidadao.”

Saber responder: Por que verificar o estado no banco alem do HTTP? Como o teste evita esperar 16 minutos?

A explicação detalhada das alterações e seus limites está no [guia da equipe](../../docs/GUIA-DE-ESTUDO-E-APRESENTACAO.md).
