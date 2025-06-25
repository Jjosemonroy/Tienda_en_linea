<template>
  <div class="perfil">
    <button class="volver" @click="volver">Volver</button>
    <h2>Mi perfil</h2>
    <form @submit.prevent="guardarCambios">
      <label>Nombre</label>
      <input v-model="nombre" type="text" required minlength="2" maxlength="100" />
      <label>Correo electrónico</label>
      <input v-model="correo" type="email" required />
      <div class="info">
        <span><b>Rol:</b> {{ usuario.rol }}</span>
        <span><b>Estado:</b> {{ usuario.estado }}</span>
      </div>
      <button type="submit">Guardar cambios</button>
      <p v-if="exito" class="exito">{{ exito }}</p>
      <p v-if="error" class="error">{{ error }}</p>
    </form>
    <hr />
    <h3>Cambiar contraseña</h3>
    <form @submit.prevent="cambiarPassword">
      <input v-model="actual" type="password" placeholder="Contraseña actual" required />
      <input v-model="nueva" type="password" placeholder="Nueva contraseña" required minlength="8" />
      <input v-model="confirmar" type="password" placeholder="Confirmar nueva contraseña" required minlength="8" />
      <button type="submit">Actualizar contraseña</button>
      <p v-if="exitoPass" class="exito">{{ exitoPass }}</p>
      <p v-if="errorPass" class="error">{{ errorPass }}</p>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const usuario = ref(JSON.parse(localStorage.getItem('usuario')))
const nombre = ref(usuario.value?.nombre || '')
const correo = ref(usuario.value?.correo || '')
const exito = ref('')
const error = ref('')

const actual = ref('')
const nueva = ref('')
const confirmar = ref('')
const exitoPass = ref('')
const errorPass = ref('')

const router = useRouter()

const guardarCambios = async () => {
  exito.value = ''
  error.value = ''
  if (nombre.value.length < 2) {
    error.value = 'El nombre debe tener al menos 2 caracteres.'
    return
  }
  if (!correo.value.includes('@')) {
    error.value = 'Correo electrónico inválido.'
    return
  }
  try {
    // Aquí deberías tener un endpoint para actualizar usuario (no implementado en backend aún)
    // await axios.put('http://localhost:8000/usuarios/actualizar', { id: usuario.value.id, nombre: nombre.value, correo: correo.value })
    exito.value = 'Datos actualizados (simulado, falta endpoint en backend).'
    usuario.value.nombre = nombre.value
    usuario.value.correo = correo.value
    localStorage.setItem('usuario', JSON.stringify(usuario.value))
  } catch (err) {
    error.value = 'Error al actualizar datos.'
  }
}

const cambiarPassword = async () => {
  exitoPass.value = ''
  errorPass.value = ''
  if (nueva.value !== confirmar.value) {
    errorPass.value = 'Las contraseñas no coinciden.'
    return
  }
  if (nueva.value.length < 8) {
    errorPass.value = 'La nueva contraseña debe tener al menos 8 caracteres.'
    return
  }
  try {
    await axios.put('http://localhost:8000/usuarios/cambiar-contraseña', {
      correo: usuario.value.correo,
      contraseña_actual: actual.value,
      nueva_contraseña: nueva.value
    })
    exitoPass.value = 'Contraseña actualizada correctamente.'
    actual.value = ''
    nueva.value = ''
    confirmar.value = ''
  } catch (err) {
    errorPass.value = err.response?.data?.detail || 'Error al cambiar contraseña.'
  }
}

function volver() {
  if (usuario.value.rol === 'admin') {
    router.push('/admin')
  } else {
    router.push('/productos')
  }
}
</script>

<style scoped>
.perfil {
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
  width: 100%;
}
button {
  margin-top: 10px;
  padding: 12px;
  font-size: 1rem;
  background-color: #333;
  color: white;
  border: none;
  cursor: pointer;
  width: 100%;
}
.error {
  color: red;
  margin-top: 10px;
}
.exito {
  color: #4caf50;
  margin-top: 10px;
}
.info {
  display: flex;
  gap: 16px;
  margin-bottom: 10px;
}
hr {
  margin: 30px 0;
  border: 1px solid #333;
}
.volver {
  background: #222;
  color: #fff;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  margin-bottom: 20px;
}
</style> 