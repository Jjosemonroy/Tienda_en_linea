<template>
  <v-container fluid class="registro-container fill-height">
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="6" lg="4">
        <v-card class="registro-card" elevation="8" rounded="xl">
          <v-card-text class="text-center pa-8">
            <!-- Header -->
            <div class="mb-8">
              <v-avatar
                size="80"
                color="primary"
                class="mb-4"
              >
                <v-icon size="40" color="white">mdi-account-plus</v-icon>
              </v-avatar>
              <h1 class="text-h4 font-weight-bold text-primary mb-2">
                Crear cuenta
              </h1>
              <p class="text-body-1 text-medium-emphasis">
                Únete a nuestra comunidad
              </p>
            </div>

            <!-- Formulario -->
            <v-form @submit.prevent="registrar">
              <v-text-field
                v-model="nombre"
                label="Nombre completo"
                type="text"
                placeholder="Tu nombre completo"
                prepend-inner-icon="mdi-account"
                variant="outlined"
                rounded="lg"
                required
                class="mb-4"
                :rules="[rules.required, rules.minLength]"
              ></v-text-field>

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
                placeholder="Mínimo 8 caracteres"
                prepend-inner-icon="mdi-lock"
                variant="outlined"
                rounded="lg"
                required
                minlength="8"
                class="mb-6"
                :rules="[rules.required, rules.minLength]"
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

              <!-- Mensaje de éxito -->
              <v-alert
                v-if="exito"
                type="success"
                variant="tonal"
                class="mb-6"
                :text="exito"
                closable
                @click:close="exito = ''"
              ></v-alert>

              <!-- Botón de registro -->
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
                <v-icon start>mdi-account-plus</v-icon>
                {{ loading ? 'Creando cuenta...' : 'Crear cuenta' }}
              </v-btn>
            </v-form>

            <!-- Footer -->
            <v-divider class="my-6"></v-divider>
            <div class="text-center">
              <p class="text-body-2 text-medium-emphasis mb-2">
                ¿Ya tienes cuenta?
              </p>
              <v-btn
                to="/"
                variant="text"
                color="primary"
                class="text-none"
              >
                Inicia sesión
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
const nombre = ref('')
const correo = ref('')
const contraseña = ref('')
const error = ref('')
const exito = ref('')
const loading = ref(false)

// Reglas de validación
const rules = {
  required: v => !!v || 'Este campo es obligatorio',
  email: v => /.+@.+\..+/.test(v) || 'El correo electrónico no es válido',
  minLength: v => v.length >= 2 || 'Debe tener al menos 2 caracteres'
}

const registrar = async () => {
  error.value = ''
  exito.value = ''
  loading.value = true

  // Validación básica en frontend
  if (nombre.value.length < 2) {
    error.value = 'El nombre debe tener al menos 2 caracteres.'
    loading.value = false
    return
  }
  if (!correo.value.includes('@')) {
    error.value = 'Correo electrónico inválido.'
    loading.value = false
    return
  }
  if (contraseña.value.length < 8) {
    error.value = 'La contraseña debe tener al menos 8 caracteres.'
    loading.value = false
    return
  }

  try {
    await axios.post(getApiUrl('register'), {
      nombre: nombre.value,
      correo: correo.value,
      contraseña: contraseña.value
    })
    exito.value = '¡Registro exitoso! Redirigiendo al login...'
    setTimeout(() => router.push('/'), 2000)
  } catch (err) {
    error.value = err.response?.data?.detail || 'Error al registrar usuario.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.registro-container {
  background: linear-gradient(135deg, rgb(var(--v-theme-primary)) 0%, rgb(var(--v-theme-secondary)) 100%);
}

.registro-card {
  backdrop-filter: blur(10px);
  background: rgba(255, 255, 255, 0.95);
}
</style> 