import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

import {API_PREFIX} from '@/constants'


Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    token: localStorage.getItem('token') || null,
    username: localStorage.getItem('username') || null
  },
  getters: {
    isLoggedIn (state) {
      return state.token != null
    },
    getToken (state) {
      return state.token || null
    },
    getUsername (state) {
      return state.username || null
    }
  },
  mutations: {
    saveLocal (state, {token, username}) {
      Vue.prototype.$http.defaults.headers.common.Authorization = `JWT ${token}`
      localStorage.setItem('token', token)
      localStorage.setItem('username', username)
      state.token = token
      state.username = username
    },
    destroyLocal (state) {
      Vue.prototype.$http.defaults.headers.common.Authorization = null
      localStorage.removeItem('token')
      localStorage.removeItem('username')
      state.token = null
      state.username = null
    },
  },
  actions: {
    refreshToken (context) {
      return new Promise((resolve, reject) => {
        // TODO: 참고로, 여기선 커스텀 http를 쓰는게 아니라 순정 axios를 씀. 이렇게 하면 store와 http의 상호 import 문제를 해결 할 수 있지! 해결인가..?
        axios
          .post(`${API_PREFIX}/token/refresh/`, {
            token: context.state.token
          })
          .then((res) => {
            context.commit('saveLocal', {
              token: res.data.token
            })
            resolve(res.data.token)
          })
          .catch((err) => {
            reject(err)
          })
      })
    },
    loginUser (context, {username, password}) {
      return new Promise((resolve, reject) => {
        axios
          .post(`${API_PREFIX}/token/auth/`, {
            username,
            password
          })
          .then((res) => {
            context.commit('saveLocal', {
              token: res.data.token,
              username
            })
            resolve()
          })
          .catch((err) => {
            reject(err)
          })
      })
    },
    logoutUser (context) {
      if(context.getters.isLoggedIn) {
        context.commit('destroyLocal')
      }
    }
  }
})
