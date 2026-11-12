describe('FilaZero - pagina publica e protecao de acesso', () => {
  it('abre a pagina inicial com acesso ao login', () => {
    cy.visit('/');
    cy.contains('FilaZero').should('be.visible');
    cy.get('a[href="/entrar"]').first().should('be.visible');
  });

  it('recusa credenciais inexistentes sem autenticar', () => {
    cy.visit('/entrar');
    cy.get('input[name="identifier"]').type('nao-cadastrado@example.test');
    cy.get('input[name="password"]').type('SenhaIncorreta123');
    cy.get('button[type="submit"]').click();
    cy.url().should('include', '/entrar');
    cy.contains('Não foi possível entrar.').should('be.visible');
    cy.visit('/gestao');
    cy.url().should('include', '/entrar');
  });

  it('exige autenticacao para abrir a gestao', () => {
    cy.visit('/gestao');
    cy.url().should('include', '/entrar');
    cy.contains('Entre na sua conta para continuar.').should('be.visible');
  });
});
