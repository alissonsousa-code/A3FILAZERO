describe('FilaZero - fluxos de equipe', () => {
  it('permite que a recepção autentique e abra a fila', () => {
    cy.visit('/entrar');
    cy.get('input[name="identifier"]').type('recepcao@filazero.local');
    cy.get('input[name="password"]').type('Recepcao@123');
    cy.get('button[type="submit"]').click();
    cy.url().should('include', '/equipe');
    cy.contains('Painel da recepção').should('be.visible');
    cy.contains('Chamar próximo paciente').should('be.visible');
  });

  it('permite que o gestor abra a tela de gestão', () => {
    cy.visit('/entrar');
    cy.get('input[name="identifier"]').type('gestor@filazero.local');
    cy.get('input[name="password"]').type('Gestor@123');
    cy.get('button[type="submit"]').click();
    cy.url().should('include', '/equipe');
    cy.visit('/gestao');
    cy.contains('Gestão da unidade').should('be.visible');
    cy.contains('Criar horário').should('be.visible');
  });
});
