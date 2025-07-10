<template>
  <div id="nav-wrap">
    <v-navigation-drawer
      app
      v-model="drawer"
      :location="$vuetify.display.mobile ? 'bottom' : 'left'"
      clipped
    >
      <v-list>
        <v-list-item
          link
          prepend-icon="mdi-home"
          @click="navigate('home')"
        >
          Home
        </v-list-item>
        <v-list-item
          link
          prepend-icon="mdi-file-document"
          @click="navigate('document-list')"
        >
          Documents
        </v-list-item>
        <v-list-item
          link
          prepend-icon="mdi-forum"
          @click="navigate('chat')"
        >
          Chat
        </v-list-item>
        <v-divider />
        <v-list-item
          link
          prepend-icon="mdi-logout"
          @click="logout"
        >
          Logout
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
    <v-app-bar color="primary">
      <template v-slot:prepend>
        <v-app-bar-nav-icon @click.stop="drawer = !drawer" />
      </template>
      <v-app-bar-title
        class="cursor-pointer"
        @click="navigate('home')"
      >
        {{ SITE_TITLE }}
      </v-app-bar-title>
      <template v-slot:append>
        <v-btn
          class="text-transform-none"
          prepend-icon="mdi-account"
          @click="navigate('profile')"
        >
          {{ userStore.username }}
        </v-btn>
      </template>
    </v-app-bar>
  </div>
</template>

<script setup lang="ts">

  import { ref } from 'vue'
  import { useAuthStore } from '@/stores/auth'
  import { useUserStore } from '@/stores/user'
  import { useRouter } from 'vue-router'
  import { SITE_TITLE } from '@/constants'

  const authStore = useAuthStore()
  const userStore = useUserStore()
  const router = useRouter()

  const drawer = ref(false)

  const logout = async () => {
    drawer.value = false
    await authStore.logout()
    router.push({ name: 'login' })
  }
  const navigate = (name: string) => {
    drawer.value = false
    router.push({ name })
  }

</script>
