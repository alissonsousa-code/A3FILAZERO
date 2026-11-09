# Cláudio — Chamada por presença

## Preparação

Seguir [CONTRIBUTING](../../CONTRIBUTING.md) e começar no clone com main atualizada e trabalho anterior guardado. Se esta alteração já estiver integrada, não reaplicar. Branch proposta: `claudio/presenca-chamada`.

## Aplicação

```bat
git switch -c claudio/presenca-chamada
git apply --check contribuicoes/claudio/alteracoes.patch
git apply contribuicoes/claudio/alteracoes.patch
git diff
```

Se a verificação falhar, parar e conferir o estado do arquivo e da branch; não forçar. O teste usa os arquivos após aplicação.

## Verificação

```bat
python -m pytest -q tests/test_presenca.py
```

Arquivos da tarefa:

- `app.py`
- `tests/test_presenca.py`

## Registro

Somente após revisar a mudança e os resultados:

```bat
git add app.py tests/test_presenca.py
git diff --cached
git commit -m "fix: chamar apenas pacientes com presenca confirmada"
git push -u origin claudio/presenca-chamada
```

Abrir PR e seguir o fluxo de revisão em CONTRIBUTING. Guardar os resultados reais; não declarar aprovação antes da execução.

## Estudo

Após executar, pode explicar: “Revisei a regra de chamada para considerar apenas presenca confirmada e validei dois cenarios de fila.”

Saber responder: Qual diferenca entre waiting e present? Por que filtrar no SELECT e no UPDATE?

A explicação detalhada das alterações e seus limites está no [guia da equipe](../../docs/GUIA-DE-ESTUDO-E-APRESENTACAO.md).
