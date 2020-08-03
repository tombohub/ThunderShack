

function fillText() {
    const button =  document.getElementById('message1');
    const text =  button.textContent;
    document.getElementById('id_body').value = text;
}

document.onload = scrollToBottom()


function scrollToBottom() {
    let conversation_box = document.getElementById('conversation');
    conversation_box.scrollTop = conversation_box.scrollHeight;
}

//get new messages in conversation
async function getMessages() {
    const conversation_box  = document.getElementById('conversation')
    const url = '/messages/conversation_ajax/34/'

    const json_response = await (await fetch(url)).json()

    return json_response;

}

// add new message to the HTML
async function addMessage() {
    const private_messages_list = await getMessages()

    const conversation_box  = document.getElementById('conversation');
    last_message_id = conversation_box.lastElementChild.id

    const current_user = document.getElementById('current-user').value
    
    let messages_HTML_array = []
    
    for (let i = 0; i < private_messages_list.length; i++) {
        let message = private_messages_list[i];
        if (message.id > last_message_id) {
            let message_HTML = getMessageHTML(current_user, message)
            messages_HTML_array.push(message_HTML)
            conversation_box.insertAdjacentHTML("beforeend", message_HTML)
        }
    }

    scrollToBottom()

    

    //conversation_box.insertAdjacentHTML("beforeend", message_HTML)
}

function getMessageHTML(current_user, message) {
    if (current_user === message.sender) {
        message_HTML = `<div class='align-self-end' id='${message.id}'>
            <div class='text-light bg-primary rounded text-center p-2'>
                ${message.body}
            </div>
            <small class='text-muted'>${message.date}</small>
            </div>`;
    } else {
        message_HTML = `<div class='align-self-start' id='${message.id}'>
            <div class='text-dark bg-light rounded text-center p-2'>
                ${message.body}
            </div>
            <small class='text-muted'>${message.date}</small>
            </div>`;
    }
    return message_HTML
}