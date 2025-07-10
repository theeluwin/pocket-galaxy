<template>
  <div id="register-view" class="container-small pt-10">
    <h1 class="text-center mb-5">{{ SITE_TITLE }} Register</h1>
    <v-form
      lazy-validation
      ref="formRef"
      v-model="form.isValid"
      @submit.prevent="register"
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
          (v: string) => /.+@.+\..+/.test(v) || 'Invalid email format'
        ]"
      />
      <v-text-field
        class="mb-3"
        label="Confirm Email"
        variant="outlined"
        prepend-inner-icon="mdi-email-check-outline"
        required
        type="email"
        v-model="form.usernameConfirm"
        :rules="[
          (v: string) => !!v || 'Email is required',
          (v: string) => /.+@.+\..+/.test(v) || 'Invalid email format',
          (v: string) => v === form.username || 'Email does not match'
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
      <v-text-field
        class="mb-3"
        label="Confirm Password"
        variant="outlined"
        prepend-inner-icon="mdi-lock-check-outline"
        required
        type="password"
        v-model="form.passwordConfirm"
        :rules="[
          (v: string) => !!v || 'Confirm password is required',
          (v: string) => v.length >= 8 || 'Password must be at least 8 characters long',
          (v: string) => v === form.password || 'Password does not match'
        ]"
      />
      <v-btn
        class="mb-5"
        text="Register"
        block
        size="large"
        color="primary"
        type="submit"
        :disabled="!form.isValid"
        :loading="form.isLoading"
      />
      <v-btn
        class="mb-5"
        text="Go to Login"
        block
        size="large"
        color="success"
        @click="router.push({ name: 'login' })"
      />
      <v-snackbar
        :text="snackbar.message"
        location="top"
        variant="outlined"
        :color="snackbar.color"
        v-model="snackbar.isVisible"
      >
        <template #actions>
          <v-btn
            @click="snackbar.isVisible = false"
          >
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
  import http from '@/plugins/http'
  import { SITE_TITLE } from '@/constants'

  const router = useRouter()
  const authStore = useAuthStore()
  const userStore = useUserStore()

  const formRef = ref()

  const form = reactive({
    username: '',
    usernameConfirm: '',
    password: '',
    passwordConfirm: '',
    isValid: true,
    isLoading: false
  })
  const snackbar = reactive({
    message: '',
    color: 'error',
    isVisible: false
  })

  async function register () {
    if (form.isLoading) {
      return
    }
    if (!formRef.value?.validate()) {
      return
    }
    form.isLoading = true
    try {
      await http.post('/api/users/register/', {
        username: form.username,
        password: form.password
      })
      await authStore.login(form.username, form.password)
      await userStore.getProfile()
      router.push({ name: 'home' })
    } catch (error: any) {
      snackbar.message = error.response.data.error || "Registration failed."
      snackbar.color = 'error'
      snackbar.isVisible = true
    } finally {
      form.isLoading = false
    }
  }

</script>
