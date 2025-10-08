<template>
  <v-container fluid class="login-container fill-height">
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="6" lg="4">
        <v-card class="login-card" elevation="8" rounded="xl">
          <v-card-text class="text-center pa-8">
            <!-- Header -->
            <div class="mb-8">
              <v-avatar
                size="80"
                color="primary"
                class="mb-4"
              >
                <v-icon size="40" color="white">mdi-package-variant</v-icon>
              </v-avatar>
              <h1 class="text-h4 font-weight-bold text-primary mb-2">
                Bienvenido de vuelta
              </h1>
              <p class="text-body-1 text-medium-emphasis">
                Inicia sesión en tu cuenta
              </p>
            </div>

            <!-- Formulario -->
            <v-form @submit.prevent="login">
              <v-text-field
                v-model="correo"
                label="Correo electrónico"
                type="email"
                placeholder="tu@email.com"
                prepend-inner-icon="mdi-email"
                variant="outlined"
                rounded="lg"
                required
                class="mb-4"
                :rules="[rules.required, rules.email]"
              ></v-text-field>

              <v-text-field
                v-model="contraseña"
                label="Contraseña"
                type="password"
                placeholder="Tu contraseña"
                prepend-inner-icon="mdi-lock"
                variant="outlined"
                rounded="lg"
                required
                class="mb-6"
                :rules="[rules.required, rules.min]"
              ></v-text-field>

              <!-- Mensaje de error -->
              <v-alert
                v-if="error"
                type="error"
                variant="tonal"
                class="mb-6"
                :text="error"
                closable
                @click:close="error = ''"
              ></v-alert>

              <!-- Botón de login -->
              <v-btn
                type="submit"
                color="primary"
                size="large"
                block
                rounded="lg"
                :loading="loading"
                :disabled="loading"
                class="mb-6"
                elevation="2"
              >
                <v-icon start>mdi-login</v-icon>
                {{ loading ? 'Iniciando sesión...' : 'Iniciar sesión' }}
              </v-btn>
            </v-form>

            <!-- Footer -->
            <v-divider class="my-6"></v-divider>
            <div class="text-center">
              <p class="text-body-2 text-medium-emphasis mb-2">
                ¿No tienes cuenta?
              </p>
              <v-btn
                to="/registro"
                variant="text"
                color="primary"
                class="text-none"
              >
                Regístrate aquí
              </v-btn>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'
import { getApiUrl } from '../config/api.js'

const router = useRouter()
const correo = ref('')
const contraseña = ref('')
const error = ref('')
const loading = ref(false)

// Reglas de validación
const rules = {
  required: v => !!v || 'Este campo es obligatorio',
  email: v => /.+@.+\..+/.test(v) || 'El correo electrónico no es válido',
  min: v => v.length >= 8 || 'La contraseña debe tener al menos 8 caracteres'
}

const limpiarFormulario = () => {
  correo.value = ''
  contraseña.value = ''
  error.value = ''
}

function traducirError(msg) {
  if (!msg) return 'Error de validación.'
  if (msg.includes('at least 8 characters')) return 'La contraseña debe tener al menos 8 caracteres.'
  if (msg.includes('value is not a valid email address')) return 'El correo electrónico no es válido.'
  if (msg.includes('field required')) return 'Todos los campos son obligatorios.'
  if (msg.includes('at most 100 characters')) return 'El nombre debe tener como máximo 100 caracteres.'
  if (msg.includes('at least 2 characters')) return 'El nombre debe tener al menos 2 caracteres.'
  return msg
}

const login = async () => {
  error.value = ''
  loading.value = true
  
  try {
    const res = await axios.post(getApiUrl('login'), {
      correo: correo.value,
      contraseña: contraseña.value
    })

    const token = res.data.access_token
    const usuario = res.data.usuario

    // Guardar token y datos del usuario
    localStorage.setItem('token', token)
    localStorage.setItem('usuario', JSON.stringify(usuario))

    limpiarFormulario()

    // Redireccionar según el rol
    if (usuario.rol === 'admin') {
      router.push('/admin')
    } else {
      router.push('/productos')
    }
  } catch (err) {
    const data = err.response?.data
    if (Array.isArray(data?.detail)) {
      error.value = 'Correo o contraseña incorrectos.'
    } else if (typeof data?.detail === 'string') {
      error.value = traducirError(data.detail)
    } else if (err.response?.status === 401) {
      error.value = 'Tu cuenta está inactiva. Contacta al administrador.'
    } else {
      error.value = 'Error de conexión con el servidor.'
    }
    limpiarFormulario()
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  background: linear-gradient(135deg, rgb(var(--v-theme-primary)) 0%, rgb(var(--v-theme-secondary)) 100%);
}

.login-card {
  backdrop-filter: blur(10px);
  background: rgba(255, 255, 255, 0.95);
}
</style>
