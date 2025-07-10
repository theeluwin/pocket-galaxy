<template>
  <div id="document-list-view" class="container pt-5">
    <h1 class="mb-5">Documents</h1>
    <v-data-table-server
      no-data-text="Documents not found."
      loading-text="Loading documents..."
      items-per-page-text="Documents per page"
      :headers="headers"
      :items="dt.items"
      :items-length="dt.itemsLength"
      :loading="dt.isLoading"
      v-model:page="dt.options.page"
      v-model:items-per-page="dt.options.itemsPerPage"
      v-model:sort-by="dt.options.sortBy"
      :items-per-page-options="[10, 20, 50, 100]"
      :hide-default-footer="dt.itemsLength <= dt.options.itemsPerPage"
      @update:options="getDocuments"
    >
      <template v-slot:item.id="{ item }">
        {{ item.id }}
      </template>
      <template v-slot:item.title="{ item }">
        {{ item.title }}
      </template>
      <template v-slot:item.content="{ item }">
        {{ item.content }}
      </template>
      <template v-slot:item.published_at="{ item }">
        {{ formatDatetime(item.published_at) }}
      </template>
      <template v-slot:item.modified_at="{ item }">
        {{ formatDatetime(item.modified_at) }}
      </template>
    </v-data-table-server>
  </div>
</template>

<script setup lang="ts">

  import { reactive } from 'vue'
  import type { DataTableSortItem } from 'vuetify'
  import http from '@/plugins/http'
  import { formatDatetime } from '@/utils'

  interface Document {
    id: number
    title: string
    content: string
    published_at: string
    modified_at: string
  }
  interface DataTableOptions {
    page: number
    itemsPerPage: number
    sortBy: DataTableSortItem[]
  }

  const headers = [
    {
      title: 'ID',
      key: 'id',
    },
    {
      title: 'Title',
      key: 'title',
      sortable: false,
    },
    {
      title: 'Content',
      key: 'content',
      sortable: false,
    },
    {
      title: 'Published At',
      key: 'published_at',
    },
    {
      title: 'Modified At',
      key: 'modified_at',
    }
  ]

  const dt = reactive({
    items: [] as Document[],
    itemsLength: 0,
    options: {
      page: 1,
      itemsPerPage: 10,
      sortBy: [{
        key: 'published_at',
        order: 'desc' as const,
      }]
    },
    isLoading: true,
  })

  async function getDocuments (options: DataTableOptions) {
    Object.assign(dt.options, options)
    dt.isLoading = true
    const params = {
      page: options.page,
      page_size: options.itemsPerPage,
      ordering: options.sortBy.map(sortItem => (sortItem.order === 'desc' ? '-' : '') + sortItem.key).join(',')
    }
    const response = await http.get('/api/documents/', { params })
    dt.items = response.data.results
    dt.itemsLength = response.data.count
    dt.isLoading = false
  }

</script>
