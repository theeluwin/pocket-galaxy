<template>
  <div id="chat-view" class="container-small pt-5">
    <h1 class="text-center mb-5">Chat</h1>
    <v-form
      lazy-validation
      ref="formRef"
      v-model="form.isValid"
      @submit.prevent="sendMessage"
    >
      <v-text-field
        class="mb-3"
        label="Message"
        variant="outlined"
        prepend-inner-icon="mdi-message-outline"
        required
        type="text"
        v-model="form.content"
        :rules="[
          (v: string) => !!v || 'Message is required',
        ]"
      />
      <v-btn
        class="mb-5"
        block
        size="large"
        color="success"
        type="submit"
        :disabled="!form.isValid"
        :loading="form.isLoading"
      >
        Send
      </v-btn>
      <v-snackbar
        :text="snackbar.message"
        location="top"
        variant="outlined"
        :color="snackbar.color"
        v-model="snackbar.isVisible"
      >
        <template #actions>
          <v-btn @click="snackbar.isVisible = false">
            Close
          </v-btn>
        </template>
      </v-snackbar>
    </v-form>
    <v-divider class="my-10" v-if="messages.length > 0" />
    <div v-if="messages.length > 0">
      <v-card
        class="mb-3"
        v-for="message in messages"
        :key="message.id"
      >
        <template v-slot:text>
          <div class="d-flex justify-space-between">
            <b v-if="message.username === userStore.username" class="text-primary">
              {{ message.username }}
            </b>
            <b v-else>
              {{ message.username }}
            </b>
            <v-chip
              size="small"
              color="info"
              variant="text"
            >
              {{ formatDatetime(message.published_at) }}
            </v-chip>
          </div>
          <p>{{ message.content }}</p>
        </template>
      </v-card>
    </div>
  </div>
</template>

<script setup lang="ts">

  import { ref, reactive, nextTick, onMounted } from 'vue'
  import { useUserStore } from '@/stores/user'
  import http from '@/plugins/http'
  import { formatDatetime } from '@/utils'

  interface Message {
    id: number
    content: string
    user: number
    username: string
    published_at: string
    modified_at: string
  }

  const userStore = useUserStore()

  const formRef = ref()
  const messages = ref<Message[]>([])

  const form = reactive({
    content: '',
    isValid: true,
    isLoading: false
  })
  const snackbar = reactive({
    message: '',
    color: 'error',
    isVisible: false
  })

  async function sendMessage () {
    if (form.isLoading) {
      return
    }
    if (!formRef.value?.validate()) {
      return
    }
    form.isLoading = true
    try {
      await http.post('/api/messages/', {
        content: form.content
      })
      form.content = ''
      await nextTick()
      formRef.value?.resetValidation()
      snackbar.message = "Message sent successfully."
      snackbar.color = 'success'
      snackbar.isVisible = true
    } catch (error: any) {
      snackbar.message = error.response.data.error || "Send message failed."
      snackbar.color = 'error'
      snackbar.isVisible = true
    } finally {
      form.isLoading = false
    }
  }
  async function getMessages () {
    const response = await http.get('/api/messages/')
    messages.value = response.data.results
  }
  async function getWebsocketTicket () {
    const response = await http.post('/api/websocket/ticket/')
    return response.data.ticket
  }
  async function connectWebsocket (ticket: string) {
    const ws = new WebSocket(`ws://${window.location.host}/ws/chat/?ticket=${ticket}`)
    return ws
  }
  function handleWebsocketMessage (event: MessageEvent) {
    const data = JSON.parse(event.data)
    if (data.type === 'chat_message') {
      messages.value.unshift(data.message)
    }
  }
  onMounted(async () => {
    await getMessages()
    const ticket = await getWebsocketTicket()
    const ws = await connectWebsocket(ticket)
    ws.onmessage = handleWebsocketMessage
  })

</script>
