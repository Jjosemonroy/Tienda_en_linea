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
    const token = localStorage.getItem('token')
    const response = await axios.get('http://localhost:8000/categorias', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
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
    const token = localStorage.getItem('token')
    
    if (!usuario || !token) {
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
        'Content-Type': 'multipart/form-data',
        'Authorization': `Bearer ${token}`
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
  max-width: 900px;
  margin: 0 auto;
  padding: var(--spacing-xl);
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
  min-height: 100vh;
}

.crear-producto-card {
  background: #ffffff;
  border-radius: var(--border-radius-xl);
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  padding: var(--spacing-2xl);
  border: 1px solid #e2e8f0;
}

.card-header {
  text-align: center;
  margin-bottom: var(--spacing-2xl);
  padding-bottom: var(--spacing-lg);
  border-bottom: 2px solid var(--border-color-light);
}

.card-title {
  font-size: var(--font-size-3xl);
  font-weight: 700;
  color: #1e293b;
  margin-bottom: var(--spacing-sm);
}

.card-subtitle {
  color: #64748b;
  font-size: var(--font-size-lg);
  font-weight: 400;
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
  font-weight: 600;
  color: #1e293b;
  font-size: var(--font-size-sm);
  margin-bottom: var(--spacing-xs);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.form-input,
.form-textarea {
  padding: var(--spacing-md) var(--spacing-lg);
  border: 2px solid #e2e8f0;
  border-radius: var(--border-radius-lg);
  background: #ffffff;
  font-size: var(--font-size-base);
  transition: all var(--transition-normal);
  color: #1e293b;
  font-weight: 500;
}

.form-input::placeholder,
.form-textarea::placeholder {
  color: #64748b;
  font-weight: 400;
}

.form-input:focus,
.form-textarea:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1);
  background: #ffffff;
  transform: translateY(-1px);
}

.form-textarea {
  resize: vertical;
  min-height: 120px;
  font-family: inherit;
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
  z-index: 2;
}

.file-preview {
  border: 3px dashed #e2e8f0;
  border-radius: var(--border-radius-lg);
  padding: var(--spacing-2xl);
  text-align: center;
  transition: all var(--transition-normal);
  min-height: 220px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f8fafc;
  position: relative;
  overflow: hidden;
}

.file-preview::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(45deg, transparent 30%, rgba(102, 126, 234, 0.05) 50%, transparent 70%);
  opacity: 0;
  transition: opacity var(--transition-normal);
}

.file-preview:hover {
  border-color: #667eea;
  background: rgba(102, 126, 234, 0.05);
  transform: translateY(-2px);
  box-shadow: 0 10px 25px -5px rgba(102, 126, 234, 0.1);
}

.file-preview:hover::before {
  opacity: 1;
}

.file-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-lg);
  color: #64748b;
  font-weight: 500;
}

.upload-icon {
  width: 64px;
  height: 64px;
  color: #667eea;
  opacity: 0.7;
  transition: all var(--transition-normal);
}

.file-preview:hover .upload-icon {
  opacity: 1;
  transform: scale(1.1);
}

.preview-image {
  max-width: 100%;
  max-height: 300px;
  border-radius: var(--border-radius-lg);
  object-fit: cover;
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
}

.mensaje {
  padding: var(--spacing-lg);
  border-radius: var(--border-radius-lg);
  font-weight: 600;
  text-align: center;
  margin: var(--spacing-lg) 0;
}

.mensaje.success {
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(16, 185, 129, 0.05) 100%);
  color: #059669;
  border: 2px solid rgba(16, 185, 129, 0.2);
}

.mensaje.error {
  background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(239, 68, 68, 0.05) 100%);
  color: #dc2626;
  border: 2px solid rgba(239, 68, 68, 0.2);
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: var(--spacing-lg);
  padding-top: var(--spacing-xl);
  border-top: 2px solid var(--border-color-light);
  margin-top: var(--spacing-lg);
}

/* Estilos de botones mejorados */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-md) var(--spacing-xl);
  border: none;
  border-radius: var(--border-radius-lg);
  font-size: var(--font-size-base);
  font-weight: 600;
  text-decoration: none;
  cursor: pointer;
  transition: all var(--transition-normal);
  position: relative;
  overflow: hidden;
  min-width: 140px;
}

.btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left var(--transition-smooth);
}

.btn:hover::before {
  left: 100%;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  box-shadow: 0 4px 14px rgba(102, 126, 234, 0.4);
}

.btn-primary:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
}

.btn-primary:active {
  transform: translateY(-1px);
}

.btn-primary:disabled {
  background: #cbd5e0;
  color: #a0aec0;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.btn-outline {
  background: transparent;
  color: #667eea;
  border: 2px solid #667eea;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.1);
}

.btn-outline:hover {
  background: #667eea;
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.3);
}

.btn-outline:active {
  transform: translateY(0);
}

.loading-spinner {
  width: 18px;
  height: 18px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top: 2px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Efectos de focus para accesibilidad */
.btn:focus,
.form-input:focus,
.form-textarea:focus,
.file-preview:focus-within {
  outline: 2px solid #667eea;
  outline-offset: 2px;
}

/* Responsive */
@media (max-width: 768px) {
  .crear-producto-container {
    padding: var(--spacing-md);
    background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
  }
  
  .crear-producto-card {
    padding: var(--spacing-lg);
    margin: var(--spacing-sm);
  }
  
  .form-grid {
    grid-template-columns: 1fr;
    gap: var(--spacing-md);
  }
  
  .form-actions {
    flex-direction: column;
    gap: var(--spacing-md);
  }
  
  .btn {
    width: 100%;
    justify-content: center;
  }
  
  .card-title {
    font-size: var(--font-size-2xl);
  }
  
  .file-preview {
    min-height: 180px;
    padding: var(--spacing-lg);
  }
  
  .upload-icon {
    width: 48px;
    height: 48px;
  }
}

@media (max-width: 480px) {
  .crear-producto-container {
    padding: var(--spacing-sm);
  }
  
  .crear-producto-card {
    padding: var(--spacing-md);
    margin: 0;
  }
  
  .card-title {
    font-size: var(--font-size-xl);
  }
  
  .form-input,
  .form-textarea {
    padding: var(--spacing-sm) var(--spacing-md);
  }
}
</style>
