<template>
  <div id="password-reset-view" class="container-small pt-10">
    <h1 class="text-center mb-5">Password Reset</h1>
    <v-card class="mb-10">
      <v-card-title class="px-5 py-6">
        <v-icon color="warning">mdi-lock</v-icon>
        Change Password
      </v-card-title>
      <v-card-text class="px-5 py-0">
        <v-form
          lazy-validation
          ref="formRef"
          v-model="form.isValid"
          @submit.prevent="changePassword"
        >
          <v-text-field
            class="mb-3"
            label="New Password"
            variant="outlined"
            prepend-inner-icon="mdi-lock-outline"
            required
            type="password"
            v-model="form.password"
            :rules="[
              (v: string) => !!v || 'New password is required',
              (v: string) => v.length >= 8 || 'Password must be at least 8 characters long'
            ]"
          />
          <v-text-field
            class="mb-3"
            label="Confirm New Password"
            variant="outlined"
            prepend-inner-icon="mdi-lock-check-outline"
            required
            type="password"
            v-model="form.passwordConfirm"
            :rules="[
              (v: string) => !!v || 'Confirm new password is required',
              (v: string) => v.length >= 8 || 'Password must be at least 8 characters long',
              (v: string) => v === form.password || 'Password does not match'
            ]"
          />
          <v-btn
            class="mb-5"
            block
            size="large"
            color="warning"
            prepend-icon="mdi-lock-reset"
            type="submit"
            :disabled="!form.isValid"
            :loading="form.isLoading"
          >
            Change
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

  async function changePassword () {
    if (form.isLoading) {
      return
    }
    if (!formRef.value?.validate()) {
      return
    }
    form.isLoading = true
    try {
      const response = await http.patch('/api/users/password/reset/', {
        token: router.currentRoute.value.query.token,
        password: form.password
      })
      form.password = ''
      form.passwordConfirm = ''
      await nextTick()
      formRef.value?.resetValidation()
      snackbar.message = response.data.message || 'Password changed successfully.'
      snackbar.color = 'success'
      snackbar.isVisible = true
    } catch (error: any) {
      snackbar.message = error.response.data.error || "Password change failed."
      snackbar.color = 'error'
      snackbar.isVisible = true
    } finally {
      form.isLoading = false
    }
  }
</script>
