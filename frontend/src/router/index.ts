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

const SITE_TITLE = import.meta.env.VITE_SITE_TITLE as string
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [

    // views
    {
      path: '/home',
      name: 'home',
      component: HomeView,
      meta: {
        title: SITE_TITLE
      },
      beforeEnter: requireAuth()
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
      meta: {
        title: `${SITE_TITLE} - Login`,
        hideNav: true
      }
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView,
      meta: {
        title: `${SITE_TITLE} - Register`,
        hideNav: true
      }
    },
    {
      path: '/password/request',
      name: 'password-request',
      component: PasswordRequestView,
      meta: {
        title: `${SITE_TITLE} - Forgot Password`,
        hideNav: true
      }
    },
    {
      path: '/password/reset',
      name: 'password-reset',
      component: PasswordResetView,
      meta: {
        title: `${SITE_TITLE} - Password Reset`,
        hideNav: true
      }
    },
    {
      path: '/profile',
      name: 'profile',
      component: ProfileView,
      meta: {
        title: `${SITE_TITLE} - Profile`,
      },
      beforeEnter: requireAuth()
    },
    {
      path: '/document/list',
      name: 'document-list',
      component: DocumentListView,
      meta: {
        title: `${SITE_TITLE} - Documents`,
      },
      beforeEnter: requireAuth()
    },
    {
      path: '/chat',
      name: 'chat',
      component: ChatView,
      meta: {
        title: `${SITE_TITLE} - Chat`,
      },
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
        title: `${SITE_TITLE}`,
        hideNav: true,
        hideFooter: true
      }
    }

  ],
})

router.afterEach((to) => {
  if (to.meta && to.meta.title) {
    document.title = to.meta.title as string
  } else {
    document.title = SITE_TITLE
  }
})

export default router
