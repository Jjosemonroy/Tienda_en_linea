<template>
  <div class="perfil-container">
    <!-- Header del perfil -->
    <div class="perfil-header glass-card">
      <div class="header-content">
        <div class="header-title">
          <div class="header-icon-container">
            <svg class="header-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
            </svg>
          </div>
          <h1>Mi Perfil</h1>
        </div>
        <button @click="volver" class="btn-volver">
          <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path>
          </svg>
          Volver
        </button>
      </div>
    </div>

    <!-- Contenido del perfil -->
    <div class="perfil-content">
      <!-- Información del usuario -->
      <div class="profile-card glass-card">
        <div class="card-header">
          <div class="user-avatar">
            {{ usuario?.nombre?.charAt(0).toUpperCase() || 'U' }}
          </div>
          <div class="user-info">
            <h2>{{ usuario?.nombre || 'Usuario' }}</h2>
            <p class="user-email">{{ usuario?.correo || 'usuario@ejemplo.com' }}</p>
            <div class="user-badges">
              <span class="badge badge-role">{{ usuario?.rol || 'Cliente' }}</span>
              <span class="badge badge-status" :class="usuario?.estado || 'activo'">
                {{ usuario?.estado === 'activo' ? 'Activo' : 'Inactivo' }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Formulario de datos personales -->
      <div class="profile-card glass-card">
        <div class="card-header">
          <h3>
            <svg class="card-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
            </svg>
            Datos Personales
          </h3>
        </div>
        
        <form @submit.prevent="guardarCambios" class="profile-form">
          <div class="form-group">
            <label for="nombre">Nombre</label>
            <input 
              id="nombre"
              v-model="nombre" 
              type="text" 
              required 
              minlength="2" 
              maxlength="100"
              class="input-elegant"
              :class="{ 'error': error && error.includes('nombre') }"
              placeholder="Tu nombre completo"
            />
          </div>
          
          <div class="form-group">
            <label for="correo">Correo Electrónico</label>
            <input 
              id="correo"
              v-model="correo" 
              type="email" 
              required 
              class="input-elegant"
              :class="{ 'error': error && error.includes('correo') }"
              placeholder="tu@email.com"
            />
          </div>
          
          <div class="form-actions">
            <button type="submit" class="btn btn-primary" :disabled="loading">
              <div v-if="loading" class="loading-spinner"></div>
              <span v-else>Guardar Cambios</span>
            </button>
          </div>
          
          <div v-if="exito" class="success-message">
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
            </svg>
            {{ exito }}
          </div>
          <div v-if="error" class="error-message">
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
            {{ error }}
          </div>
        </form>
      </div>

      <!-- Formulario de cambio de contraseña -->
      <div class="profile-card glass-card">
        <div class="card-header">
          <h3>
            <svg class="card-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z"></path>
            </svg>
            Cambiar Contraseña
          </h3>
        </div>
        
        <form @submit.prevent="cambiarPassword" class="profile-form">
          <div class="form-group">
            <label for="actual">Contraseña Actual</label>
            <input 
              id="actual"
              v-model="actual" 
              type="password" 
              required 
              class="input-elegant"
              placeholder="Tu contraseña actual"
            />
          </div>
          
          <div class="form-group">
            <label for="nueva">Nueva Contraseña</label>
            <input 
              id="nueva"
              v-model="nueva" 
              type="password" 
              required 
              minlength="8"
              class="input-elegant"
              placeholder="Mínimo 8 caracteres"
            />
          </div>
          
          <div class="form-group">
            <label for="confirmar">Confirmar Nueva Contraseña</label>
            <input 
              id="confirmar"
              v-model="confirmar" 
              type="password" 
              required 
              minlength="8"
              class="input-elegant"
              :class="{ 'error': errorPass && errorPass.includes('coinciden') }"
              placeholder="Confirma tu nueva contraseña"
            />
          </div>
          
          <div class="form-actions">
            <button type="submit" class="btn btn-warning" :disabled="loadingPass">
              <div v-if="loadingPass" class="loading-spinner"></div>
              <span v-else>Actualizar Contraseña</span>
            </button>
          </div>
          
          <div v-if="exitoPass" class="success-message">
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
            </svg>
            {{ exitoPass }}
          </div>
          <div v-if="errorPass" class="error-message">
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
            {{ errorPass }}
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'
import { getApiUrl } from '../config/api.js'

const router = useRouter()
const toast = useToast()

const usuario = ref(JSON.parse(localStorage.getItem('usuario')))
const nombre = ref(usuario.value?.nombre || '')
const correo = ref(usuario.value?.correo || '')
const exito = ref('')
const error = ref('')
const loading = ref(false)

const actual = ref('')
const nueva = ref('')
const confirmar = ref('')
const exitoPass = ref('')
const errorPass = ref('')
const loadingPass = ref(false)

onMounted(() => {
  // Verificar que el usuario esté logueado
  if (!usuario.value) {
    router.push('/')
    return
  }
})

const guardarCambios = async () => {
  exito.value = ''
  error.value = ''
  loading.value = true
  
  // Validaciones
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
  
  try {
    const token = localStorage.getItem('token')
    const response = await axios.put(getApiUrl('updateProfile'), {
      nombre: nombre.value,
      correo: correo.value
    }, {
      headers: { Authorization: `Bearer ${token}` }
    })
    
    // Actualizar datos del usuario en localStorage
    usuario.value.nombre = response.data.usuario.nombre
    usuario.value.correo = response.data.usuario.correo
    localStorage.setItem('usuario', JSON.stringify(usuario.value))
    
    exito.value = 'Datos actualizados exitosamente.'
    toast.success('Datos actualizados exitosamente')
  } catch (err) {
    console.error('Error al actualizar datos:', err)
    if (err.response?.status === 400) {
      error.value = err.response.data.detail || 'Error al actualizar datos.'
    } else if (err.response?.status === 401) {
      error.value = 'Sesión expirada. Por favor, inicia sesión nuevamente.'
      router.push('/')
    } else {
      error.value = 'Error al actualizar datos. Inténtalo de nuevo.'
    }
    toast.error(error.value)
  } finally {
    loading.value = false
  }
}

const cambiarPassword = async () => {
  exitoPass.value = ''
  errorPass.value = ''
  loadingPass.value = true
  
  if (nueva.value !== confirmar.value) {
    errorPass.value = 'Las contraseñas no coinciden.'
    loadingPass.value = false
    return
  }
  if (nueva.value.length < 8) {
    errorPass.value = 'La nueva contraseña debe tener al menos 8 caracteres.'
    loadingPass.value = false
    return
  }
  
  try {
    await axios.put(getApiUrl('changePassword'), {
      correo: usuario.value.correo,
      contraseña_actual: actual.value,
      nueva_contraseña: nueva.value
    })
    
    exitoPass.value = 'Contraseña actualizada correctamente.'
    toast.success('Contraseña actualizada correctamente')
    actual.value = ''
    nueva.value = ''
    confirmar.value = ''
  } catch (err) {
    console.error('Error al cambiar contraseña:', err)
    if (err.response?.status === 401) {
      errorPass.value = 'Contraseña actual incorrecta.'
    } else if (err.response?.status === 400) {
      errorPass.value = err.response.data.detail || 'Error al cambiar contraseña.'
    } else {
      errorPass.value = 'Error al cambiar contraseña. Inténtalo de nuevo.'
    }
    toast.error(errorPass.value)
  } finally {
    loadingPass.value = false
  }
}

function volver() {
  if (usuario.value?.rol === 'admin') {
    router.push('/admin')
  } else {
    router.push('/productos')
  }
}
</script>

<style scoped>
.perfil-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: var(--spacing-xl);
  min-height: 100vh;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
}

