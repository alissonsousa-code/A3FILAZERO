const cpfInput = document.querySelector('#cpf');

cpfInput?.addEventListener('input', () => {
  cpfInput.value = cpfInput.value
    .replace(/\D/g, '')
    .slice(0, 11)
    .replace(/(\d{3})(\d)/, '$1.$2')
    .replace(/(\d{3})(\d)/, '$1.$2')
    .replace(/(\d{3})(\d{1,2})$/, '$1-$2');
});

document.querySelectorAll('form[data-confirm]').forEach((form) => {
  form.addEventListener('submit', (event) => {
    if (!window.confirm(form.dataset.confirm)) event.preventDefault();
  });
});

const queue = document.querySelector('[data-queue-poll]');

if (queue) {
  const status = queue.querySelector('#queue-status-label');
  const position = queue.querySelector('#queue-position');
  const estimate = queue.querySelector('#queue-estimate');
  const updated = queue.querySelector('#queue-updated');
  const cancelForm = queue.querySelector('[data-queue-cancel]');

  function setText(element, value) {
    const text = String(value);
    if (element.textContent.trim() !== text) element.textContent = text;
  }

  async function refreshQueue() {
    try {
      const response = await fetch(queue.dataset.queuePoll, {
        headers: {Accept: 'application/json'},
      });

      if (response.redirected) {
        setText(updated, 'Sua sessão terminou. Entre novamente para acompanhar a fila.');
        return;
      }

      if (!response.ok) throw new Error('Falha ao consultar a fila');

      const data = await response.json();
      setText(status, data.active ? data.status_label : 'Você não possui fila ativa');
      setText(position, data.position ?? '—');
      setText(estimate, data.active ? `${data.estimated_minutes} min` : '—');
      if (cancelForm) cancelForm.hidden = !data.active || data.status === 'attending';

      const time = data.active ? new Date(data.updated_at) : new Date();
      setText(updated, `Última sincronização às ${time.toLocaleTimeString('pt-BR')}`);
    } catch {
      setText(updated, 'Conexão indisponível. A fila será consultada novamente em instantes.');
    }

    window.setTimeout(refreshQueue, 5000);
  }

  refreshQueue();
}
