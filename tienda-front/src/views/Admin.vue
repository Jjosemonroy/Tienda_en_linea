<template>
  <div class="admin">
    <h2>Panel de Administración</h2>
    <!-- Aquí iría el contenido del panel admin -->
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const usuario = ref(null)

onMounted(() => {
  usuario.value = JSON.parse(localStorage.getItem('usuario'))
})

function cerrarSesion() {
  localStorage.removeItem('token')
  localStorage.removeItem('usuario')
  router.push('/')
}
</script>

<style scoped>
.admin {
  padding: 40px;
  color: white;
}
</style>
