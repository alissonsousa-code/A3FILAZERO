import { citizen, login, logout, receptionist } from '../support/login';

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

describe('FilaZero - permissões por perfil', () => {
  it('impede que o cidadão acesse recepção ou gestão', () => {
    login(citizen, '/painel');
    for (const path of ['/equipe', '/gestao']) {
      cy.visit(path, { failOnStatusCode: false });
      cy.contains('h1', 'Acesso não permitido').should('be.visible');
      cy.contains('Erro 403').should('be.visible');
    }
  });

  it('impede que a recepção acesse gestão e encerra o acesso após sair', () => {
    login(receptionist, '/equipe');
    cy.visit('/gestao', { failOnStatusCode: false });
    cy.contains('h1', 'Acesso não permitido').should('be.visible');
    cy.contains('Erro 403').should('be.visible');
    logout();
    cy.visit('/equipe');
    cy.location('pathname').should('eq', '/entrar');
  });
});
