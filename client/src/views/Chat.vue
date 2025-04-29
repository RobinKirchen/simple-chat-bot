<template>
  <div class="chat-container">
    <div class="chat-messages" ref="chatMessages">
      <div
        v-for="(msg, index) in messages"
        :key="index"
        :class="['message-wrapper', msg.sender === 'user' ? 'align-right' : 'align-left']"
      >
        <div
          :class="['message-bubble', msg.sender === 'user' ? 'user-bubble' : 'bot-bubble']"
        >
          {{ msg.text }}
        </div>
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
import { ref, onUpdated } from 'vue'

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
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ message: text }),
    });
    if (!response.ok) {
      throw new Error(`Response status: ${response.status}`);
    }

    const json = await response.json();
    messages.value.push({ sender: 'bot', text: json["message"].toString() });
  } catch (error) {
    console.error(error);
  }
}

// Auto-scroll to bottom on new message
onUpdated(() => {
  const container = chatMessages.value;
  if (container) {
    container.scrollTop = container.scrollHeight;
  }
});
</script>

<style scoped>
.chat-container {
   width: 80vw;
  height: 90vh;
  background: #f5f5f5;
  border-radius: 12px;
  border: 2px solid #4CAF50;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  font-family: sans-serif;

  /* Center on screen */
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.chat-messages {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 12px;
  border-bottom: 1px solid #4CAF50;
  background-color: #ffffff;
}

.message-wrapper {
  display: flex;
}

.align-right {
  justify-content: flex-end;
}

.align-left {
  justify-content: flex-start;
}

.message-bubble {
  padding: 10px 15px;
  border-radius: 20px;
  max-width: 70%;
  word-wrap: break-word;
  font-size: 14px;
  line-height: 1.4;
}

.user-bubble {
  background-color: #dcf8c6;
  color: #000;
  border-bottom-right-radius: 0;
}

.bot-bubble {
  background-color: #ececec;
  color: #000;
  border-bottom-left-radius: 0;
}

.chat-input {
  display: flex;
  padding: 15px;
  border-top: 1px solid #ddd;
  background-color: #fafafa;
}

.chat-input input {
  flex: 1;
  padding: 10px 14px;
  border: 1px solid #ccc;
  border-radius: 20px;
  outline: none;
}

.chat-input button {
  margin-left: 10px;
  padding: 10px 18px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.chat-input button:hover {
  background-color: #45a049;
}
</style>
