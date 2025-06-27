import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '../services/api'

export const useSlotStore = defineStore('slot', () => {
  const slots = ref([])
  const availableSlots = ref([])
  const loading = ref(false)
  const error = ref('')

  const fetchTenantSlots = async (tenantId) => {
    loading.value = true
    error.value = ''

    try {
      const response = await api.get(`/tenants/${tenantId}/slots`)
      slots.value = response.data
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to fetch slots'
    } finally {
      loading.value = false
    }
  }

  const fetchAvailableSlots = async (tenantUsername) => {
    loading.value = true
    error.value = ''

    try {
      const response = await api.get(`/tenants/${tenantUsername}/slots`)
      availableSlots.value = response.data
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to fetch available slots'
    } finally {
      loading.value = false
    }
  }

  const createSlot = async (tenantId, slotData) => {
    loading.value = true
    error.value = ''

    try {
      const response = await api.post(`/tenants/${tenantId}/slots`, slotData)
      slots.value.push(response.data)
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to create slot'
      throw err
    } finally {
      loading.value = false
    }
  }

  const bookSlot = async (tenantUsername, slotId, bookingData) => {
    loading.value = true
    error.value = ''

    try {
      const response = await api.post(`/tenants/${tenantUsername}/slots/${slotId}/book`, bookingData)
      // Remove booked slot from available slots
      availableSlots.value = availableSlots.value.filter(s => s.id !== slotId)
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to book slot'
      throw err
    } finally {
      loading.value = false
    }
  }

  const deleteSlot = async (slotId) => {
    loading.value = true
    error.value = ''

    try {
      await api.delete(`/slots/${slotId}`)
      slots.value = slots.value.filter(s => s.id !== slotId)
      return true
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to delete slot'
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    slots,
    availableSlots,
    loading,
    error,
    fetchTenantSlots,
    fetchAvailableSlots,
    createSlot,
    bookSlot,
    deleteSlot
  }
})
