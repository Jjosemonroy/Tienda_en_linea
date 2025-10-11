<template>
  <v-app>
    <!-- Loading state mientras se inicializa -->
    <div v-if="!isInitialized" class="loading-overlay">
      <v-progress-circular
        indeterminate
        color="primary"
        size="64"
      ></v-progress-circular>
    </div>
    
    <Sidebar 
      v-if="isInitialized" 
      @sidebarStateChange="handleSidebarStateChange" 
      @logout="handleLogout" 
    />
    
    <v-main :class="{ 
      'main-content-expanded': isSidebarCollapsed && hasUser && isInitialized,
      'main-content-no-sidebar': !hasUser || !isInitialized
    }">
      <v-container fluid class="pa-6">
        <router-view />
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import Sidebar from './components/Sidebar.vue'

const isSidebarCollapsed = ref(true)
const hasUser = ref(false)
const isInitialized = ref(false)

// Verificar si hay usuario logueado
function checkUser() {
  const usuario = localStorage.getItem('usuario')
  const token = localStorage.getItem('token')
  
  // Verificar que el token no esté expirado
  if (token) {
    try {
      const tokenPayload = JSON.parse(atob(token.split('.')[1]))
      const currentTime = Math.floor(Date.now() / 1000)
      
      if (tokenPayload.exp && tokenPayload.exp < currentTime) {
        // Token expirado, limpiar
        localStorage.removeItem('usuario')
        localStorage.removeItem('token')
        hasUser.value = false
        return
      }
    } catch (tokenError) {
      // Token inválido, limpiar
      localStorage.removeItem('usuario')
      localStorage.removeItem('token')
      hasUser.value = false
      return
    }
  }
  
  const newHasUser = !!(usuario && token)
  
  if (newHasUser !== hasUser.value) {
    hasUser.value = newHasUser
  }
}

onMounted(() => {
  // Verificar usuario inicialmente
  checkUser()
  isInitialized.value = true
  
  // Verificar cuando la ventana recupera el foco
  window.addEventListener('focus', checkUser)
  
  // Verificar cuando cambia el localStorage (para sincronización entre pestañas)
  window.addEventListener('storage', checkUser)
})

onUnmounted(() => {
  window.removeEventListener('focus', checkUser)
  window.removeEventListener('storage', checkUser)
})

function handleSidebarStateChange(collapsed) {
  isSidebarCollapsed.value = collapsed
}

function handleLogout() {
  hasUser.value = false
  // Forzar verificación del estado
  checkUser()
}
</script>

<style scoped>
.main-content-expanded {
  margin-left: 80px;
}

.main-content-no-sidebar {
  margin-left: 0;
}

/* Responsive */
@media (max-width: 768px) {
  .main-content-expanded,
  .main-content-no-sidebar {
    margin-left: 0;
  }
}

/* Loading overlay */
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}
</style>
