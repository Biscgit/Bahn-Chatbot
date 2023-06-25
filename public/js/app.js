// let $SCRIPT_ROOT = {{ rootroute }};

let messages = []
const user_id = Math.floor(Math.random() * 1e10)

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

    // field has message excluding whitespace only
    if (message.trim().length === 0) {
        sendButton.disabled = false
        return
    }

    pushMessage(true, message)
    push_history(true, message)

    fetch('http://127.0.0.1:8000/request_answer', {
        method: 'POST',
        body: JSON.stringify({
            user_id: user_id,
            message: message,
        }),
        headers: {'Content-Type': 'application/json'}

    })
        .then(resp => resp.json())
        .then(resp => {
            console.log(resp.message)
            pushMessage(false, resp.message)
            push_history(false, resp.message)
        })
        .catch((error) => {
            console.error('Failed to get response:', error)

            // get an "error"-Answer
            const answers = [
                "I am currently sleeping\ntry again later",
                "I can't access our servers at the moment",
                "There is nobody answering my requests"
            ]
            pushMessage(false, answers[Math.floor(Math.random() * answers.length)])
        })
        .then(() => {
            sendButton.disabled = false
        })
}

// user: {true: user or false: bot}
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

function push_history(user, new_message) {
    messages.push({user: messages})

    if (messages.length > 10) {
        messages.shift()
    }
}

// window.onbeforeunload =
function unl(event) {
    // You can perform any necessary cleanup tasks here.

    // Custom confirmation message
    var confirmationMessage = 'Are you sure you want to leave this page?';

    // For modern browsers
    event.preventDefault();
    event.returnValue = confirmationMessage;

    // For older browsers
    return confirmationMessage;
}

function handleKeyDown(event) {
    if (event.keyCode === 13) {
        event.preventDefault()
        sendMessage()
    }
}