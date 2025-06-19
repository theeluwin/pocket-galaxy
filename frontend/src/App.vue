<template>
  <v-app>
    <Nav v-if="!$route.meta.hideNav" />
    <v-main>
      <v-container>
        <router-view />
      </v-container>
    </v-main>
    <Footer v-if="!$route.meta.hideFooter" />
  </v-app>
</template>

<script setup lang="ts">
  import { useRoute } from 'vue-router'

  import Nav from '@/components/Nav.vue'
  import Footer from '@/components/Footer.vue'

  const route = useRoute()
</script>
