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

// Substitui **texto** por <span class="destaque">texto</span>
function formatBotResponse(text) {
    return text
        .replace(/\*\*(.*?)\*\*/g, '<span class="destaque">$1</span>')
        .replace(/\\n/g, '<br>'); // Transforma \n em <br>
}

        document.getElementById("chat-form").addEventListener("submit", async function (e) {
    e.preventDefault();

    const input = document.getElementById("message-input");
    const userMessage = input.value;
    input.value = "";

    const chatBox = document.getElementById("chat-box");

    // Exibe a mensagem do usuário imediatamente
    chatBox.innerHTML += `
        <div class="chat-message user-message">
            <p><strong>Você:</strong> ${userMessage}</p>
        </div>
    `;

    // Exibe a mensagem "Pesquisando..." imediatamente
    const tempId = "temp-bot-msg-" + Date.now();
    chatBox.innerHTML += `
        <div class="chat-message bot-message" id="${tempId}">
            <p><strong>Bot:</strong> Pesquisando...</p>
        </div>
    `;
    chatBox.scrollTop = chatBox.scrollHeight;

    // Envia a mensagem para o backend
    const response = await fetch("/send-message", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userMessage })
    });

    const data = await response.json();

    // Substitui "Pesquisando..." pela resposta real
    // document.getElementById(tempId).innerHTML = `
    // <p><strong>Bot:</strong> ${formatBotResponse(data.bot_response)}</p>
    // `;

    document.getElementById(tempId).innerHTML = `
     <p><strong>Bot:</strong> ${data.bot_response}</p>
     `;
});


