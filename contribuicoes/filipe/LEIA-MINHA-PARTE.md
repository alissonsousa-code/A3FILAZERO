# Filipe — Cobertura no pipeline

## Preparação

Seguir [CONTRIBUTING](../../CONTRIBUTING.md) e começar no clone com main atualizada e trabalho anterior guardado. Se esta alteração já estiver integrada, não reaplicar. Branch proposta: `filipe/cobertura-ci`.

## Aplicação

```bat
git switch -c filipe/cobertura-ci
git apply --check contribuicoes/filipe/alteracoes.patch
git apply contribuicoes/filipe/alteracoes.patch
git diff
```

Se a verificação falhar, parar e conferir o estado do arquivo e da branch; não forçar. O teste usa os arquivos após aplicação.

## Verificação

```bat
coverage run --source=app -m pytest -q
```

Depois executar coverage report -m e coverage xml -o coverage.xml. Na execução GitHub Actions, conferir o artefato cobertura-python. A mudança não executa Cypress.

Arquivos da tarefa:

- `.github/workflows/quality.yml`
- `docs/metricas/COMO-MEDIR.md`

## Registro

Somente após revisar a mudança e os resultados:

```bat
git add .github/workflows/quality.yml docs/metricas/COMO-MEDIR.md
git diff --cached
git commit -m "ci: publicar cobertura Python como artefato"
git push -u origin filipe/cobertura-ci
```

Abrir PR e seguir o fluxo de revisão em CONTRIBUTING. Guardar os resultados reais; não declarar aprovação antes da execução.

## Estudo

Após executar, pode explicar: “Revisei o pipeline para executar a suite com medicao e disponibilizar o arquivo de cobertura, explicando o recorte dessa metrica.”

Saber responder: Qual diferenca entre cobertura e aprovacao? Onde aparece o artefato do workflow?

A explicação detalhada das alterações e seus limites está no [guia da equipe](../../docs/GUIA-DE-ESTUDO-E-APRESENTACAO.md).
