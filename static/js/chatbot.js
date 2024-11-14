<<<<<<< HEAD
document.addEventListener("DOMContentLoaded", function() {
    const inputField = document.getElementById("chatbotInput");
    const sendButton = document.getElementById("sendButton");
    let messageCount = 0; // Contador para gerar IDs únicos

    function toggleInput(enabled) {
        inputField.disabled = !enabled;
        sendButton.disabled = !enabled;
    }

    async function getContextData() {
    try {
        const response = await fetch("http://localhost:8080/context_data", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            },
        });
        if (!response.ok) throw new Error("Erro ao carregar dados de contexto");
        return await response.json();
    } catch (error) {
        console.error("Erro ao obter dados do contexto:", error);
        return null;
    }
}


    async function enviarMensagem() {
        const userMessage = inputField.value.trim();
        const respostaContainer = document.getElementById("chatbotContent");

        if (userMessage !== "") {
            toggleInput(false); // Bloqueia o envio de novas mensagens

            // Criar e exibir a mensagem do usuário
            const userMessageElement = document.createElement("div");
            userMessageElement.classList.add("message", "user-message");
            userMessageElement.textContent = userMessage;
            respostaContainer.appendChild(userMessageElement);

            // Criar a div da resposta do bot com um id único
            const botResponseElement = document.createElement("div");
            botResponseElement.classList.add("message", "bot-message");
            botResponseElement.id = `botResponse-${messageCount}`;
            botResponseElement.textContent = "Carregando resposta...";
            respostaContainer.appendChild(botResponseElement);

            // Incrementar o contador para o próximo par de mensagens
            messageCount++;

            // Limpar o campo de entrada e rolar para o final
            inputField.value = "";
            respostaContainer.scrollTop = respostaContainer.scrollHeight;

            // Obter dados de contexto do servidor
            const contextData = await getContextData();
            const contexto = contextData 
                ? `Contexto atual: Quartos livres: ${contextData.pousadas.length} pousadas disponíveis, ${contextData.reservas.length} reservas, clientes: ${contextData.clientes.length}.`
                : "Contexto não disponível.";

            // Enviar a mensagem para o servidor
            const mensagemCompleta = contexto + "responda em poucas palavras " + userMessage;

            try {
                const response = await fetch("http://localhost:7000/ia", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ text: mensagemCompleta }),
                });

                if (!response.ok) {
                    throw new Error("Erro na requisição: " + response.statusText);
                }

                const responseText = await response.text();
                try {
                    const data = JSON.parse(responseText);
                    document.getElementById(`botResponse-${messageCount - 1}`).textContent = data.response;
                } catch (error) {
                    document.getElementById(`botResponse-${messageCount - 1}`).textContent = responseText;
                }
            } catch (error) {
                document.getElementById(`botResponse-${messageCount - 1}`).textContent = "Erro ao enviar a mensagem.";
                console.error("Erro:", error);
            } finally {
                toggleInput(true); // Reabilita o envio de mensagens
            }
        }
    }

    // Evento para clicar no botão Enviar
    sendButton.addEventListener("click", enviarMensagem);

    // Evento para pressionar a tecla Enter no campo de entrada
    inputField.addEventListener("keypress", function(event) {
        if (event.key === "Enter") {
            event.preventDefault(); // Prevenir a ação padrão do Enter
            enviarMensagem();
        }
    });

    // Evento para abrir/fechar a janela do chatbot
    document.getElementById("chatbotButton").addEventListener("click", function() {
        var chatbotWindow = document.getElementById("chatbotWindow");
        chatbotWindow.style.display = chatbotWindow.style.display === "block" ? "none" : "block";
        if (chatbotWindow.style.display === "block") {
            toggleInput(true); // Ativa o input quando o chatbot for aberto
        }
    });

    // Evento para fechar a janela do chatbot ao clicar fora
    document.addEventListener("click", function(event) {
        var chatbotWindow = document.getElementById("chatbotWindow");
        var chatbotButton = document.getElementById("chatbotButton");
        if (chatbotWindow.style.display === "block" &&
            !chatbotWindow.contains(event.target) &&
            event.target !== chatbotButton) {
            chatbotWindow.style.display = "none";
        }
    });
});
=======
document.addEventListener("DOMContentLoaded", function() {
    const inputField = document.getElementById("chatbotInput");
    const sendButton = document.getElementById("sendButton");
    let messageCount = 0; // Contador para gerar IDs únicos

    function toggleInput(enabled) {
        inputField.disabled = !enabled;
        sendButton.disabled = !enabled;
    }

    async function enviarMensagem() {
        const userMessage = inputField.value.trim();
        const respostaContainer = document.getElementById("chatbotContent");

        if (userMessage !== "") {
            toggleInput(false); // Bloqueia o envio de novas mensagens

            // Criar e exibir a mensagem do usuário
            const userMessageElement = document.createElement("div");
            userMessageElement.classList.add("message", "user-message");
            userMessageElement.textContent = userMessage;
            respostaContainer.appendChild(userMessageElement);

            // Criar a div da resposta do bot com um id único
            const botResponseElement = document.createElement("div");
            botResponseElement.classList.add("message", "bot-message");
            botResponseElement.id = `botResponse-${messageCount}`;
            botResponseElement.textContent = "Carregando resposta...";
            respostaContainer.appendChild(botResponseElement);

            // Incrementar o contador para o próximo par de mensagens
            messageCount++;

            // Limpar o campo de entrada e rolar para o final
            inputField.value = "";
            respostaContainer.scrollTop = respostaContainer.scrollHeight;

            // Enviar a mensagem para o servidor
            const contexto = "Nesta conversa, você terá que me responder dúvidas sobre uma pousada. Saiba que essa pousada tem 4 quartos livres e 2 ocupados, os quartos que estão livres estão na faixa de preço de 500 reais a diária.";
            const mensagemCompleta = contexto + userMessage;

            try {
                const response = await fetch("http://localhost:7000/ia", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ text: mensagemCompleta }),
                });

                if (!response.ok) {
                    throw new Error("Erro na requisição: " + response.statusText);
                }

                const responseText = await response.text();
                try {
                    const data = JSON.parse(responseText);
                    document.getElementById(`botResponse-${messageCount - 1}`).textContent = data.response;
                } catch (error) {
                    document.getElementById(`botResponse-${messageCount - 1}`).textContent = responseText;
                }
            } catch (error) {
                document.getElementById(`botResponse-${messageCount - 1}`).textContent = "Erro ao enviar a mensagem.";
                console.error("Erro:", error);
            } finally {
                toggleInput(true); // Reabilita o envio de mensagens
            }
        }
    }

    // Evento para clicar no botão Enviar
    sendButton.addEventListener("click", enviarMensagem);

    // Evento para pressionar a tecla Enter no campo de entrada
    inputField.addEventListener("keypress", function(event) {
        if (event.key === "Enter") {
            event.preventDefault(); // Prevenir a ação padrão do Enter
            enviarMensagem();
        }
    });

    // Evento para abrir/fechar a janela do chatbot
    document.getElementById("chatbotButton").addEventListener("click", function() {
        var chatbotWindow = document.getElementById("chatbotWindow");
        chatbotWindow.style.display = chatbotWindow.style.display === "block" ? "none" : "block";
        if (chatbotWindow.style.display === "block") {
            toggleInput(true); // Ativa o input quando o chatbot for aberto
        }
    });

    // Evento para fechar a janela do chatbot ao clicar fora
    document.addEventListener("click", function(event) {
        var chatbotWindow = document.getElementById("chatbotWindow");
        var chatbotButton = document.getElementById("chatbotButton");
        if (chatbotWindow.style.display === "block" &&
            !chatbotWindow.contains(event.target) &&
            event.target !== chatbotButton) {
            chatbotWindow.style.display = "none";
        }
    });
});
>>>>>>> 412eb28f518c8d638e83e68597755a303a14388f
