function sendMessage() {
    console.debug("Pressed Button!")

    let sendButton = document.getElementById("send-button")
    sendButton.disabled = true

    let inputElement = document.getElementById("message-input")
    const message = inputElement.value

    inputElement.value = ""
    pushMessage(0, message)

    // field has message excluding whitespace only
    if (message.trim().length === 0) {
        sendButton.disabled = false
        return
    }

    fetch('http://127.0.0.1:8000/request_answer', {
        method: 'POST',
        body: JSON.stringify({message: message}),
        headers: {'Content-Type': 'application/json'}

    })
        .then(resp => resp.json())
        .then(resp => {
            const answer = resp.message
            pushMessage(1, message)
        })
        .catch((error) => {
            console.error('Failed to get response:', error)
        })
}

function pushMessage(user, message) {
    // user: {0: user or 1: bot}
    let messageContainer = document.getElementById("chatbox");

    let messageElement = document.createElement("p");
    messageElement.textContent = message;

    messageContainer.appendChild(messageElement);

    // Scroll to the bottom
    messageContainer.scrollTop = messageContainer.scrollHeight;
}
