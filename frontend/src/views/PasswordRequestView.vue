<template>
  <div id="password-request-view" class="container-small pt-10">
    <h1 class="text-center mb-5">Password Reset Request</h1>
    <v-card class="mb-10">
      <v-card-text class="px-5 pt-5 pb-0">
        <v-form
          lazy-validation
          ref="formRef"
          v-model="form.isValid"
          @submit.prevent="requestPassword"
        >
          <v-text-field
            class="mb-3"
            label="Email"
            variant="outlined"
            prepend-inner-icon="mdi-email-outline"
            required
            type="email"
            v-model="form.email"
            :rules="[
              (v: string) => !!v || 'Email is required',
              (v: string) => /.+@.+\..+/.test(v) || 'Invalid email format'
            ]"
          />
          <v-btn
            class="mb-5"
            block
            size="large"
            color="info"
            prepend-icon="mdi-email-lock"
            type="submit"
            :disabled="!form.isValid"
            :loading="form.isLoading"
          >
            Send Reset Link
          </v-btn>
          <v-btn
            class="mb-5"
            block
            size="large"
            color="info"
            variant="text"
            @click="router.push({ name: 'login' })"
          >
            Go to Login
          </v-btn>
        </v-form>
      </v-card-text>
    </v-card>
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
  </div>
</template>

<script setup lang="ts">
  import { ref, reactive, nextTick } from 'vue'
  import { useRouter } from 'vue-router'
  import http from '@/plugins/http'

  const router = useRouter()

  const formRef = ref()

  const form = reactive({
    email: '',
    isValid: true,
    isLoading: false
  })
  const snackbar = reactive({
    message: '',
    color: 'error',
    isVisible: false
  })

  async function requestPassword () {
    if (form.isLoading) {
      return
    }
    if (!formRef.value?.validate()) {
      return
    }
    form.isLoading = true
    try {
      const response = await http.post('/api/users/password/request/', {
        email: form.email
      })
      form.email = ''
      await nextTick()
      formRef.value?.resetValidation()
      snackbar.message = response.data.message || "Password reset link sent to email."
      snackbar.color = 'success'
      snackbar.isVisible = true
    } catch (error: any) {
      snackbar.message = error.response.data.error || "Password reset link sending failed."
      snackbar.color = 'error'
      snackbar.isVisible = true
    } finally {
      form.isLoading = false
    }
  }
</script>
