<template>
  <v-navigation-drawer
    app
    v-model="drawer"
    :location="$vuetify.display.mobile ? 'bottom' : 'left'"
    clipped
  >
    <v-list>
      <v-list-item
        link
        title="Home"
        prepend-icon="mdi-home"
        @click="navigate('home')"
      />
      <v-list-item
        link
        title="Documents"
        prepend-icon="mdi-file-document-multiple"
        @click="navigate('document-list')"
      />
      <v-divider />
      <v-list-item
        link
        title="Logout"
        prepend-icon="mdi-logout"
        @click="logout"
      />
    </v-list>
  </v-navigation-drawer>
  <v-app-bar color="primary">
    <template v-slot:prepend>
      <v-app-bar-nav-icon @click.stop="drawer = !drawer" />
    </template>
    <v-app-bar-title
      class="clickable-title"
      @click="navigate('home')"
    >
      Pocket Galaxy
    </v-app-bar-title>
    <template v-slot:append>
      <v-btn
        class="no-text-transform"
        prepend-icon="mdi-account"
        @click="navigate('profile')"
      >
        {{ userStore.username }}
      </v-btn>
    </template>
  </v-app-bar>
</template>

<style scoped>
  .no-text-transform {
    text-transform: none;
  }
  .clickable-title {
    cursor: pointer;
  }
</style>

<script setup lang="ts">
  import { ref } from 'vue'
  import { useUserStore } from '@/stores/user'
  import { useRouter } from 'vue-router'

  const drawer = ref(false)
  const userStore = useUserStore()
  const router = useRouter()

  const logout = async () => {
    drawer.value = false
    await userStore.logout()
    router.push({ name: 'login' })
  }

  const navigate = (name: string) => {
    drawer.value = false
    router.push({ name })
  }
</script>
