
 document.onload = scrollToBottom()
 setInterval(refreshConversationHTML, 3000)
 document.querySelector('form').addEventListener('submit', postMessage);




 /**
 * fill the textarea in ad reply to premade message
 */
function fillText() {
    const button =  document.getElementById('message1');
    const text =  button.textContent;
    document.getElementById('id_body').value = text;
}


/**
 * scroll to bottom of the conversation div
 */
function scrollToBottom() {
    let conversation_box = document.getElementById('conversation');
    conversation_box.scrollTop = conversation_box.scrollHeight;
}


/*                        */
/*  FETCHING MESSAGE JSON */
/*                        */

//get json data of all the messages in conversation
async function getMessages() {
    const conversation_box  = document.getElementById('conversation')
    const url = '/messages/conversation_json/34/'

    const json_response = await (await fetch(url)).json()

    return json_response;

}

// loop through the conversation messages and generate HTML for new ones, then 
// insert into the website HTML
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
}



/**
 * generate HTML template for message so it can be inserted into the website HTLM
 * @param {strig} current_user the username of current user
 * @param {obj} message json object of message data
 */
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




/*********************************/
/*** FETHCING CONVERSATION HTML **/
/*********************************/


/**
 * fetch html from server for conversation box template then refresh the
 * conversation div
 */
async function refreshConversationHTML() {
    const conversation_div  = document.getElementById('conversation')
    const url = '/messages/conversation_html/34/'

    const html_response = await (await fetch(url)).text()

    conversation_div.innerHTML = html_response

    scrollToBottom()
}


/**************************/
/*****FORM POST MESSAGE****/
/**************************/

async function postMessage(event) {
    event.preventDefault()
    
    let csrftoken = getCookie('csrftoken')
    
    let conversation_form = document.getElementById('conversation_form')
    let form_data = new FormData(conversation_form)
    document.getElementById('message-input').value = ''
    
    let response = await fetch('/messages/send_ajax/?conversation=34', {
        method: 'POST',
        body: form_data,
        credentials: 'include',
        headers: {
            "X-CSRFToken": csrftoken,
        }
    });

    await refreshConversationHTML()
    
    
}



function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

