<template>
  <h1>Profile View</h1>
  <p>Your name: {{ userStore.username }}</p>
</template>

<script setup lang="ts">
  import { useUserStore } from '@/stores/user'

  const userStore = useUserStore()
</script>
