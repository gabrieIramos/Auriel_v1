// Botão para abrir configurações
const settingsButton = document.getElementById('settings-button');
const settingsPanel = document.getElementById('settings-panel');
const closeSettings = document.getElementById('close-settings');

// Exibe o painel ao clicar no botão de configurações
settingsButton.addEventListener('click', () => {
    settingsPanel.classList.remove('hidden');
});

// Esconde o painel ao clicar no botão de fechar
closeSettings.addEventListener('click', () => {
    settingsPanel.classList.add('hidden');
});
