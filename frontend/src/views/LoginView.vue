<template>
  <div id="login-view" class="container-small pt-10">
    <h1 class="text-center mb-5">{{ SITE_TITLE }} Login</h1>
    <v-form
      lazy-validation
      ref="formRef"
      v-model="form.isValid"
      @submit.prevent="login"
    >
      <v-text-field
        class="mb-3"
        label="Email"
        variant="outlined"
        prepend-inner-icon="mdi-email-outline"
        required
        type="email"
        v-model="form.username"
        :rules="[
          (v: string) => !!v || 'Email is required',
        ]"
      />
      <v-text-field
        class="mb-3"
        label="Password"
        variant="outlined"
        prepend-inner-icon="mdi-lock-outline"
        required
        type="password"
        v-model="form.password"
        :rules="[
          (v: string) => !!v || 'Password is required',
          (v: string) => v.length >= 8 || 'Password must be at least 8 characters long'
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
        Login
      </v-btn>
      <v-btn
        class="mb-5"
        block
        size="large"
        color="primary"
        @click="router.push({ name: 'register' })"
      >
        Go to Register
      </v-btn>
      <v-btn
        class="mb-5"
        block
        size="large"
        color="info"
        variant="text"
        @click="router.push({ name: 'password-request' })"
      >
        Forgot Password
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
  </div>
</template>

<script setup lang="ts">

  import { ref, reactive } from 'vue'
  import { useRouter } from 'vue-router'
  import { useAuthStore } from '@/stores/auth'
  import { useUserStore } from '@/stores/user'
  import { SITE_TITLE } from '@/constants'

  const router = useRouter()
  const authStore = useAuthStore()
  const userStore = useUserStore()

  const formRef = ref()

  const form = reactive({
    username: '',
    password: '',
    isValid: true,
    isLoading: false
  })
  const snackbar = reactive({
    message: '',
    color: 'error',
    isVisible: false
  })

  async function login () {
    if (form.isLoading) {
      return
    }
    if (!formRef.value?.validate()) {
      return
    }
    form.isLoading = true
    try {
      await authStore.login(form.username, form.password)
      await userStore.getProfile()
      router.push({ name: 'home' })
    } catch (error: any) {
      snackbar.message = error.response.data.error || "Login failed. Please check your email and password."
      snackbar.color = 'error'
      snackbar.isVisible = true
    } finally {
      form.isLoading = false
    }
  }

</script>