.perfil-header {
  background: var(--glass-bg);
  backdrop-filter: var(--glass-blur-strong);
  border: 1px solid var(--glass-border);
  border-radius: var(--border-radius-2xl);
  padding: var(--spacing-2xl);
  margin-bottom: var(--spacing-xl);
  box-shadow: var(--shadow-2xl);
  transition: all var(--transition-smooth);
}

.perfil-header:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-2xl), var(--shadow-glow);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-title {
  display: flex;
  align-items: center;
  gap: var(--spacing-lg);
}

.header-icon-container {
  width: 64px;
  height: 64px;
  background: var(--gradient-neon-purple);
  border-radius: var(--border-radius-xl);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: var(--shadow-xl), var(--shadow-glow-purple);
  transition: all var(--transition-smooth);
}

.header-icon-container:hover {
  transform: scale(1.1) rotate(5deg);
  box-shadow: var(--shadow-2xl), var(--shadow-glow-purple);
}

.header-icon {
  width: 32px;
  height: 32px;
  color: var(--text-light);
}

.header-title h1 {
  margin: 0;
  font-size: var(--font-size-4xl);
  font-weight: 800;
  background: var(--gradient-neon-purple);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: -0.025em;
}

.btn-volver {
  background: var(--glass-bg);
  backdrop-filter: var(--glass-blur);
  color: var(--text-primary);
  border: 1px solid var(--border-color-light);
  padding: var(--spacing-md) var(--spacing-lg);
  border-radius: var(--border-radius-lg);
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  font-size: var(--font-size-sm);
  font-weight: 600;
  transition: all var(--transition-smooth);
  box-shadow: var(--shadow-sm);
}

.btn-volver:hover {
  background: var(--bg-secondary);
  border-color: var(--neon-blue);
  box-shadow: var(--shadow-lg);
  transform: translateY(-2px);
}

.btn-volver svg {
  width: 20px;
  height: 20px;
}

.perfil-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: var(--spacing-xl);
}

.profile-card {
  background: var(--glass-bg);
  backdrop-filter: var(--glass-blur-strong);
  border: 1px solid var(--glass-border);
  border-radius: var(--border-radius-2xl);
  padding: var(--spacing-2xl);
  box-shadow: var(--shadow-xl);
  transition: all var(--transition-smooth);
}

.profile-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-2xl), var(--shadow-glow);
}

