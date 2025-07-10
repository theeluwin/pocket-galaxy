<template>
  <div id="profile-view" class="container-small pt-5">
    <h1 class="text-center mb-5">Profile</h1>
    <v-card class="mb-10">
      <v-card-title class="px-5 py-6">
        <v-icon color="info">mdi-email</v-icon>
        Change Email
      </v-card-title>
      <v-card-text class="px-5 py-0">
        <v-form
          lazy-validation
          ref="usernameFormRef"
          v-model="usernameForm.isValid"
          @submit.prevent="changeUsername"
        >
          <v-text-field
            class="mb-3"
            label="Email"
            variant="outlined"
            prepend-inner-icon="mdi-email-outline"
            required
            type="email"
            v-model="usernameForm.username"
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
            v-model="usernameForm.usernameConfirm"
            :rules="[
              (v: string) => !!v || 'Confirm email is required',
              (v: string) => /.+@.+\..+/.test(v) || 'Invalid email format',
              (v: string) => v === usernameForm.username || 'Email does not match'
            ]"
          />
          <v-btn
            class="mb-5"
            block
            size="large"
            color="info"
            variant="elevated"
            prepend-icon="mdi-email-edit"
            type="submit"
            :disabled="!usernameForm.isValid"
            :loading="usernameForm.isLoading"
          >
            Change
          </v-btn>
        </v-form>
      </v-card-text>
    </v-card>
    <v-card class="mb-10">
      <v-card-title class="px-5 py-6">
        <v-icon color="warning">mdi-lock</v-icon>
        Change Password
      </v-card-title>
      <v-card-text class="px-5 py-0">
        <v-form
          lazy-validation
          ref="passwordFormRef"
          v-model="passwordForm.isValid"
          @submit.prevent="changePassword"
        >
          <v-text-field
            class="mb-3"
            label="New Password"
            variant="outlined"
            prepend-inner-icon="mdi-lock-outline"
            required
            type="password"
            v-model="passwordForm.password"
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
            v-model="passwordForm.passwordConfirm"
            :rules="[
              (v: string) => !!v || 'Confirm new password is required',
              (v: string) => v.length >= 8 || 'Password must be at least 8 characters long',
              (v: string) => v === passwordForm.password || 'Password does not match'
            ]"
          />
          <v-btn
            class="mb-5"
            block
            size="large"
            color="warning"
            variant="elevated"
            prepend-icon="mdi-lock-reset"
            type="submit"
            :disabled="!passwordForm.isValid"
            :loading="passwordForm.isLoading"
          >
            Change
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
  import { useUserStore } from '@/stores/user'
  import http from '@/plugins/http'

  const userStore = useUserStore()

  const usernameFormRef = ref()
  const passwordFormRef = ref()

  const usernameForm = reactive({
    username: userStore.username || '',
    usernameConfirm: userStore.username || '',
    isValid: true,
    isLoading: false
  })
  const passwordForm = reactive({
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

  async function changeUsername () {
    if (usernameForm.isLoading) {
      return
    }
    if (!usernameFormRef.value?.validate()) {
      return
    }
    usernameForm.isLoading = true
    try {
      const response = await http.patch('/api/users/profile/', {
        username: usernameForm.username
      })
      await userStore.getProfile()
      usernameForm.username = userStore.username
      usernameForm.usernameConfirm = userStore.username
      snackbar.message = response.data.message || "Email changed successfully."
      snackbar.color = 'success'
      snackbar.isVisible = true
    } catch (error: any) {
      snackbar.message = error.response.data.error || "Email change failed."
      snackbar.color = 'error'
      snackbar.isVisible = true
    } finally {
      usernameForm.isLoading = false
    }
  }
  async function changePassword () {
    if (passwordForm.isLoading) {
      return
    }
    if (!passwordFormRef.value?.validate()) {
      return
    }
    passwordForm.isLoading = true
    try {
      const response = await http.patch('/api/users/profile/', {
        password: passwordForm.password
      })
      passwordForm.password = ''
      passwordForm.passwordConfirm = ''
      await nextTick()
      passwordFormRef.value?.resetValidation()
      snackbar.message = response.data.message || 'Password changed successfully.'
      snackbar.color = 'success'
      snackbar.isVisible = true
    } catch (error: any) {
      snackbar.message = error.response.data.error || "Password change failed."
      snackbar.color = 'error'
      snackbar.isVisible = true
    } finally {
      passwordForm.isLoading = false
    }
  }

</script>
