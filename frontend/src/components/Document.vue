<template>
  <v-card
    :title="document.title"
    :subtitle="formatDate(document.published_at)"
    :text="document.content"
    class="mb-5"
  />
</template>

<script setup lang="ts">
  const props = defineProps({
    document: {
      type: Object,
      required: true
    }
  })

  function formatDate(date: Date) {
    return date.toLocaleString()
  }
</script>
