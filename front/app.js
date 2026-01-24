// // actually idk if we need this for this project just common to have in frontend hierarchy

// function sendMessage() {
//     const input = document.getElementById('chatInput');
//     const messagesContainer = document.getElementById('chatMessages');
//     const message = input.value.trim();

//     if (!message) return;

//     // user message
//     const userMsg = document.createElement('div');
//     userMsg.style.cssText = 'background:#ffb3d9;color:white;padding:12px 20px;border-radius:18px;margin-bottom:10px;max-width:70%;margin-left:auto;';
//     userMsg.textContent = message;
//     messagesContainer.appendChild(userMsg);

//     fetch('/api/chatbot', {
//         method: 'POST',
//         headers: {'Content-Type': 'application/json'},
//         body: JSON.stringify({message: message})
//     })
//     .then(res => res.json())
//     .then(data => {
//         const botMsg = document.createElement('div');
//         botMsg.style.cssText = 'background:#fff5f8;color:#666;padding:12px 20px;border-radius:18px;margin-bottom:10px;max-width:70%;border:2px solid #ffd6e8;';
//         botMsg.textContent = data.reply;
//         messagesContainer.appendChild(botMsg);
//         messagesContainer.scrollTop = messagesContainer.scrollHeight;
//     });

//     input.value = '';
// }
