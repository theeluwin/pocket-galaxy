// base
import Vue from 'vue'
import VueRouter from 'vue-router'
import store from '@/plugins/store'

// common
import CommonLostView from '@/views/common/LostView'
import CommonLoginView from '@/views/common/LoginView'
import CommonHomeView from '@/views/common/HomeView'

// views
import DocumentListView from '@/views/DocumentListView'


Vue.use(VueRouter)

const requireAuth = () => (from, to, next) => {
  if(store.getters.isLoggedIn) {
    return next()
  } else {
    return next({name: 'login'})
  }
}

export default new VueRouter({
  routes: [

    // common
    {
      path: '/login',
      name: 'login',
      component: CommonLoginView,
      meta: {
        hideNav: true,
        hideFooter: true
      }
    },
    {
      path: '/home',
      name: 'home',
      component: CommonHomeView,
      beforeEnter: requireAuth()
    },

    // views
    {
      path: '/documents',
      name: 'document-list',
      component: DocumentListView,
      beforeEnter: requireAuth()
    },

    // fallback
    {
      path: '/',
      name: 'index',
      redirect: {
        name: 'home'
      }
    },
    {
      path: '*',
      name: 'lost',
      component: CommonLostView,
      meta: {
        hideNav: true,
        hideFooter: true
      }
    }

  ]
})
