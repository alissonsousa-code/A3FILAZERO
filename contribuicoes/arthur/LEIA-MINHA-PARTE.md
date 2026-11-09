# Arthur — Capacidade após check-in

## Preparação

Seguir [CONTRIBUTING](../../CONTRIBUTING.md) e começar no clone com main atualizada e trabalho anterior guardado. Se esta alteração já estiver integrada, não reaplicar. Branch proposta: `arthur/capacidade-checkin`.

## Aplicação

```bat
git switch -c arthur/capacidade-checkin
git apply --check contribuicoes/arthur/alteracoes.patch
git apply contribuicoes/arthur/alteracoes.patch
git diff
```

Se a verificação falhar, parar e conferir o estado do arquivo e da branch; não forçar. O teste usa os arquivos após aplicação.

## Verificação

```bat
python -m pytest -q tests/test_capacidade_checkin.py
```

Arquivos da tarefa:

- `app.py`
- `tests/test_capacidade_checkin.py`

## Registro

Somente após revisar a mudança e os resultados:

```bat
git add app.py tests/test_capacidade_checkin.py
git diff --cached
git commit -m "fix: manter ocupacao da vaga apos check-in"
git push -u origin arthur/capacidade-checkin
```

Abrir PR e seguir o fluxo de revisão em CONTRIBUTING. Guardar os resultados reais; não declarar aprovação antes da execução.

## Estudo

Após executar, pode explicar: “Apliquei e verifiquei a correcao da contagem de capacidade para incluir agendamentos com check-in.”

Saber responder: Por que checked_in continua ocupando a vaga? Em quais consultas a regra precisa ser consistente?

A explicação detalhada das alterações e seus limites está no [guia da equipe](../../docs/GUIA-DE-ESTUDO-E-APRESENTACAO.md).
