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
        const artworkTitle = document.getElementById("art_title").textContent;
        const artistName = document.getElementById("artist_name").textContent;
        const medium = document.querySelector(".art_panel h4.desc").textContent; 
        const imageUrl = document.getElementById("artwork_image").src;

        if (message === "") {
            return;
        }

        addMessage("user", message);
        chatInput.value = "";

        try {
            const response = await fetch("/api/chat", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({
                    message: message,
                    artwork_title: artworkTitle,
                    artist_name: artistName,
                    medium: medium,
                    image_url: imageUrl
                })
            });

            const data = await response.json();
            addMessage("bot", data.response);
        } catch (error) {
            console.error("Error:", error);
        }
    }

    function addMessage(sender, text) {
        const messageDiv = document.createElement("div");
        const messageText = document.createElement("h3");
        messageText.classList.add("chat");
        messageText.textContent = text;

        if (sender === "user") {
            messageDiv.classList.add("user-message");
        } else if (sender == "bot") {
            messageDiv.classList.add("bot-message"); 
        }

        messageDiv.appendChild(messageText);
        
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
});