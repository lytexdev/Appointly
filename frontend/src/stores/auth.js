import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '../services/api'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token'))
  const user = ref(null)
  const loading = ref(false)
  const error = ref('')

  const isAuthenticated = computed(() => !!token.value)

  const login = async (email, password) => {
    loading.value = true
    error.value = ''

    try {
      const response = await api.post('/auth/login-json', {
        email,
        password
      })

      token.value = response.data.access_token
      localStorage.setItem('token', token.value)
      
      // Set the token for future requests
      api.defaults.headers.common['Authorization'] = `Bearer ${token.value}`
      
      // Get user info
      await getCurrentUser()
      
      return true
    } catch (err) {
      error.value = err.response?.data?.detail || 'Login failed'
      return false
    } finally {
      loading.value = false
    }
  }

  const logout = () => {
    token.value = null
    user.value = null
    localStorage.removeItem('token')
    delete api.defaults.headers.common['Authorization']
  }

  const getCurrentUser = async () => {
    if (!token.value) return

    try {
      // Ensure token is set in headers
      api.defaults.headers.common['Authorization'] = `Bearer ${token.value}`
      
      const response = await api.get('/auth/me')
      user.value = response.data
    } catch (err) {
      console.error('Failed to get current user:', err)
      // Don't logout on 401 during init, might be token refresh issue
      if (err.response?.status === 401) {
        logout()
      }
    }
  }

  // Initialize auth state
  const init = async () => {
    if (token.value) {
      api.defaults.headers.common['Authorization'] = `Bearer ${token.value}`
      await getCurrentUser()
    }
  }

  return {
    token,
    user,
    loading,
    error,
    isAuthenticated,
    login,
    logout,
    getCurrentUser,
    init
  }
})
