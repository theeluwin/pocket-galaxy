<template>
  <div>

    <v-navigation-drawer
      app
      v-model="drawer"
      clipped
    >

      <v-list dense>
        <v-list-item link :to="{name: 'home'}">
          <v-list-item-avatar>
            <v-icon class="blue white--text">mdi-home</v-icon>
          </v-list-item-avatar>
          <v-list-item-content>
            <v-list-item-title>홈</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
      <v-list dense>
        <v-list-item link :to="{name: 'document-list'}">
          <v-list-item-avatar>
            <v-icon class="orange white--text">mdi-file-document-multiple</v-icon>
          </v-list-item-avatar>
          <v-list-item-content>
            <v-list-item-title>문서</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>

      <v-divider />

      <v-list dense>
        <v-list-item link @click="logout">
          <v-list-item-action>
            <v-icon>mdi-logout</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>로그아웃</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>

    </v-navigation-drawer>

    <v-app-bar
      app
      color="indigo"
      dark
      clipped-left
    >
      <v-app-bar-nav-icon @click.stop="drawer = !drawer" />
      <v-toolbar-title>Pocket Galaxy</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-toolbar-items>
        <v-btn text class="no-text-transform">{{ username }}</v-btn>
      </v-toolbar-items>
    </v-app-bar>

  </div>
</template>

<style scoped>
  .no-text-transform {
    text-transform: none;
  }
</style>

<script>
  export default {
    name: 'CommonNav',
    data () {
      return {
        drawer: true
      }
    },
    computed: {
      username () {
        return this.$store.getters.getUsername
      }
    },
    methods: {
      async logout () {
        await this.$store.dispatch('logoutUser')
        this.$router.push({name: 'login'})
      }
    }
  }
</script>
