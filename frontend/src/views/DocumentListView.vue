<template>
  <div>

    <!-- documents -->
    <v-row>
      <v-col
        sm="3"
        v-for="document in documents"
        :key="document.id"
      >
        <Document :document="document" />
      </v-col>
    </v-row>

    <!-- pagination -->
    <v-row v-if="isDocumentsInitialized">
      <v-col sm="3">
      </v-col>
      <v-col sm="9">
        <v-row>
          <v-col sm="3">
            <v-text-field
              label="페이지 번호"
              single-line
              v-model="pagination.directPageTarget"
              type="number"
              @keydown.enter="pageInput(pagination.directPageTarget)"
            />
          </v-col>
          <v-col sm="3" class="pt-5">
            <v-btn @click="pageInput(pagination.directPageTarget)">페이지 이동</v-btn>
          </v-col>
          <v-col sm="6">
            <v-pagination
              v-model="pagination.page"
              :length="pagination.maxPage"
              :total-visible="pagination.totalVisible"
              @input="pageInput"
            />
          </v-col>
        </v-row>
      </v-col>
    </v-row>

    <!-- overlay -->
    <v-overlay :value="isLoading" opacity=0.2>
      <v-progress-circular indeterminate size="128" color="purple" />
    </v-overlay>

  </div>
</template>

<style scoped>

</style>

<script>
  import {API_PREFIX} from '@/constants'
  import Document from '@/components/Document'

  const PAGE_SIZE = 20

  export default {
    name: 'DocumentListView',
    components: {
      'Document': Document
    },
    data () {
      return {
        isDocumentsInitialized: false,
        isLoading: false,
        documents: [],
        pagination: {
          directPageTarget: 1,
          page: 1,
          maxPage: 1,
          totalVisible: 7
        },
      }
    },
    methods: {
      loadDocuments (page) {
        this.isLoading = true
        const targetPage = parseInt(page)
        let params = {
          format: 'json',
          page: targetPage,
          page_size: PAGE_SIZE,
        }
        this.$http.get(`${API_PREFIX}/documents/`, {
          params: params
        })
        .then((res) => {
          this.documents = res.data.results
          this.pagination.page = targetPage
          this.pagination.maxPage = Math.max(Math.ceil(res.data.count / PAGE_SIZE), 1)
          this.isLoading = false
          this.isDocumentsInitialized = true
        })
      },
      pageInput (page) {
        page = parseInt(page)
        if(isNaN(page)) {
          page = 1
        } else if(page < 1) {
          page = 1
        } else if(page > this.pagination.maxPage) {
          page = this.pagination.maxPage
        }
        this.loadItems(page)
        window.scrollTo(0, 0)
      },
    },
    created () {
      this.loadDocuments(1)
    },
  }
</script>
