<template>
  <div class="crear-producto-container">
    <div class="crear-producto-card">
      <div class="card-header">
        <h1 class="card-title">Crear Nuevo Producto</h1>
        <p class="card-subtitle">Agrega un nuevo producto al catálogo</p>
      </div>

      <form @submit.prevent="crearProducto" class="product-form" enctype="multipart/form-data">
        <div class="form-grid">
          <div class="form-group">
            <label for="nombre" class="form-label">Nombre del producto</label>
            <input 
              id="nombre"
              v-model="nombre" 
              type="text" 
              placeholder="Ingresa el nombre del producto" 
              required 
              class="form-input"
            />
          </div>

          <div class="form-group">
            <label for="categoria" class="form-label">Categoría</label>
            <select id="categoria" v-model="categoria_id" class="form-input" required>
              <option value="">Selecciona una categoría</option>
              <option v-for="categoria in categorias" :key="categoria.id" :value="categoria.id">
                {{ categoria.nombre }}
              </option>
            </select>
          </div>

          <div class="form-group">
            <label for="precio" class="form-label">Precio (Q)</label>
            <input 
              id="precio"
              v-model.number="precio" 
              type="number" 
              step="0.01" 
              placeholder="0.00" 
              required 
              class="form-input"
            />
          </div>

          <div class="form-group">
            <label for="stock" class="form-label">Stock disponible</label>
            <input 
              id="stock"
              v-model.number="stock" 
              type="number" 
              placeholder="0" 
              required 
              class="form-input"
            />
          </div>

          <div class="form-group full-width">
            <label for="descripcion" class="form-label">Descripción</label>
            <textarea 
              id="descripcion"
              v-model="descripcion" 
              placeholder="Describe el producto..." 
              required 
              class="form-textarea"
              rows="4"
            ></textarea>
          </div>

          <div class="form-group full-width">
            <label for="imagen" class="form-label">Imagen del producto</label>
            <div class="file-upload">
              <input 
                id="imagen"
                type="file" 
                @change="handleFileChange" 
                accept="image/*" 
                required 
                class="file-input"
              />
              <div class="file-preview">
                <div v-if="!imagenPreview" class="file-placeholder">
                  <svg class="upload-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path>
                  </svg>
                  <span>Haz clic para seleccionar una imagen</span>
                </div>
                <img v-else :src="imagenPreview" alt="Vista previa" class="preview-image" />
              </div>
            </div>
          </div>
        </div>

        <div v-if="mensaje" :class="['mensaje', mensajeTipo]">
          {{ mensaje }}
        </div>

        <div class="form-actions">
          <button type="button" @click="$router.push('/admin')" class="btn btn-outline">
            Cancelar
          </button>
          <button type="submit" class="btn btn-primary" :disabled="loading">
            <div v-if="loading" class="loading-spinner"></div>
            <span v-else>{{ loading ? 'Guardando...' : 'Guardar Producto' }}</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'

const router = useRouter()
const toast = useToast()

const nombre = ref('')
const descripcion = ref('')
const precio = ref(0)
const stock = ref(0)
const categoria_id = ref('')
const imagen = ref(null)
const imagenPreview = ref(null)
const mensaje = ref('')
const mensajeTipo = ref('')
const loading = ref(false)
const categorias = ref([])

onMounted(async () => {
  await cargarCategorias()
})

async function cargarCategorias() {
  try {
    const response = await axios.get('http://localhost:8000/categorias')
    categorias.value = response.data
  } catch (error) {
    console.error('Error al cargar categorías:', error)
    toast.error('Error al cargar las categorías')
  }
}

const handleFileChange = (event) => {
  const file = event.target.files[0]
  if (file) {
    imagen.value = file
    const reader = new FileReader()
    reader.onload = (e) => {
      imagenPreview.value = e.target.result
    }
    reader.readAsDataURL(file)
  }
}

