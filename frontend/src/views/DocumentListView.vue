<template>
  <Document
    v-for="document in documents"
    :key="document.id"
    :document="document"
  />
</template>

<script setup lang="ts">
  import { ref } from 'vue'

  import http from '@/plugins/http'

  import Document from '@/components/Document.vue'

  interface DocumentType {
    id: number,
    title: string,
    content: string,
    published_at: Date,
    modified_at: Date,
  }

  const documents = ref<DocumentType[]>([])

  const fetchDocuments = async () => {
    const res = await http.get('/documents/')
    documents.value = res.data.results.map((document: DocumentType) => ({
      ...document,
      published_at: new Date(document.published_at),
      modified_at: new Date(document.modified_at),
    }))
  }

  fetchDocuments()
</script>
