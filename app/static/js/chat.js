document.addEventListener("DOMContentLoaded", () => {
    const chatInput = document.getElementById("chat-input");
    const sendBtn = document.getElementById("send-btn");
    const chatMessages = document.getElementById("chat-messages");

    chatInput.addEventListener("keypress", function (e) {
        if (e.key === "Enter") {
            sendMessage();
        } 
    });

    sendBtn.addEventListener("click", sendMessage);

    async function sendMessage() {
        const message = chatInput.value.trim();
        if (message === "") {
            return;
        }

        addMessage("user", message);
        chatInput.value = "";

        try {
            const response = await fetch("/api/chat", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({ message })
            });

            const data = await response.json();
            addMessage("bot", data.response);
        } catch (error) {
            console.error("Error:", error);
        }
    }

    function addMessage(sender, text) {
        const messageDiv = document.createElement("div");
        if (sender === "user") {
            messageDiv.classList.add("user-message");
        } else if (sender == "bot") {
            messageDiv.classList.add("bot-message"); 
        }
        messageDiv.textContent = text;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
});