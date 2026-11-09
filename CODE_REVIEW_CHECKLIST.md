# Checklist de revisão de código — FilaZero

Antes de aprovar um Pull Request, o revisor deve conferir:

- [ ] A alteração está ligada a um RF, RNF, regra de negócio ou critério CA identificado?
- [ ] O fluxo principal e os fluxos alternativos foram considerados?
- [ ] Os dados recebidos são validados no servidor; a validação do navegador é apenas complementar?
- [ ] O acesso respeita o perfil e o escopo da unidade? Um cidadão não acessa dados de outro cidadão?
- [ ] As senhas continuam armazenadas com hash; nenhum segredo ou dado pessoal foi incluído no código/log?
- [ ] A operação evita duplicidade, corrida ou perda de posição (transação/condição atômica quando necessário)?
- [ ] Erros são tratados sem expor credenciais, CPF completo ou detalhes internos?
- [ ] Há teste unitário ou de integração para a alteração e teste de regressão para o fluxo afetado?
- [ ] A interface mantém contraste, rótulos, foco de teclado, mensagens claras e responsividade?
- [ ] A documentação e a matriz requisito → teste foram atualizadas?
- [ ] Ruff, Bandit e testes automatizados foram executados? Não há falha crítica pendente?

**Regra de aprovação proposta:** pelo menos um integrante diferente do autor revisa o Pull Request; alterações de autenticação, permissão, fila e reserva precisam de dois revisores quando possível.
