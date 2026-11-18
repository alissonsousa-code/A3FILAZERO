import { citizen, login } from '../support/login';

describe('Agendamentos', () => {
  it('confirma reserva, bloqueia duplicidade e libera a vaga ao cancelar', () => {
    login(citizen, '/painel');
    cy.visit('/agendamentos');

    cy.get('.slot-card').first().find('input[name="slot_id"]').invoke('val').then((slotId) => {
      const slot = () => cy.get(`.slot-card:has(input[name="slot_id"][value="${slotId}"])`);
      slot().find('.slot-hours').invoke('text').then((hours) => {
        const [time, availability] = hours.trim().split(' · ');
        const capacity = Number.parseInt(availability, 10);

        slot().contains('button', 'Reservar').click();
        cy.contains('Agendamento confirmado!').should('be.visible');
        cy.contains('.item-row', 'Confirmado')
          .contains(/Código FZ-[0-9A-F]{6}$/).should('be.visible');
        slot().find('.slot-hours').should('have.text', `${time} · ${capacity - 1} vagas`);

        slot().contains('button', 'Reservar').click();
        cy.contains('você já possui reserva neste horário').should('be.visible');
        cy.get('.item-list .item-row').should('have.length', 1);
        slot().find('.slot-hours').should('have.text', `${time} · ${capacity - 1} vagas`);

        cy.on('window:confirm', (message) => {
          expect(message).to.equal('Cancelar este agendamento?');
          return true;
        });
        cy.contains('.item-row', 'Confirmado').contains('button', 'Cancelar').click();
        cy.contains('Agendamento cancelado e vaga liberada.').should('be.visible');
        cy.contains('.item-row', 'Cancelado').should('be.visible');
        slot().find('.slot-hours').should('have.text', hours);

        slot().contains('button', 'Reservar').click();
        cy.contains('.item-row', 'Confirmado').should('be.visible');
        cy.contains('.item-row', 'Cancelado').should('be.visible');
        slot().find('.slot-hours').should('have.text', `${time} · ${capacity - 1} vagas`);
      });
    });
  });
});
