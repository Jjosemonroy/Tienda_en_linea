<template>
  <div class="login">
    <h2>Iniciar sesión</h2>
    <form @submit.prevent="login">
      <input v-model="correo" type="email" placeholder="Correo" required />
      <input v-model="contraseña" type="password" placeholder="Contraseña" required />
      <button type="submit">Entrar</button>
    </form>
    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()
const correo = ref('')
const contraseña = ref('')
const error = ref('')

const limpiarFormulario = () => {
  correo.value = ''
  contraseña.value = ''
}

const login = async () => {
  error.value = ''
  try {
    const res = await axios.post('http://localhost:8000/usuarios/login', {
      correo: correo.value,
      contraseña: contraseña.value
    })

    const token = res.data.access_token
    const usuario = res.data.usuario

    alert(`Bienvenido ${usuario.nombre} (${usuario.rol})`)

    // Guardar token y datos del usuario
    localStorage.setItem('token', token)
    localStorage.setItem('usuario', JSON.stringify(usuario))

    alert(`Bienvenido ${usuario.nombre} (${usuario.rol})`)

    limpiarFormulario()

    // Redireccionar según el rol
    if (usuario.rol === 'admin') {
      router.push('/admin')
    } else {
      router.push('/productos')
    }
  } catch (err) {
    if (err.response?.status === 401) {
      error.value = 'Tu cuenta esta inactiva. Contacta al administrador.'
    } else if (err.response?.status === 401) {
      error.value = 'Credenciales incorrectas. Intenta nuevamente.'
    } else {
      error.value = err.response?.data?.detail || 'Error de conexión con el servidor.'
    }

    limpiarFormulario()
  }
}
</script>

<style scoped>
.login {
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
</style>
