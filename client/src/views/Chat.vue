<template>
  <div class="chat-container">
    <div class="chat-messages" ref="chatMessages">
      <div
        v-for="(msg, index) in messages"
        :key="index"
        :class="['message', msg.sender === 'user' ? 'user-message' : 'bot-message']"
      >
        {{ msg.text}}
      </div>
    </div>
    <div class="chat-input">
      <input
        v-model="userInput"
        @keyup.enter="sendMessage"
        type="text"
        placeholder="Type your message..."
      />
      <button @click="sendMessage">Send</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const messages = ref([])
const userInput = ref('')
const chatMessages = ref(null)

async function sendMessage() {
  const url = "http://127.0.0.1:5000";
  const text = userInput.value.trim()
  if (text === '') return

  messages.value.push({ sender: 'user', text })
  userInput.value = ''

  try {
    const response = await fetch(url, {method: "POST",headers: {
        "Content-Type": "application/json", // Specify JSON content type
      },
      body: JSON.stringify({ message: text }), // Convert the body to JSON
    });
    if (!response.ok) {
      throw new Error(`Response status: ${response.status}`);
    }

    const json = await response.json();
    messages.value.push({ sender: 'bot', text: json["message"].toString() });
    console.log(messages)
  } catch (error) {
    console.error(error);
  }
}
</script>

<style scoped>
.chat-container {
  width: 92vw;
  height: 92vh;
  padding: 4%;
  background: #ffffff;
  border-radius: 1px;
  box-shadow: 0px 0px 10px rgba(0,0,0,0.1);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.chat-messages {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.chat-input {
  display: flex;
  padding: 10px;
  border-top: 1px solid #ddd;
}

.chat-input input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  margin-right: 10px;
}

.chat-input button {
  padding: 10px 20px;
  border: none;
  background-color: #4CAF50;
  color: white;
  border-radius: 5px;
  cursor: pointer;
}

.chat-input button:hover {
  background-color: #45a049;
}

.message {
  padding: 10px;
  border-radius: 10px;
  max-width: 80%;
  word-wrap: break-word;
}

.user-message {
  background-color: #dcf8c6;
  align-self: flex-end;
}

.bot-message {
  background-color: #f1f0f0;
  align-self: flex-start;
}
</style>