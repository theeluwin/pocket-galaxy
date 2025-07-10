// base
import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useUserStore } from '@/stores/user'

// views
import HomeView from '@/views/HomeView.vue'
import LostView from '@/views/LostView.vue'
import LoginView from '@/views/LoginView.vue'
import RegisterView from '@/views/RegisterView.vue'
import PasswordRequestView from '@/views/PasswordRequestView.vue'
import PasswordResetView from '@/views/PasswordResetView.vue'
import ProfileView from '@/views/ProfileView.vue'
import DocumentListView from '@/views/DocumentListView.vue'
import ChatView from '@/views/ChatView.vue'


const requireAuth = () => {
  return (from: any, to: any, next: any) => {
    const authStore = useAuthStore()
    if(authStore.username) {
      return next()
    } else {
      return next({ name: 'login' })
    }
  }
}
const requireStaff = () => {
  return (from: any, to: any, next: any) => {
    const authStore = useAuthStore()
    const userStore = useUserStore()
    if(authStore.username && userStore.isStaff) {
      return next()
    } else {
      return next({ name: 'login' })
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
      path: '/register',
      name: 'register',
      component: RegisterView,
      meta: {
        hideNav: true
      }
    },
    {
      path: '/password/request',
      name: 'password-request',
      component: PasswordRequestView,
      meta: {
        hideNav: true
      }
    },
    {
      path: '/password/reset',
      name: 'password-reset',
      component: PasswordResetView,
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
      path: '/document/list',
      name: 'document-list',
      component: DocumentListView,
      beforeEnter: requireAuth()
    },
    {
      path: '/chat',
      name: 'chat',
      component: ChatView,
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
