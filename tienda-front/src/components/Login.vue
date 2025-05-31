<template>
  <div class="login">
    <h2>Iniciar sesión</h2>
    <form @submit.prevent="login">
      <input v-model="correo" type="email" placeholder="Correo" required />
      <input v-model="contraseña" type="password" placeholder="Contraseña" required />
      <button type="submit">Entrar</button>
    </form>
    <p v-if="error">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const correo = ref('')
const contraseña = ref('')
const error = ref('')

const login = async () => {
  try {
    const res = await axios.post('http://localhost:8000/usuarios/login', {
      correo: correo.value,
      contraseña: contraseña.value
    })
    const token = res.data.access_token
    localStorage.setItem('token', token)
    alert(`Bienvenido ${res.data.usuario.nombre} (${res.data.usuario.rol})`)
    // Redireccionar según rol, más adelante
  } catch (err) {
    error.value = err.response?.data?.detail || 'Error de conexión'
  }
}
</script>

<style scoped>
.login {
  max-width: 400px;
  margin: 50px auto;
  display: flex;
  flex-direction: column;
}
input, button {
  margin: 8px 0;
  padding: 10px;
  font-size: 1rem;
}
</style>
