import axios from 'axios'
import { useUserStore } from '@/stores/user'
import { API_PREFIX } from '@/constants'


const http = axios.create({
  baseURL: API_PREFIX,
  withCredentials: true
})

http.interceptors.request.use(
  (config) => {
    const userStore = useUserStore()
    if (userStore.accessToken) {
      config.headers.Authorization = `Bearer ${userStore.accessToken}`
    }
    return config
  }
)

http.interceptors.response.use(
  (res) => {
    return res
  },
  async (err) => {
    const userStore = useUserStore()
    const originalRequest = err.config
    if (originalRequest && err.response && err.response.status === 401) {
      if (originalRequest.url.endsWith('/token/refresh/')) {
        throw err
      }
      try {
        await userStore.refreshToken()
        originalRequest.headers.Authorization = `Bearer ${userStore.accessToken}`
        return http(originalRequest)
      } catch (refreshError) {
        throw refreshError
      }
    }
    throw err
  }
)

export default http
