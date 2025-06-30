<template>
  <v-form
    lazy-validation
    id="form"
    ref="form"
    v-model="isValid"
    @submit.prevent="onClick"
  >
    <h1 class="mb-3">Pocket Galaxy</h1>
    <v-text-field
      required
      label="Username"
      type="text"
      v-model="body.username"
      :rules="rules.username"
      :error-messages="messages.username"
      class="mb-3"
    />
    <v-text-field
      required
      label="Password"
      type="password"
      v-model="body.password"
      :rules="rules.password"
      :error-messages="messages.password"
      class="mb-3"
    />
    <v-btn
      block
      color="success"
      type="submit"
      :disabled="!isValid"
      class="mb-5"
    >
      Login
    </v-btn>
    <v-snackbar
      location="top"
      color="error"
      variant="outlined"
      v-model="snackbar"
    >
      {{ messages.common }}
      <template #actions>
        <v-btn
          text="Close"
          @click="snackbar = false"
        />
      </template>
    </v-snackbar>
  </v-form>
</template>

<style scoped>
  #form {
    width: 100%;
    max-width: 480px;
    margin: 70px auto 0 auto;
  }
</style>

<script setup lang="ts">
  import { ref, reactive } from 'vue'
  import { useRouter } from 'vue-router'
  import { useUserStore } from '@/stores/user' // Use Pinia store

  const router = useRouter()
  const userStore = useUserStore()

  const form = ref()
  const isValid = ref(true)
  const snackbar = ref(false)

  const body = reactive({
    username: '',
    password: ''
  })
  const rules = {
    username: [(v: string) => !!v || 'Username is required'],
    password: [(v: string) => !!v || 'Password is required']
  }
  const messages = reactive({
    common: null as string | null,
    username: null as string | null,
    password: null as string | null
  })

  async function onClick() {
    if (!form.value?.validate()) {
      return
    }
    try {
      await userStore.login(body.username, body.password)
      router.push({ name: 'home' })
    } catch (err: any) {
      console.log(err)
      const resd = err?.response?.data || {}
      messages.username = resd.username || null
      messages.password = resd.password || null
      messages.common = resd.detail || null
      if (messages.common) {
        snackbar.value = true
      }
    }
  }
</script>
