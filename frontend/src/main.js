import Vue from 'vue'
import router from '@/plugins/router'
import vuetify from '@/plugins/vuetify'
import store from '@/plugins/store'
import http from '@/plugins/http'

import App from '@/App.vue'


Vue.config.productionTip = false
Vue.prototype.$http = http

new Vue({
  vuetify,
  store,
  router: router,
  render: h => h(App)
}).$mount('#app')
