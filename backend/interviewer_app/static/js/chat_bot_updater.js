"use strict";

// Get all key HTML elements and csrf_token.
const form = document.getElementById("chat-form");
const input = document.getElementById("userPrompt");
const csrf_token = document.getElementById("csrf_token").value;
const chatBox = document.getElementById("chat-box");

// Adds a message to the chat-box div element.
// A new div element is created with the text being added to it as well as being give class name/s
// based on whether the message is a user or chat bot message.
function addMessage(role, text){
    const div = document.createElement("div");
    div.classList.add("message", role);
    div.textContent = text;
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;

    // The div is returned so text can be added to the element as the data is being streamed to the
    // page. This helps in making a visual effect where the text can be seen updating in the element on the fly.
    if(role === "bot"){
        return div;
    }
    else{
        return;
    }
}

// Handles the chat bot form where the user types their prompt which is sent to the OpenAI API.
async function handleUserInput(event){
    event.preventDefault();

    try{
        // Configuring settings for when submitting a POST request at the ask() route in a way that
        // is compliant and compatible for the OpenAI API.
        const options = {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({userPrompt: input.value}),
        };

        addMessage("user", input.value);
        input.value = "";
        const response = await fetch(url, options); // The url is obtained from the chat_bot_page.html which is embedded in the Script element and using JS within the element.

        // If the ok field within the response JSON object is false, then a response was not received from the API.
        if(!response.ok){
            throw new Error("Could not get API response.")
        }

        // Preparing for adding the stream of text data to the divBot element using reader.
        const reader = response.body.getReader();
        const divBot = addMessage("bot", "");

        // Manages the stream of data by adding it to the div element created for the chat bot response.
        // Each stream of data will also have a done value, this will either be True or False.
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