const crearProducto = async () => {
  loading.value = true
  mensaje.value = ''
  mensajeTipo.value = ''
  
  try {
    const usuario = JSON.parse(localStorage.getItem('usuario'))
    if (!usuario) {
      router.push('/login')
      return
    }

    const formData = new FormData()
    formData.append('admin_id', usuario.id)
    formData.append('nombre', nombre.value)
    formData.append('descripcion', descripcion.value)
    formData.append('precio', precio.value)
    formData.append('stock', stock.value)
    if (categoria_id.value) {
      formData.append('categoria_id', categoria_id.value)
    }
    if (imagen.value) {
      formData.append('imagen', imagen.value)
    }

    const res = await axios.post('http://localhost:8000/productos/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })

    mensaje.value = 'Producto creado exitosamente.'
    mensajeTipo.value = 'success'
    toast.success('Producto creado exitosamente')
    
    setTimeout(() => {
      router.push('/admin')
    }, 1500)
    
    limpiarFormulario()
  } catch (error) {
    console.error('Error al crear producto:', error)
    mensaje.value = error.response?.data?.detail || 'Error al crear producto.'
    mensajeTipo.value = 'error'
    toast.error('Error al crear el producto')
  } finally {
    loading.value = false
  }
}

const limpiarFormulario = () => {
  nombre.value = ''
  descripcion.value = ''
  precio.value = 0
  stock.value = 0
  categoria_id.value = ''
  imagen.value = null
  imagenPreview.value = null
}
</script>

<style scoped>
.crear-producto-container {
  max-width: 800px;
  margin: 0 auto;
  padding: var(--spacing-xl);
}

.crear-producto-card {
  background: var(--bg-primary);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-lg);
  padding: var(--spacing-2xl);
}

.card-header {
  text-align: center;
  margin-bottom: var(--spacing-2xl);
}

.card-title {
  font-size: var(--font-size-3xl);
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: var(--spacing-sm);
}

.card-subtitle {
  color: var(--text-secondary);
  font-size: var(--font-size-base);
}

.product-form {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xl);
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--spacing-lg);
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.form-group.full-width {
  grid-column: 1 / -1;
}

.form-label {
  font-weight: 500;
  color: var(--text-primary);
  font-size: var(--font-size-sm);
}

.form-input,
.form-textarea {
  padding: var(--spacing-md);
  border: 2px solid var(--border-color);
  border-radius: var(--border-radius);
  background: var(--bg-primary);
  font-size: var(--font-size-base);
  transition: all var(--transition-fast);
}

.form-input:focus,
.form-textarea:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgb(37 99 235 / 0.1);
}

.form-textarea {
  resize: vertical;
  min-height: 100px;
}

.file-upload {
  position: relative;
}

.file-input {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0;
  cursor: pointer;
}

.file-preview {
  border: 2px dashed var(--border-color);
  border-radius: var(--border-radius);
  padding: var(--spacing-xl);
  text-align: center;
  transition: all var(--transition-fast);
  min-height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.file-preview:hover {
  border-color: var(--primary-color);
  background: var(--bg-secondary);
}

.file-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-md);
  color: var(--text-muted);
}

.upload-icon {
  width: 48px;
  height: 48px;
  color: var(--text-muted);
}

.preview-image {
  max-width: 100%;
  max-height: 300px;
  border-radius: var(--border-radius);
  object-fit: cover;
}

.mensaje {
  padding: var(--spacing-md);
  border-radius: var(--border-radius);
  font-weight: 500;
}

.mensaje.success {
  background: rgb(16 185 129 / 0.1);
  color: var(--success-color);
  border: 1px solid rgb(16 185 129 / 0.2);
}

.mensaje.error {
  background: rgb(239 68 68 / 0.1);
  color: var(--error-color);
  border: 1px solid rgb(239 68 68 / 0.2);
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: var(--spacing-md);
  padding-top: var(--spacing-lg);
  border-top: 1px solid var(--border-color);
}

.loading-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top: 2px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Responsive */
@media (max-width: 768px) {
  .crear-producto-container {
    padding: var(--spacing-md);
  }
  
  .crear-producto-card {
    padding: var(--spacing-lg);
  }
  
  .form-grid {
    grid-template-columns: 1fr;
  }
  
  .form-actions {
    flex-direction: column;
  }
  
  .card-title {
    font-size: var(--font-size-xl);
  }
}
</style>
