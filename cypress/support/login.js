export const citizen = {
  email: 'cidadao@filazero.local',
  password: 'Cidadao@123',
};
export const receptionist = {
  email: 'recepcao@filazero.local',
  password: 'Recepcao@123',
};

export function login({ email, password }, destination) {
  cy.visit('/entrar');
  cy.get('input[name="identifier"]').type(email);
  cy.get('input[name="password"]').type(password, { log: false });
  cy.get('button[type="submit"]').click();
  cy.location('pathname').should('eq', destination);
}

export function logout() {
  cy.get('form[action="/sair"] button[type="submit"]').click();
  cy.location('pathname').should('eq', '/');
}
