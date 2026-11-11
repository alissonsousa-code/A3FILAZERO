# Medicao de qualidade

Executar na raiz: `coverage run --source=app -m pytest -q`, depois `coverage report -m` e `coverage xml -o coverage.xml`.

O pipeline registra o resumo e disponibiliza o XML no artefato cobertura-python. O arquivo mede Python e nao comprova cobertura de navegador ou do modulo de fila isoladamente. Nao ha limite minimo novo imposto por este workflow.

Aprovacao: aprovados / executados; apresentar nao executados a parte. Correcao: defeitos corrigidos e retestados / defeitos distintos registrados. Densidade: defeitos distintos / casos de uso analisados, declarando recorte. Informar commit, ambiente e data de toda medicao.
