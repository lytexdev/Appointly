import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '../services/api'

export const useTenantStore = defineStore('tenant', () => {
  const tenants = ref([])
  const currentTenant = ref(null)
  const loading = ref(false)
  const error = ref('')

  const fetchUserTenants = async () => {
    loading.value = true
    error.value = ''

    try {
      const response = await api.get('/tenants/')
      tenants.value = response.data
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to fetch tenants'
    } finally {
      loading.value = false
    }
  }

  const fetchTenantByUsername = async (username) => {
    loading.value = true
    error.value = ''

    try {
      const response = await api.get(`/tenants/${username}`)
      currentTenant.value = response.data
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || 'Tenant not found'
      currentTenant.value = null
      return null
    } finally {
      loading.value = false
    }
  }

  const createTenant = async (tenantData) => {
    loading.value = true
    error.value = ''

    try {
      const response = await api.post('/tenants/', tenantData)
      tenants.value.push(response.data)
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to create tenant'
      throw err
    } finally {
      loading.value = false
    }
  }

  const updateTenant = async (tenantId, tenantData) => {
    loading.value = true
    error.value = ''

    try {
      const response = await api.put(`/tenants/${tenantId}`, tenantData)
      const index = tenants.value.findIndex(t => t.id === tenantId)
      if (index !== -1) {
        tenants.value[index] = response.data
      }
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to update tenant'
      throw err
    } finally {
      loading.value = false
    }
  }

  const deleteTenant = async (tenantId) => {
    loading.value = true
    error.value = ''

    try {
      await api.delete(`/tenants/${tenantId}`)
      tenants.value = tenants.value.filter(t => t.id !== tenantId)
      return true
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to delete tenant'
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    tenants,
    currentTenant,
    loading,
    error,
    fetchUserTenants,
    fetchTenantByUsername,
    createTenant,
    updateTenant,
    deleteTenant
  }
})
