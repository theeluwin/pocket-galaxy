<template>
  <v-app id="inspire">
    <Nav v-if="!$route.meta.hideNav" />
    <v-main>
      <v-container id="container">
        <router-view />
      </v-container>
    </v-main>
    <Footer v-if="!$route.meta.hideFooter" />
  </v-app>
</template>

<style scoped>
  #container {
    max-width: 1200px;
  }
</style>

<script>
  import CommonNav from '@/components/common/Nav'
  import CommonFooter from '@/components/common/Footer'
  export default {
    name: 'App',
    components: {
      'Nav': CommonNav,
      'Footer': CommonFooter
    },
    props: {
      source: String
    }
  }
</script>
