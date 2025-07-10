import axios from 'axios'
import { defineStore } from 'pinia'
import { AUTH_USERNAME_KEY, USER_USERNAME_KEY, USER_IS_STAFF_KEY } from '@/constants'


export const useAuthStore = defineStore('auth', {
  state: () => ({
    username: localStorage.getItem(AUTH_USERNAME_KEY) as string || '',
  }),
  actions: {
    async login (username: string, password: string) {
      const res = await axios.post('/api/token/login/', {
        username,
        password
      }, {
        withCredentials: true
      })
      this.username = username
      localStorage.setItem(AUTH_USERNAME_KEY, username)
    },
    async refreshToken () {
      const res = await axios.post('/api/token/refresh/', {}, {
        withCredentials: true
      })
    },
    async logout () {
      try {
        const res = await axios.post('/api/token/logout/', {}, {
          withCredentials: true
        })
      } catch (err: any) {
        if (err.response.status !== 401) {
          throw err
        }
      } finally {
        this.username = ''
        localStorage.removeItem(AUTH_USERNAME_KEY)
        localStorage.removeItem(USER_USERNAME_KEY)
        localStorage.removeItem(USER_IS_STAFF_KEY)
      }
    }
  }
})
