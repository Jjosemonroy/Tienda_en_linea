<template>
  <transition name="sidebar-fade" mode="out-in">
    <v-navigation-drawer
      v-model="drawer"
      :rail="isCollapsed"
      :permanent="false"
      :temporary="false"
      @mouseenter="expandSidebar"
      @mouseleave="collapseSidebar"
      class="sidebar-vuetify"
      elevation="3"
      color="surface"
    >
      <!-- Header del sidebar -->
      <v-list-item
        prepend-avatar=""
        :title="!isCollapsed ? (usuario?.nombre || '') : ''"
        :subtitle="!isCollapsed ? (usuario?.rol || '') : ''"
        class="sidebar-header"
      >
        <template v-slot:prepend>
          <v-avatar
            :color="usuario ? 'primary' : 'grey'"
            size="56"
            class="user-avatar"
          >
            <span class="text-h6 font-weight-bold text-white">
              {{ usuario ? usuario.nombre.charAt(0).toUpperCase() : '' }}
            </span>
          </v-avatar>
        </template>
      </v-list-item>

      <v-divider></v-divider>

      <!-- Navegación -->
      <v-list density="compact" nav class="sidebar-nav" v-if="usuario">
        <v-list-item
          prepend-icon="mdi-view-dashboard"
          title="Dashboard"
          to="/admin"
          value="dashboard"
          class="nav-item"
          rounded="lg"
        ></v-list-item>

        <v-list-item
          prepend-icon="mdi-package-variant"
          title="Productos"
          to="/productos"
          value="productos"
          class="nav-item"
          rounded="lg"
        ></v-list-item>

        <v-list-item
          prepend-icon="mdi-cart"
          title="Carrito"
          to="/carrito"
          value="carrito"
          class="nav-item"
          rounded="lg"
        >
          <template v-slot:append>
            <v-badge
              v-if="carritoCount > 0"
              :content="carritoCount"
              color="error"
              size="small"
            ></v-badge>
          </template>
        </v-list-item>

        <v-list-item
          prepend-icon="mdi-account"
          title="Mi Perfil"
          to="/perfil"
          value="perfil"
          class="nav-item"
          rounded="lg"
        ></v-list-item>

        <v-list-item
          prepend-icon="mdi-history"
          title="Historial de Compras"
          to="/historial-compras"
          value="historial-compras"
          class="nav-item"
          rounded="lg"
        ></v-list-item>

        <v-list-item
          v-if="usuario && usuario.rol === 'admin'"
          prepend-icon="mdi-plus-circle"
          title="Crear Producto"
          to="/admin/crear-producto"
          value="crear-producto"
          class="nav-item"
          rounded="lg"
        ></v-list-item>
      </v-list>

      <template v-slot:append>
        <div class="pa-2">
          <v-btn
            block
            color="error"
            variant="outlined"
            prepend-icon="mdi-logout"
            @click="cerrarSesion"
            class="logout-btn"
            rounded="lg"
          >
            <span v-show="!isCollapsed">Cerrar Sesión</span>
          </v-btn>
        </div>
      </template>
    </v-navigation-drawer>
  </transition>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { getApiUrl } from '../config/api.js'

const router = useRouter()
const usuario = ref(null)
const carritoCount = ref(0)
const isCollapsed = ref(true)
const drawer = ref(true)
let collapseTimeout = null

const emit = defineEmits(['sidebarStateChange', 'logout'])

// Verificar usuario
function checkUser() {
  const storedUser = localStorage.getItem('usuario')
  const storedToken = localStorage.getItem('token')
  
  // Si no hay usuario o token, limpiar todo
  if (!storedUser || !storedToken) {
    if (usuario.value !== null) {
      usuario.value = null
      carritoCount.value = 0
      drawer.value = false
      isCollapsed.value = true
    }
    return
  }
  
  try {
    const newUser = JSON.parse(storedUser)
    
    // Verificar que el token no esté expirado
    try {
      const tokenPayload = JSON.parse(atob(storedToken.split('.')[1]))
      const currentTime = Math.floor(Date.now() / 1000)
      
      if (tokenPayload.exp && tokenPayload.exp < currentTime) {
        // Token expirado, limpiar todo
        localStorage.removeItem('usuario')
        localStorage.removeItem('token')
        usuario.value = null
        carritoCount.value = 0
        drawer.value = false
        isCollapsed.value = true
        return
      }
    } catch (tokenError) {
      // Si no se puede decodificar el token, limpiar todo
      localStorage.removeItem('usuario')
      localStorage.removeItem('token')
      usuario.value = null
      carritoCount.value = 0
      drawer.value = false
      isCollapsed.value = true
      return
    }
    
    // Verificar si el usuario cambió
    if (JSON.stringify(newUser) !== JSON.stringify(usuario.value)) {
      usuario.value = newUser
      if (newUser) {
        cargarCarrito()
        drawer.value = true
      } else {
        carritoCount.value = 0
        drawer.value = false
      }
    }
  } catch (error) {
    console.error('Error al parsear usuario:', error)
    // Si hay error, limpiar todo
    localStorage.removeItem('usuario')
    localStorage.removeItem('token')
    usuario.value = null
    carritoCount.value = 0
    drawer.value = false
    isCollapsed.value = true
  }
}

