<template>
  <div id="app">
    <nav class="navbar">
      <div class="nav-container">
        <router-link to="/" class="nav-logo">
          Appointly
        </router-link>
        
        <div class="nav-menu">
          <router-link to="/" class="nav-link">
            Home
          </router-link>
          
          <router-link 
            v-if="authStore.isAuthenticated" 
            to="/dashboard" 
            class="nav-link"
          >
            Dashboard
          </router-link>
          
          <router-link 
            v-if="authStore.user?.is_admin" 
            to="/super-admin" 
            class="nav-link"
          >
            Super Admin
          </router-link>
          
          <router-link 
            v-if="!authStore.isAuthenticated" 
            to="/login" 
            class="nav-link"
          >
            Login
          </router-link>
          
          <router-link 
            v-if="!authStore.isAuthenticated" 
            to="/register" 
            class="nav-link"
          >
            Register
          </router-link>
          
          <div v-if="authStore.isAuthenticated" class="user-menu">
            <span class="user-greeting">
              Hi, {{ authStore.user?.first_name || authStore.user?.email }}!
            </span>
            <button @click="logout" class="nav-link logout-btn">
              Logout
            </button>
          </div>
        </div>
      </div>
    </nav>

    <main class="main-content">
      <router-view />
    </main>

    <footer class="footer">
      <p>&copy; 2025 Appointly - Terminbuchungssystem</p>
    </footer>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useAuthStore } from './stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

const logout = () => {
  authStore.logout()
  router.push('/')
}

onMounted(async () => {
  await authStore.init()
})
</script>

<style lang="scss">
@import "./styles/main.scss";
</style>