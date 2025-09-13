"use strict";

const form = document.getElementById("chat-form");
const input = document.getElementById("userPrompt");
const csrf_token = document.getElementById("csrf_token").value;
const chatBox = document.getElementById("chat-box");

function addMessage(role, text){
    const div = document.createElement("div");
    div.classList.add("message", role);
    div.textContent = text;
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;

    if(role === "bot"){
        return div;
    }
    else{
        return;
    }
}

async function handleUserInput(event){
    event.preventDefault();

    try{
        const options = {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({userPrompt: input.value}),
        };

        addMessage("user", input.value);
        input.value = "";
        const response = await fetch(url, options);

        if(!response.ok){
            throw new Error("Could not get API response.")
        }

        const reader = response.body.getReader();
        const divBot = addMessage("bot", "");

        while(true){
            const { done, value } = await reader.read();

            if(done){
                break;
            }

            const data = new TextDecoder().decode(value);
            
            console.log(data);
            divBot.append(data);

            // const isScrolledToBottom = chatBox.scrollHeight - chatBox.clientHeight <= chatBox.scrollTop + 1

            // if (isScrolledToBottom) {
            //     chatBox.scrollTop = chatBox.scrollHeight - chatBox.clientHeight
            // }
        }
    }
    catch(error){
        console.error(error);
    }
}

form.addEventListener("submit", handleUserInput);