<template>
  <v-container>
    <v-form
      id="form"
      ref="form"
      v-model="isValid"
      lazy-validation
      @submit.prevent
    >
      <v-row class="mb-2">
        <h1>Pocket Galaxy</h1>
      </v-row>
      <v-row>
        <v-text-field
          label="Username"
          type="text"
          v-model="body.username"
          :rules="rules.username"
          :error-messages="messages.username"
          required
        />
      </v-row>
      <v-row class="mb-3">
        <v-text-field
          label="Password"
          type="password"
          v-model="body.password"
          :rules="rules.password"
          :error-messages="messages.password"
          required
        />
      </v-row>
      <v-row>
        <v-alert
          dense
          outlined
          type="error"
          v-if="messages.common"
        >
          {{ messages.common }}
        </v-alert>
      </v-row>
      <v-row>
        <v-btn
          :disabled="!isValid"
          color="success"
          @click="onClick"
          type="submit"
          block
        >
          Login
        </v-btn>
      </v-row>
    </v-form>
  </v-container>
</template>

<style scoped>
  #form {
    width: 100%;
    max-width: 480px;
    margin: 70px auto 0 auto;
  }
</style>

<script>
  function perhaps(some_list) {
    if(some_list.length) {
      return some_list[0]
    }
    return null
  }
  export default {
    name: 'CommonLoginView',
    data () {
      return {
        isValid: true,
        body: {
          username: null,
          password: null
        },
        rules: {
          username: [v => !!v || "Username is required"],
          password: [v => !!v || "Password is required"]
        },
        messages: {
          common: null,
          username: null,
          password: null
        }
      }
    },
    methods: {
      onClick () {
        if(!this.$refs.form.validate()) {
          return
        }
        this.$store
          .dispatch('loginUser', this.body)
          .then(() => {
            this.$router.push({name: 'home'})
          })
          .catch((err) => {
            const resd = err.response.data
            this.messages.username = resd.username || null
            this.messages.password = resd.password || null
            this.messages.common = perhaps(resd.non_field_errors)
          })
      }
    }
  }
</script>
