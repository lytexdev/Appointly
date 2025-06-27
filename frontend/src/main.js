import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'

// Import components
import Home from './views/Home.vue'
import Dashboard from './views/Dashboard.vue'
import TenantBooking from './views/TenantBooking.vue'
import SuperAdmin from './views/SuperAdmin.vue'
import Login from './views/Login.vue'
import Register from './views/Register.vue'

// Routes
const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/dashboard', name: 'Dashboard', component: Dashboard, meta: { requiresAuth: true } },
  { path: '/super-admin', name: 'SuperAdmin', component: SuperAdmin, meta: { requiresAuth: true, requiresAdmin: true } },
  { path: '/login', name: 'Login', component: Login },
  { path: '/register', name: 'Register', component: Register },
  { path: '/:username', name: 'TenantBooking', component: TenantBooking, props: true }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach(async (to, from, next) => {
  const token = localStorage.getItem('token')
  
  if (to.meta.requiresAuth && !token) {
    next('/login')
    return
  }
  
  if (to.meta.requiresAdmin) {
    // Import auth store here to avoid circular dependency
    const { useAuthStore } = await import('./stores/auth')
    const authStore = useAuthStore()
    
    // Initialize auth if not done yet
    if (!authStore.user && token) {
      await authStore.init()
    }
    
    if (!authStore.user?.is_admin) {
      next('/dashboard')
      return
    }
  }
  
  next()
})

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)
app.mount('#app')
