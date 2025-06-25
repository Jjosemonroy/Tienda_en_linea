<template>
  <nav class="sidebar" v-if="usuario">
    <div class="sidebar-header">
      <span class="sidebar-user">{{ usuario.nombre }}</span>
      <span class="sidebar-role">({{ usuario.rol }})</span>
    </div>
    <ul>
      <li><router-link to="/productos">Productos</router-link></li>
      <li><router-link to="/perfil">Perfil</router-link></li>
      <li v-if="usuario.rol === 'admin'"><router-link to="/admin">Admin</router-link></li>
      <li><a href="#" @click.prevent="cerrarSesion">Cerrar sesión</a></li>
    </ul>
  </nav>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const usuario = ref(JSON.parse(localStorage.getItem('usuario')))

onMounted(() => {
  // Actualizar usuario en cada navegación
  router.afterEach(() => {
    usuario.value = JSON.parse(localStorage.getItem('usuario'))
  })
})

watch(() => localStorage.getItem('usuario'), () => {
  usuario.value = JSON.parse(localStorage.getItem('usuario'))
})

function cerrarSesion() {
  localStorage.removeItem('token')
  localStorage.removeItem('usuario')
  router.push('/')
}
</script>

<style scoped>
.sidebar {
  position: fixed;
  left: 0;
  top: 0;
  width: 200px;
  height: 100vh;
  background: #181818;
  color: #fff;
  display: flex;
  flex-direction: column;
  padding: 24px 0;
  z-index: 1000;
}
.sidebar-header {
  margin-bottom: 32px;
  text-align: center;
}
.sidebar-user {
  font-weight: bold;
  font-size: 1.1rem;
}
.sidebar-role {
  font-size: 0.9rem;
  color: #4caf50;
  margin-left: 4px;
}
ul {
  list-style: none;
  padding: 0;
  margin: 0;
}
ul li {
  margin: 18px 0;
}
ul li a, ul li .router-link-active {
  color: #fff;
  text-decoration: none;
  font-size: 1rem;
  transition: color 0.2s;
}
ul li a:hover, ul li .router-link-active {
  color: #4caf50;
}
</style> 