import { citizen, login, logout, receptionist } from '../support/login';

const regular = 'Cidadão Demonstração';
const priority = {
  name: 'Paciente Prioritário E2E',
  email: 'prioridade-e2e@example.test',
  password: 'SenhaTeste@123',
};

function joinQueue(unit, declared = false) {
  cy.visit('/unidades');
  cy.contains('.unit-card', unit).within(() => {
    cy.get('select[name="service"]').select('Consulta clínica');
    if (declared) cy.get('input[name="priority_declared"]').check();
    cy.contains('button', 'Entrar na fila virtual').click();
  });
}

function patient(name) {
  return cy.contains('.patient', name);
}

function registerPriorityCitizen() {
  cy.visit('/cadastro');
  cy.get('#name').type(priority.name);
  cy.get('#cpf').type('52998224725');
  cy.get('#birth_date').type('1990-01-01');
  cy.get('#email').type(priority.email);
  cy.get('#password').type(priority.password, { log: false });
  cy.get('input[name="lgpd_consent"]').check();
  cy.contains('button', 'Finalizar cadastro').click();
  cy.location('pathname').should('eq', '/entrar');
}

describe('Fila virtual', () => {
  it('mostra posição, impede segunda fila ativa e permite cancelar e voltar', () => {
    login(citizen, '/painel');
    joinQueue('Brotas');
    cy.location('pathname').should('eq', '/minha-fila');
    cy.get('#queue-status-label').should('have.text', 'Aguardando');
    cy.get('#queue-position').should('have.text', '1');

    joinQueue('Itapuã');
    cy.location('pathname').should('eq', '/painel');
    cy.contains('Você já possui uma fila ativa.').should('be.visible');
    cy.visit('/minha-fila');
    cy.get('[data-queue-poll]').should('contain.text', 'Brotas');

    cy.on('window:confirm', (message) => {
      expect(message).to.equal('Deseja sair desta fila?');
      return true;
    });
    cy.contains('button', 'Sair da fila').click();
    cy.contains('Saída da fila registrada.').should('be.visible');
    cy.visit('/minha-fila');
    cy.contains('Nenhuma fila ativa').should('be.visible');

    joinQueue('Itapuã');
    cy.get('[data-queue-poll]').should('contain.text', 'Itapuã');
    cy.contains('button', 'Sair da fila').click();
    cy.contains('Saída da fila registrada.').should('be.visible');
  });

  it('chama por prioridade confirmada entre presentes e conclui o atendimento', () => {
    login(citizen, '/painel');
    joinQueue('Centro');
    cy.get('#queue-position').should('have.text', '1');
    logout();

    registerPriorityCitizen();
    login(priority, '/painel');
    joinQueue('Centro', true);
    cy.get('#queue-position').should('have.text', '2');
    logout();

    login(receptionist, '/equipe');
    patient(priority.name).should('contain.text', 'Prioridade a confirmar');
    cy.contains('button', 'Chamar próximo paciente').click();
    cy.contains('Não há pacientes com presença confirmada').should('be.visible');
    patient(regular).should('contain.text', 'Aguardando');

    patient(regular).contains('button', 'Registrar presença').click();
    patient(regular).should('contain.text', 'Presente');
    patient(priority.name).within(() => {
      cy.get('input[name="priority_confirmed"]').check();
      cy.contains('button', 'Registrar presença').click();
    });
    patient(priority.name).should('contain.text', 'Prioridade confirmada');

    cy.contains('button', 'Chamar próximo paciente').click();
    patient(priority.name).should('contain.text', 'Chamado');
    patient(regular).should('contain.text', 'Presente');
    patient(priority.name).contains('button', 'Iniciar atendimento').click();
    patient(priority.name).should('contain.text', 'Em atendimento');
    patient(priority.name).contains('button', 'Concluir atendimento').click();
    cy.contains('Atendimento concluído.').should('be.visible');
    patient(priority.name).should('not.exist');

    cy.contains('button', 'Chamar próximo paciente').click();
    patient(regular).should('contain.text', 'Chamado');
    patient(regular).contains('button', 'Iniciar atendimento').click();
    patient(regular).contains('button', 'Concluir atendimento').click();
    patient(regular).should('not.exist');
  });
});
