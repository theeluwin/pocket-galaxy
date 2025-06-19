// vue
import { createApp } from 'vue'
import { createPinia } from 'pinia'

// vuetify
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

// components
import App from './App.vue'
import router from './router'

// init vuetify
const vuetify = createVuetify({
  components,
  directives,
})

// init app
const app = createApp(App)
app.use(createPinia())
app.use(router)
app.use(vuetify)
app.mount('#app')
