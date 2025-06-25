<template>
  <div class="registro">
    <h2>Crear cuenta</h2>
    <form @submit.prevent="registrar">
      <input v-model="nombre" type="text" placeholder="Nombre completo" required />
      <input v-model="correo" type="email" placeholder="Correo electrónico" required />
      <input v-model="contraseña" type="password" placeholder="Contraseña" required minlength="8" />
      <button type="submit">Registrarse</button>
    </form>
    <p v-if="error" class="error">{{ error }}</p>
    <p v-if="exito" class="exito">{{ exito }}</p>
    <router-link to="/">¿Ya tienes cuenta? Inicia sesión</router-link>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()
const nombre = ref('')
const correo = ref('')
const contraseña = ref('')
const error = ref('')
const exito = ref('')

const registrar = async () => {
  error.value = ''
  exito.value = ''
  // Validación básica en frontend
  if (nombre.value.length < 2) {
    error.value = 'El nombre debe tener al menos 2 caracteres.'
    return
  }
  if (!correo.value.includes('@')) {
    error.value = 'Correo electrónico inválido.'
    return
  }
  if (contraseña.value.length < 8) {
    error.value = 'La contraseña debe tener al menos 8 caracteres.'
    return
  }
  try {
    await axios.post('http://localhost:8000/usuarios/registrar', {
      nombre: nombre.value,
      correo: correo.value,
      contraseña: contraseña.value
    })
    exito.value = '¡Registro exitoso! Ahora puedes iniciar sesión.'
    setTimeout(() => router.push('/'), 2000)
  } catch (err) {
    error.value = err.response?.data?.detail || 'Error al registrar usuario.'
  }
}
</script>

<style scoped>
.registro {
  max-width: 400px;
  margin: 50px auto;
  padding: 30px;
  background: #202020;
  border-radius: 8px;
  color: white;
  display: flex;
  flex-direction: column;
}
input {
  margin: 10px 0;
  padding: 12px;
  font-size: 1rem;
  border-radius: 4px;
  border: none;
}
button {
  margin-top: 10px;
  padding: 12px;
  font-size: 1rem;
  background-color: #333;
  color: white;
  border: none;
  cursor: pointer;
}
.error {
  color: red;
  margin-top: 10px;
}
.exito {
  color: #4caf50;
  margin-top: 10px;
}
</style> 