/**
 * Variables
 */

let chatName = ''
let chatSocket = null
let chatWindowUrl = window.location.href
let chatRoomUuid = Math.random().toString(36).slice(2, 12)

var loc = window.location;

var wsStart = 'ws://';
if (loc.protocol == 'https:') {
    wsStart = 'wss://';
}

var endpoint = wsStart + loc.host + '/ws/notifications';
notification_websocket = new WebSocket(endpoint + '/');


notification_websocket.onmessage = function (e) {
    let data = JSON.parse(e.data);
    console.log("Just received this from the back end.. 0", data);

    if (data.type == 'room_created') {
        document.querySelector('#notification').innerHTML = `<div class="bg-indigo-900 text-center py-4 lg:px-4"> 
            <div class="p-2 bg-blue-600 items-center text-indigo-100 leading-none lg:rounded-full flex lg:inline-flex" role = "alert">
                <span class="font-semibold mr-2 text-left flex-auto">${ data.text }</span>
         </div >
        </div>`

        myPlay("Chat")
    }
    if (data.type == 'ticket_created') {
        document.querySelector('#notification').innerHTML = `<div class="bg-green-900 text-center py-4 lg:px-4"> 
            <div class="p-2 bg-green-600 items-center text-green-100 leading-none lg:rounded-full flex lg:inline-flex" role = "alert">
                <span class="font-semibold mr-2 text-left flex-auto">${data.text}</span>
         </div >
        </div>`

        myPlay("Ticket")
    }
}

notification_websocket.onclose = function (e) {
    console.log("websocket closed");
}


/**
 * Elements
 */

const chatElement = document.querySelector('#chat')
const chatOpenElement = document.querySelector('#chat_open')
const chatJoinElement = document.querySelector('#chat_join')
const chatIconElement = document.querySelector('#chat_icon')
const chatWelcomeElement = document.querySelector('#chat_welcome')
const chatRoomElement = document.querySelector('#chat_room')
const chatNameElement = document.querySelector('#chat_name')
const chatLogElement = document.querySelector('#chat_log')
const chatInputElement = document.querySelector('#chat_message_input')
const chatSubmitElement = document.querySelector('#chat_message_submit')


/**
 * Functions 
 */

function scrollToBottom() {
    chatLogElement.scrollTop = chatLogElement.scrollHeight
}


function getCookie(name) {
    var cookieValue = null

    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';')

        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim()

            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1))

                break
            }
        }
    }

    return cookieValue
}


function sendMessage() {
    chatSocket.send(JSON.stringify({
        'type': 'message',
        'message': chatInputElement.value,
        'name': chatName
    }))

    chatInputElement.value = ''
}


function onChatMessage(data) {
    console.log('onChatMessage', data)

    if (data.type == 'chat_message') {
        let tmpInfo = document.querySelector('.tmp-info')

        if (tmpInfo) {
            tmpInfo.remove()
        }

        if (data.agent) {
            chatLogElement.innerHTML += `
                <div class="flex w-full mt-2 space-x-3 max-w-md">
                    <div class="flex-shrink-0 h-10 w-10 rounded-full bg-gray-300 text-center pt-2">${data.initials}</div>

                    <div>
                        <div class="bg-gray-300 p-3 rounded-l-lg rounded-br-lg">
                            <p class="text-sm">${data.message}</p>
                        </div>
                        
                        <span class="text-xs text-gray-500 leading-none">${data.created_at} ago</span>
                    </div>
                </div>
            `
            myPlay()
        } else {
            chatLogElement.innerHTML += `
                <div class="flex w-full mt-2 space-x-3 max-w-md ml-auto justify-end">
                    <div>
                        <div class="p-4 rounded-xl bg-blue-100 text-black">
                            <p class="text-sm">${data.message}</p>
                        </div>
                        
                        <span class="text-xs text-gray-500 leading-none">${data.created_at} ago</span>
                    </div>

                    <div class="flex-shrink-0 h-10 w-10 rounded-full bg-gray-300 text-center pt-2">${data.initials}</div>
                </div>
            `
        }
    } else if (data.type == 'users_update') {
        chatLogElement.innerHTML += '<p class="mt-2">The manager has joined the chat!'
    } else if (data.type == 'writing_active') {
        if (data.agent) {
            let tmpInfo = document.querySelector('.tmp-info')

            if (tmpInfo) {
                tmpInfo.remove()
            }

            chatLogElement.innerHTML += `
                <div class="tmp-info flex w-full mt-2 space-x-3 max-w-md">
                    <div class="flex-shrink-0 h-10 w-10 rounded-full bg-gray-300 text-center pt-2">${data.initials}</div>

                    <div>
                        <div class="bg-gray-100 p-3 rounded-l-lg rounded-br-lg">
                            <p class="text-sm">The manager is writing a message</p>
                        </div>
                    </div>
                </div>
            `
        }
    }

    scrollToBottom()
}

function myPlay(Type) {
    console.log(loc.protocol + "/" + loc.host)


    if (Type === "Chat") {
        var t_audio = new Audio(loc.protocol + "/static/Chat_room.wav");
        t_audio.play();
    }
    if (Type === "Ticket") {
        var t_audio = new Audio(loc.protocol + "/static/Ticket.wav");
        t_audio.play();
    }
    var audio = new Audio(loc.protocol + "/static/Ding.wav");

    if (document.visibilityState !== 'visible') {
        audio.play();
    }

}

async function joinChatRoom() {
    console.log('joinChatRoom')

    chatName = chatNameElement.value

    console.log('Join as:', chatName)
    console.log('Room uuid:', chatRoomUuid)

    const data = new FormData()
    data.append('name', chatName)
    data.append('url', chatWindowUrl)

    await fetch(`/api/create-room/${chatRoomUuid}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: data
    })
        .then(function (res) {
            return res.json()
        })
        .then(function (data) {
            console.log('data', data)
        })

    var loc = window.location;

    var wsStart = 'ws://';
    if (loc.protocol == 'https:') {
        wsStart = 'wss://';
    }

    var endpoint = wsStart + loc.host + '/ws/' + chatRoomUuid;
    chatSocket = new WebSocket(endpoint + '/');

    console.log(chatSocket);
/**
 *     chatSocket = new WebSocket(`ws://${window.location.host}/ws/${chatRoomUuid}/`)
 */



    chatSocket.onmessage = function (e) {
        console.log('onMessage')

        onChatMessage(JSON.parse(e.data))
    }


    chatSocket.onopen = function (e) {
        console.log('onOpen - chat socket was opened')

        scrollToBottom()
    }


    chatSocket.onclose = function (e) {

        console.log('onClose - chat socket was closed')
    }
}

/**
 * Event listeners
 */

chatOpenElement.onclick = function (e) {
    e.preventDefault()

    chatIconElement.classList.add('hidden')
    chatWelcomeElement.classList.remove('hidden')

    return false
}


chatJoinElement.onclick = function (e) {
    e.preventDefault()

    chatWelcomeElement.classList.add('hidden')
    chatRoomElement.classList.remove('hidden')

    joinChatRoom()

    return false
}


chatSubmitElement.onclick = function (e) {
    e.preventDefault()

    sendMessage()

    return false
}


chatInputElement.onkeyup = function (e) {
    if (e.keyCode == 13) {
        sendMessage()
    }
}


chatInputElement.onfocus = function (e) {
    chatSocket.send(JSON.stringify({
        'type': 'update',
        'message': 'writing_active',
        'name': chatName
    }))
}