onMounted(() => {
  checkUser()
  emit('sidebarStateChange', isCollapsed.value)
  
  // Escuchar el evento de inicio de sesión exitoso
  window.addEventListener('login-success', checkUser)
  
  // Verificar cuando cambia el localStorage (para sincronización entre pestañas)
  window.addEventListener('storage', checkUser)
  
  // Escuchar el evento personalizado para actualizar el contador del carrito
  window.addEventListener('carritoActualizado', (event) => {
    carritoCount.value = event.detail.count
  })
})

// Watcher para el usuario
watch(usuario, (newUser) => {
  if (!newUser) {
    // Si no hay usuario, ocultar sidebar
    drawer.value = false
    isCollapsed.value = true
    carritoCount.value = 0
  } else {
    // Si hay usuario, mostrar sidebar
    drawer.value = true
    cargarCarrito()
  }
}, { immediate: true })

onUnmounted(() => {
  if (collapseTimeout) {
    clearTimeout(collapseTimeout)
  }
  window.removeEventListener('storage', checkUser)
  window.removeEventListener('login-success', checkUser)
  window.removeEventListener('carritoActualizado', null)
})

async function cargarCarrito() {
  if (!usuario.value) {
    carritoCount.value = 0
    return
  }
  
  try {
    const token = localStorage.getItem('token')
    const response = await fetch(`${getApiUrl('cart')}/${usuario.value.id}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    
    if (response.ok) {
      const data = await response.json()
      carritoCount.value = data.items ? data.items.length : 0
    } else {
      carritoCount.value = 0
    }
  } catch (error) {
    console.error('Error al cargar carrito:', error)
    carritoCount.value = 0
  }
}

function expandSidebar() {
  clearTimeout(collapseTimeout)
  isCollapsed.value = false
  emit('sidebarStateChange', false)
}

function collapseSidebar() {
  collapseTimeout = setTimeout(() => {
    isCollapsed.value = true
    emit('sidebarStateChange', true)
  }, 300) // Pequeño delay para evitar que se cierre inmediatamente
}

function cerrarSesion() {
  // Limpiar localStorage
  localStorage.removeItem('token')
  localStorage.removeItem('usuario')
  
  // Limpiar estado local inmediatamente
  usuario.value = null
  carritoCount.value = 0
  drawer.value = false
  isCollapsed.value = true
  
  // Emitir evento de cierre de sesión
  emit('logout')
  
  // Redirigir al login
  router.push('/')
}
</script>

<style scoped>
.sidebar-vuetify {
  transition: all 0.3s ease;
}

.sidebar-header {
  min-height: 100px;
}

.user-avatar {
  transition: transform 0.3s ease;
}

.user-avatar:hover {
  transform: scale(1.1) rotate(5deg);
}

.nav-item {
  margin: 4px 8px;
}

.logout-btn {
  transition: all 0.3s ease;
}

.logout-btn:hover {
  transform: translateY(-2px);
}

/* Responsive */
@media (max-width: 768px) {
  .sidebar-vuetify {
    width: 80px !important;
  }
}

/* Transiciones del sidebar */
.sidebar-fade-enter-active,
.sidebar-fade-leave-active {
  transition: all 0.3s ease;
}

.sidebar-fade-enter-from {
  transform: translateX(-100%);
  opacity: 0;
}

.sidebar-fade-leave-to {
  transform: translateX(-100%);
  opacity: 0;
}
</style>