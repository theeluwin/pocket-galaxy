import axios from 'axios'
import { defineStore } from 'pinia'
import { API_PREFIX } from '@/constants'

// Keys for localStorage
const ACCESS_TOKEN_KEY = 'accessToken'
const USERNAME_KEY = 'username'

export const useUserStore = defineStore('user', {
  state: () => ({
    username: localStorage.getItem(USERNAME_KEY) as string | null,
    accessToken: localStorage.getItem(ACCESS_TOKEN_KEY) as string | null,
  }),
  actions: {
    async login (username: string, password: string) {
      const res = await axios.post(`${API_PREFIX}/token/auth/`, {
        username,
        password
      }, {
        withCredentials: true
      })
      this.username = username
      this.accessToken = res.data.access
      localStorage.setItem(USERNAME_KEY, username)
      localStorage.setItem(ACCESS_TOKEN_KEY, res.data.access)
    },
    async verifyToken () {
      if (!this.accessToken) {
        return false
      }
      try {
        await axios.post(`${API_PREFIX}/token/verify/`, {
          token: this.accessToken
        }, {
          withCredentials: true
        })
        return true
      } catch {
        this.logout()
        return false
      }
    },
    async refreshToken () {
      const res = await axios.post(`${API_PREFIX}/token/refresh/`, {}, {
        withCredentials: true
      })
      this.accessToken = res.data.access
      localStorage.setItem(ACCESS_TOKEN_KEY, res.data.access)
    },
    async logout() {
      this.username = null
      this.accessToken = null
      localStorage.removeItem(USERNAME_KEY)
      localStorage.removeItem(ACCESS_TOKEN_KEY)
    }
  }
})
