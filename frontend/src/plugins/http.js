import axios from 'axios'
import store from '@/plugins/store'

import {API_PREFIX} from '@/constants'


let http = axios.create({
  baseURL: API_PREFIX,
  headers: {
    common: {
      Authorization: `JWT ${store.getters.getToken}`
    }
  }
})

http.interceptors.response.use(
  res => res,
  async err => {
    if(err.config && err.response && err.response.status === 401) {
      if(!store.getters.isLoggedIn) {
        throw err
      }
      if(err.config.url.endsWith('/token/refresh/')) {
        throw err
      }
      await store.dispatch('refreshToken')
      err.config.headers.Authorization = `JWT ${store.getters.getToken}`
      return http(err.config)
    } else {
      throw err
    }
  }
)

export default http
