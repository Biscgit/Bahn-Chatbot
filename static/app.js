// let $SCRIPT_ROOT = {{ rootroute }};

function sendMessage() {
    console.debug("Pressed Button!")

    let sendButton = document.getElementById("send-button")

    // avoid multiple sending via enter-press
    if (sendButton.disabled) {
        return
    }

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
    // create chat bauble
    let messageBauble = document.createElement("p")
    messageBauble.classList.add('message')
    messageBauble.classList.add(user ? 'user_message' : 'bot_message')
    messageBauble.textContent = message

    let messageContainer = document.getElementById("chat-body")
    messageContainer.appendChild(messageBauble)

    // Scroll to the bottom
    messageContainer.scrollTop = messageContainer.scrollHeight
}

function handleKeyDown(event) {
    if (event.keyCode === 13) {
        event.preventDefault();
        sendMessage();
    }
}