.card-header {
  display: flex;
  align-items: center;
  gap: var(--spacing-lg);
  margin-bottom: var(--spacing-xl);
  padding-bottom: var(--spacing-lg);
  border-bottom: 1px solid var(--border-color-light);
}

.card-header h3 {
  margin: 0;
  font-size: var(--font-size-2xl);
  font-weight: 700;
  color: var(--text-primary);
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.card-icon {
  width: 32px;
  height: 32px;
  color: var(--neon-blue);
}

.user-avatar {
  width: 80px;
  height: 80px;
  background: var(--gradient-neon-purple);
  border-radius: var(--border-radius-full);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: var(--font-size-3xl);
  font-weight: 800;
  color: var(--text-light);
  box-shadow: var(--shadow-lg), var(--shadow-glow-purple);
}

.user-info h2 {
  margin: 0 0 var(--spacing-sm) 0;
  font-size: var(--font-size-2xl);
  font-weight: 700;
  color: var(--text-primary);
}

.user-email {
  font-size: var(--font-size-base);
  color: var(--text-secondary);
  margin-bottom: var(--spacing-md);
}

.user-badges {
  display: flex;
  gap: var(--spacing-sm);
}

.badge {
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--border-radius-full);
  font-size: var(--font-size-sm);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.badge-role {
  background: var(--gradient-neon-blue);
  color: var(--text-light);
  box-shadow: var(--shadow-sm);
}

.badge-status.activo {
  background: var(--gradient-neon-green);
  color: var(--text-light);
  box-shadow: var(--shadow-sm);
}

.badge-status.inactivo {
  background: var(--gradient-neon-pink);
  color: var(--text-light);
  box-shadow: var(--shadow-sm);
}

.profile-form {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.form-group label {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.input-elegant {
  padding: var(--spacing-md) var(--spacing-lg);
  font-size: var(--font-size-base);
  border: 2px solid var(--border-color-light);
  border-radius: var(--border-radius-lg);
  background: var(--glass-bg);
  backdrop-filter: var(--glass-blur);
  color: var(--text-primary);
  transition: all var(--transition-smooth);
  box-shadow: var(--shadow-sm);
}

.input-elegant:focus {
  outline: none;
  border-color: var(--neon-blue);
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1), var(--shadow-lg);
  transform: translateY(-1px);
}

.input-elegant.error {
  border-color: var(--error-color);
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1);
}

.input-elegant::placeholder {
  color: var(--text-muted);
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: var(--spacing-lg);
}

.btn {
  padding: var(--spacing-md) var(--spacing-xl);
  font-size: var(--font-size-sm);
  font-weight: 600;
  border-radius: var(--border-radius-lg);
  cursor: pointer;
  transition: all var(--transition-smooth);
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  min-width: 140px;
  justify-content: center;
}

.btn-primary {
  background: var(--gradient-neon-blue);
  color: var(--text-light);
  border: none;
  box-shadow: var(--shadow-md);
}

.btn-primary:hover:not(:disabled) {
  background: var(--gradient-neon-blue);
  box-shadow: var(--shadow-lg), 0 0 20px rgba(59, 130, 246, 0.4);
  transform: translateY(-2px);
}

.btn-primary:disabled {
  background: var(--bg-secondary);
  cursor: not-allowed;
  color: var(--text-muted);
  transform: none;
  box-shadow: var(--shadow-sm);
}

.btn-warning {
  background: var(--gradient-neon-orange);
  color: var(--text-light);
  border: none;
  box-shadow: var(--shadow-md);
}

.btn-warning:hover:not(:disabled) {
  background: var(--gradient-neon-orange);
  box-shadow: var(--shadow-lg), 0 0 20px rgba(245, 158, 11, 0.4);
  transform: translateY(-2px);
}

.btn-warning:disabled {
  background: var(--bg-secondary);
  cursor: not-allowed;
  color: var(--text-muted);
  transform: none;
  box-shadow: var(--shadow-sm);
}

.loading-spinner {
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-top: 3px solid var(--neon-blue);
  border-radius: 50%;
  width: 20px;
  height: 20px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.success-message, .error-message {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  margin-top: var(--spacing-md);
  padding: var(--spacing-md) var(--spacing-lg);
  border-radius: var(--border-radius-lg);
  font-size: var(--font-size-sm);
  font-weight: 600;
  box-shadow: var(--shadow-sm);
}

.success-message {
  background: var(--gradient-neon-green);
  color: var(--text-light);
}

.error-message {
  background: var(--gradient-neon-pink);
  color: var(--text-light);
}

.success-message svg, .error-message svg {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
}

/* Responsive */
@media (max-width: 768px) {
  .perfil-container {
    padding: var(--spacing-md);
  }
  
  .perfil-content {
    grid-template-columns: 1fr;
  }
  
  .header-content {
    flex-direction: column;
    gap: var(--spacing-lg);
    text-align: center;
  }
  
  .card-header {
    flex-direction: column;
    text-align: center;
    gap: var(--spacing-md);
  }
  
  .user-badges {
    justify-content: center;
  }
}
</style> 