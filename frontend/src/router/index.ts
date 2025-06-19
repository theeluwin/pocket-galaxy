// base
import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'

// views
import HomeView from '@/views/HomeView.vue'
import LostView from '@/views/LostView.vue'
import LoginView from '@/views/LoginView.vue'
import ProfileView from '@/views/ProfileView.vue'
import DocumentListView from '@/views/DocumentListView.vue'


const requireAuth = () => {
  return (from: any, to: any, next: any) => {
    const userStore = useUserStore()
    if(userStore.accessToken) {
      return next()
    } else {
      return next({name: 'login'})
    }
  }
}

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [

    // views
    {
      path: '/home',
      name: 'home',
      component: HomeView,
      beforeEnter: requireAuth()
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
      meta: {
        hideNav: true
      }
    },
    {
      path: '/profile',
      name: 'profile',
      component: ProfileView,
      beforeEnter: requireAuth()
    },
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
      path: '/:pathMatch(.*)*',
      name: 'lost',
      component: LostView,
      meta: {
        hideNav: true,
        hideFooter: true
      }
    }

  ],
})

export default router
