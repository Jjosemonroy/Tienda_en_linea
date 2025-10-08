<template>
  <div class="admin-container">
    <!-- Header del admin -->
    <div class="admin-header">
      <div class="header-content">
        <div class="header-title">
          <div class="header-icon-container">
            <svg class="header-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path>
            </svg>
          </div>
          <h1>Panel de Administración</h1>
        </div>
        <div class="header-actions">
          <div class="admin-info">
            <span class="admin-name">{{ usuario?.nombre }}</span>
            <span class="admin-role">{{ usuario?.rol }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Estadísticas -->
    <div class="stats-grid">
      <div class="stat-card" style="animation-delay: 0.1s;">
        <div class="stat-icon">
          <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"></path>
          </svg>
        </div>
        <div class="stat-content">
          <h3 class="stat-number">{{ stats.totalProductos }}</h3>
          <p class="stat-label">Productos</p>
        </div>
      </div>

      <div class="stat-card" style="animation-delay: 0.2s;">
        <div class="stat-icon">
          <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-6a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z"></path>
          </svg>
        </div>
        <div class="stat-content">
          <h3 class="stat-number">{{ stats.totalUsuarios }}</h3>
          <p class="stat-label">Usuarios</p>
        </div>
      </div>

      <div class="stat-card" style="animation-delay: 0.3s;">
        <div class="stat-icon">
          <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
          </svg>
        </div>
        <div class="stat-content">
          <h3 class="stat-number">{{ stats.totalVentas }}</h3>
          <p class="stat-label">Ventas</p>
        </div>
      </div>

      <div class="stat-card" style="animation-delay: 0.4s;">
        <div class="stat-icon">
          <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1"></path>
          </svg>
        </div>
        <div class="stat-content">
          <h3 class="stat-number">Q{{ stats.ingresosTotales.toFixed(2) }}</h3>
          <p class="stat-label">Ingresos</p>
        </div>
      </div>
    </div>

    <!-- Navegación del admin -->
    <div class="admin-nav">
      <button 
        v-for="tab in tabs" 
        :key="tab.id"
        @click="activeTab = tab.id"
        :class="['nav-tab', { active: activeTab === tab.id }]"
      >
        <svg class="tab-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="tab.icon"></path>
        </svg>
        {{ tab.name }}
      </button>
    </div>

    <!-- Contenido del admin -->
    <div class="admin-content">
      <!-- Dashboard -->
      <div v-if="activeTab === 'dashboard'" class="tab-content">
        <div class="dashboard-grid">
          <div class="dashboard-card">
            <h3>Productos recientes</h3>
            <div class="recent-items">
              <div v-for="producto in productosRecientes" :key="producto.id" class="recent-item">
                <img v-if="producto.imagen" :src="getImageUrl(producto.imagen)" :alt="producto.nombre" class="item-image" />
                <div v-else class="item-image-placeholder">Sin imagen</div>
                <div class="item-info">
                  <h4>{{ producto.nombre }}</h4>
                  <p>Q{{ typeof producto.precio === 'number' ? producto.precio.toFixed(2) : parseFloat(producto.precio || 0).toFixed(2) }}</p>
                </div>
              </div>
            </div>
          </div>

          <div class="dashboard-card">
            <h3>Ventas recientes</h3>
            <div class="recent-sales">
              <div v-for="venta in ventasRecientes" :key="venta.id" class="sale-item">
                <div class="sale-info">
                  <h4>Venta #{{ venta.id }}</h4>
                  <p>{{ venta.fecha }}</p>
                </div>
                <div class="sale-amount">
                  Q{{ typeof venta.total === 'number' ? venta.total.toFixed(2) : parseFloat(venta.total || 0).toFixed(2) }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Gestión de Productos -->
      <div v-if="activeTab === 'productos'" class="tab-content">
        <div class="section-header">
          <h2>Gestión de Productos</h2>
          <button @click="showCreateModal = true" class="btn btn-primary">
            <svg class="btn-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
            </svg>
            Nuevo Producto
          </button>
        </div>

        <div class="products-table">
          <table>
            <thead>
              <tr>
                <th>Imagen</th>
                <th>Nombre</th>
                <th>Precio</th>
                <th>Stock</th>
                <th>Categoría</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="producto in productos" :key="producto.id">
                <td>
                  <div class="image-container">
                    <img 
                      v-if="producto.imagen && getSimpleImageUrl(producto.imagen)" 
                      :src="getSimpleImageUrl(producto.imagen)" 
                      :alt="producto.nombre" 
                      class="product-thumb"
                    />
                    <div v-else class="no-image">
                      <v-icon size="24" color="grey">mdi-image-off</v-icon>
                      <span>Sin imagen</span>
                    </div>
                  </div>
                </td>
                <td>{{ producto.nombre }}</td>
                <td>Q{{ typeof producto.precio === 'number' ? producto.precio.toFixed(2) : parseFloat(producto.precio || 0).toFixed(2) }}</td>
                <td>
                  <span :class="['stock-badge', { 'low-stock': (producto.stock || 0) < 10 }]">
                    {{ producto.stock || 0 }}
                  </span>
                </td>
                <td>{{ producto.categoria?.nombre || 'Sin categoría' }}</td>
                <td>
                  <div class="action-buttons">
                    <button @click="editarProducto(producto)" class="btn btn-sm btn-outline">
                      <svg class="btn-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
                      </svg>
                    </button>
                    <button @click="eliminarProducto(producto.id)" class="btn btn-sm btn-error">
                      <svg class="btn-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                      </svg>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Gestión de Usuarios -->
      <div v-if="activeTab === 'usuarios'" class="tab-content">
        <div class="section-header">
          <h2>Gestión de Usuarios</h2>
        </div>

        <div class="users-table">
          <table>
            <thead>
              <tr>
                <th>Nombre</th>
                <th>Email</th>
                <th>Rol</th>
                <th>Estado</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="user in usuarios" :key="user.id">
                <td>{{ user.nombre }}</td>
                <td>{{ user.correo }}</td>
                <td>
                  <select 
                    v-model="user.rol" 
                    @change="cambiarRolUsuario(user)"
                    class="role-dropdown"
                    :class="{ 'disabled': user.id === usuario?.id }"
                    :disabled="user.id === usuario?.id"
                    :title="user.id === usuario?.id ? 'No puedes cambiar tu propio rol' : 'Cambiar rol del usuario'"
                  >
                    <option value="cliente">Cliente</option>
                    <option value="admin">Admin</option>
                  </select>
                </td>
                <td>
                  <span :class="['status-badge', (user.estado || 'activo') === 'activo' ? 'active' : 'inactive']">
                    {{ (user.estado || 'activo') === 'activo' ? 'Activo' : 'Inactivo' }}
                  </span>
                </td>
                <td>
                  <div class="action-buttons">
                    <button @click="toggleUserStatus(user)" class="btn btn-sm btn-outline">
                      {{ (user.estado || 'activo') === 'activo' ? 'Desactivar' : 'Activar' }}
                    </button>
                    <button @click="mostrarModalRestablecerContraseña(user)" class="btn btn-sm btn-warning">
                      <svg class="btn-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z"></path>
                      </svg>
                      Restablecer Contraseña
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Ventas -->
      <div v-if="activeTab === 'ventas'" class="tab-content">
        <div class="section-header">
          <h2>Historial de Ventas</h2>
        </div>

        <div class="sales-table">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Cliente</th>
                <th>Productos</th>
                <th>Total</th>
                <th>Fecha</th>
                <th>Estado</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="venta in ventas" :key="venta.id">
                <td>#{{ venta.id }}</td>
                <td>{{ venta.usuario && venta.usuario.nombre ? venta.usuario.nombre : 'N/A' }}</td>
                <td>{{ (venta.productos && venta.productos.length) || 0 }} productos</td>
                <td>Q{{ typeof venta.total === 'number' ? venta.total.toFixed(2) : parseFloat(venta.total || 0).toFixed(2) }}</td>
                <td>{{ venta.fecha ? new Date(venta.fecha).toLocaleDateString() : 'N/A' }}</td>
                <td>
                  <span class="status-badge active">Completada</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Gestión de Categorías -->
      <div v-if="activeTab === 'categorias'" class="tab-content">
        <div class="section-header">
          <h2>Gestión de Categorías</h2>
          <button @click="showCategoryModal = true" class="btn btn-primary">
            <svg class="btn-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
            </svg>
            Nueva Categoría
          </button>
        </div>

        <div class="categories-grid">
          <div v-for="categoria in categorias" :key="categoria.id" class="category-card">
            <div class="category-header">
              <h3>{{ categoria.nombre }}</h3>
              <div class="category-actions">
                <button @click="editarCategoria(categoria)" class="btn btn-sm btn-outline">
                  <svg class="btn-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
                  </svg>
                </button>
                <button @click="eliminarCategoria(categoria.id)" class="btn btn-sm btn-error">
                  <svg class="btn-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                  </svg>
                </button>
              </div>
            </div>
            <div class="category-stats">
              <span class="stat-item">
                <strong>{{ (categoria.productos && categoria.productos.length) || 0 }}</strong> productos
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal para crear/editar producto -->
    <div v-if="showCreateModal" class="modal-overlay" @click="showCreateModal = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ editingProduct ? 'Editar' : 'Crear' }} Producto</h3>
          <button @click="showCreateModal = false" class="modal-close">
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>
        
        <form @submit.prevent="guardarProducto" class="product-form">
          <div class="form-group">
            <label for="nombre">Nombre</label>
            <input id="nombre" v-model="productForm.nombre" type="text" required />
          </div>
          
          <div class="form-group">
            <label for="descripcion">Descripción</label>
            <textarea id="descripcion" v-model="productForm.descripcion" required></textarea>
          </div>
          
          <div class="form-row">
            <div class="form-group">
              <label for="precio">Precio</label>
              <input id="precio" v-model.number="productForm.precio" type="number" step="0.01" required />
            </div>
            
            <div class="form-group">
              <label for="stock">Stock</label>
              <input id="stock" v-model.number="productForm.stock" type="number" required />
            </div>
          </div>
          
          <div class="form-group">
            <label for="categoria">Categoría</label>
            <select id="categoria" v-model="productForm.categoria_id">
              <option value="">Seleccionar categoría</option>
              <option v-for="cat in categorias" :key="cat.id" :value="cat.id">
                {{ cat.nombre }}
              </option>
            </select>
          </div>
          
          <div class="form-group">
            <label for="imagen">Imagen</label>
            <input id="imagen" type="file" @change="handleImageChange" accept="image/*" />
          </div>
          
          <div class="form-actions">
            <button type="button" @click="showCreateModal = false" class="btn btn-outline">
              Cancelar
            </button>
            <button type="submit" class="btn btn-primary">
              {{ editingProduct ? 'Actualizar' : 'Crear' }} Producto
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Modal para crear/editar categoría -->
    <div v-if="showCategoryModal" class="modal-overlay" @click="showCategoryModal = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ editingCategory ? 'Editar' : 'Crear' }} Categoría</h3>
          <button @click="showCategoryModal = false" class="modal-close">
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>
        
        <form @submit.prevent="guardarCategoria" class="product-form">
          <div class="form-group">
            <label for="nombre">Nombre</label>
            <input id="nombre" v-model="categoryForm.nombre" type="text" required />
          </div>
          
          <div class="form-group">
            <label for="descripcion">Descripción (Opcional)</label>
            <textarea id="descripcion" v-model="categoryForm.descripcion"></textarea>
          </div>
          
          <div class="form-actions">
            <button type="button" @click="showCategoryModal = false" class="btn btn-outline">
              Cancelar
            </button>
            <button type="submit" class="btn btn-primary">
              {{ editingCategory ? 'Actualizar' : 'Crear' }} Categoría
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Modal para restablecer contraseña -->
    <div v-if="showResetPasswordModal" class="modal-overlay" @click="showResetPasswordModal = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>Restablecer Contraseña</h3>
          <button @click="showResetPasswordModal = false" class="modal-close">
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>
        
        <form @submit.prevent="restablecerContraseña" class="reset-password-form">
          <div class="form-group">
            <label for="usuario-nombre">Usuario</label>
            <input id="usuario-nombre" :value="selectedUser?.nombre" type="text" disabled class="form-input disabled" />
          </div>
          
          <div class="form-group">
            <label for="usuario-email">Email</label>
            <input id="usuario-email" :value="selectedUser?.correo" type="email" disabled class="form-input disabled" />
          </div>
          
          <div class="form-group">
            <label for="nueva-contraseña">Nueva Contraseña</label>
            <input 
              id="nueva-contraseña"
              v-model="resetPasswordForm.nueva_contraseña" 
              type="password" 
              required 
              class="form-input"
              :class="{ 'error': passwordError }"
              placeholder="Ingresa la nueva contraseña (mínimo 6 caracteres)"
              @input="validarContraseña"
            />
            <div v-if="passwordError" class="error-message">{{ passwordError }}</div>
            <div class="password-requirements">
              <small>La contraseña debe tener al menos 6 caracteres</small>
            </div>
          </div>
          
          <div class="form-group">
            <label for="confirmar-contraseña">Confirmar Contraseña</label>
            <input 
              id="confirmar-contraseña"
              v-model="resetPasswordForm.confirmar_contraseña" 
              type="password" 
              required 
              class="form-input"
              :class="{ 'error': confirmPasswordError }"
              placeholder="Confirma la nueva contraseña"
              @input="validarConfirmacion"
            />
            <div v-if="confirmPasswordError" class="error-message">{{ confirmPasswordError }}</div>
          </div>
          
          <div class="form-actions">
            <button type="button" @click="showResetPasswordModal = false" class="btn btn-outline">
              Cancelar
            </button>
            <button type="submit" class="btn btn-warning" :disabled="loading">
              <div v-if="loading" class="loading-spinner"></div>
              <span v-else>Restablecer Contraseña</span>
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Modal de Confirmación Elegante -->
    <div v-if="showConfirmModal" class="modal-overlay" @click="closeConfirmModal">
      <div class="confirm-modal" @click.stop>
        <div class="confirm-modal-header">
          <div class="confirm-modal-icon" :class="confirmModalData.type">
            <svg v-if="confirmModalData.type === 'warning'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.34 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
            </svg>
            <svg v-else-if="confirmModalData.type === 'danger'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
            <svg v-else fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
          </div>
          <h3 class="confirm-modal-title">{{ confirmModalData.title }}</h3>
        </div>
        <div class="confirm-modal-body">
          <p class="confirm-modal-message">{{ confirmModalData.message }}</p>
        </div>
        <div class="confirm-modal-actions">
          <button @click="closeConfirmModal" class="btn btn-outline">
            {{ confirmModalData.cancelText }}
          </button>
          <button @click="executeConfirmAction" class="btn" :class="getConfirmButtonClass()">
            {{ confirmModalData.confirmText }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'
import { getApiUrl, getImageUrl, getSimpleImageUrl } from '../config/api.js'

const router = useRouter()
const toast = useToast()
const usuario = ref(null)
const activeTab = ref('dashboard')
const showCreateModal = ref(false)
const showCategoryModal = ref(false)
const editingProduct = ref(null)
const editingCategory = ref(null)
const showResetPasswordModal = ref(false)
const selectedUser = ref(null)
const loading = ref(false)

// Variables para validación
const passwordError = ref('')
const confirmPasswordError = ref('')

// Variables para modal de confirmación elegante
const showConfirmModal = ref(false)
const confirmModalData = ref({
  title: '',
  message: '',
  confirmText: 'Confirmar',
  cancelText: 'Cancelar',
  type: 'warning', // warning, danger, info
  onConfirm: null
})

// Datos
const stats = ref({
  totalProductos: 0,
  totalUsuarios: 0,
  totalVentas: 0,
  ingresosTotales: 0
})

const productos = ref([])
const usuarios = ref([])
const ventas = ref([])
const categorias = ref([])
const productosRecientes = ref([])
const ventasRecientes = ref([])

// Formulario de producto
const productForm = ref({
  nombre: '',
  descripcion: '',
  precio: 0,
  stock: 0,
  categoria_id: '',
  imagen: null
})

// Formulario de categoría
const categoryForm = ref({
  nombre: '',
  descripcion: ''
})

// Formulario de restablecimiento de contraseña
const resetPasswordForm = ref({
  nueva_contraseña: '',
  confirmar_contraseña: ''
})

// Tabs de navegación
const tabs = [
  { id: 'dashboard', name: 'Dashboard', icon: 'M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2H5a2 2 0 00-2-2z' },
  { id: 'productos', name: 'Productos', icon: 'M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4' },
  { id: 'categorias', name: 'Categorías', icon: 'M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10' },
  { id: 'usuarios', name: 'Usuarios', icon: 'M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-6a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z' },
  { id: 'ventas', name: 'Ventas', icon: 'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z' }
]

onMounted(async () => {
  usuario.value = JSON.parse(localStorage.getItem('usuario'))
  if (!usuario.value || usuario.value.rol !== 'admin') {
    router.push('/productos')
    return
  }
  
  await cargarDatos()
})

async function cargarDatos() {
  try {
    const token = localStorage.getItem('token')
    const headers = { Authorization: `Bearer ${token}` }
    
    // Cargar estadísticas
    const [productosRes, usuariosRes, ventasRes, categoriasRes] = await Promise.all([
      axios.get(getApiUrl('products'), { headers }),
      axios.get(`${getApiUrl('users')}?admin_id=${usuario.value.id}`, { headers }),
      axios.get(`${getApiUrl('sales')}?admin_id=${usuario.value.id}`, { headers }),
      axios.get(getApiUrl('categories'), { headers })
    ])
    
    productos.value = productosRes.data || []
    usuarios.value = usuariosRes.data || []
    ventas.value = ventasRes.data || []
    categorias.value = categoriasRes.data || []
    
    // Limpiar datos de imagen inválidos
    productos.value = productos.value.map(producto => {
      if (producto.imagen) {
        // Detectar valores de imagen inválidos
        const invalidValues = ['no hay', 'sin imagen', 'null', 'undefined', 'none', '']
        if (invalidValues.includes(producto.imagen.toLowerCase().trim())) {
          producto.imagen = null
        }
      }
      return producto
    })
    
    // Calcular estadísticas
    stats.value = {
      totalProductos: productos.value.length,
      totalUsuarios: usuarios.value.length,
      totalVentas: ventas.value.length,
      ingresosTotales: ventas.value.reduce((sum, venta) => {
        const total = typeof venta.total === 'number' ? venta.total : parseFloat(venta.total || 0)
        return sum + total
      }, 0)
    }
    
    // Productos y ventas recientes
    productosRecientes.value = productos.value.slice(-5).reverse()
    ventasRecientes.value = ventas.value.slice(-5).reverse()
    
  } catch (error) {
    console.error('Error al cargar datos:', error)
    if (error.response?.status === 422) {
      toast.error('Error de validación: ' + (error.response.data?.detail || 'Parámetros inválidos'))
    } else if (error.response?.status === 403) {
      toast.error('No tienes permisos para acceder a estos datos')
    } else if (error.response?.status === 401) {
      toast.error('Sesión expirada. Por favor, inicia sesión nuevamente')
      router.push('/')
    } else {
      toast.error('Error al cargar los datos del dashboard: ' + (error.response?.data?.detail || error.message))
    }
  }
}

function handleImageChange(event) {
  productForm.value.imagen = event.target.files[0]
}

async function guardarProducto() {
  try {
    const token = localStorage.getItem('token')
    const formData = new FormData()
    
    formData.append('nombre', productForm.value.nombre)
    formData.append('descripcion', productForm.value.descripcion)
    formData.append('precio', productForm.value.precio)
    formData.append('stock', productForm.value.stock)
    formData.append('admin_id', usuario.value.id)
    if (productForm.value.categoria_id) {
      formData.append('categoria_id', productForm.value.categoria_id)
    }
    if (productForm.value.imagen) {
      formData.append('imagen', productForm.value.imagen)
    }
    
    if (editingProduct.value) {
      await axios.put(`${getApiUrl('products')}/${editingProduct.value.id}?admin_id=${usuario.value.id}`, formData, {
        headers: { Authorization: `Bearer ${token}` }
      })
      toast.success('Producto actualizado exitosamente')
    } else {
      await axios.post(getApiUrl('products'), formData, {
        headers: { Authorization: `Bearer ${token}` }
      })
      toast.success('Producto creado exitosamente')
    }
    
    showCreateModal.value = false
    limpiarFormulario()
    await cargarDatos()
    
  } catch (error) {
    console.error('Error al guardar producto:', error)
    toast.error('Error al guardar el producto')
  }
}

function editarProducto(producto) {
  editingProduct.value = producto
  productForm.value = {
    nombre: producto.nombre,
    descripcion: producto.descripcion,
    precio: producto.precio,
    stock: producto.stock,
    categoria_id: producto.categoria_id || '',
    imagen: null
  }
  showCreateModal.value = true
}

async function eliminarProducto(id) {
  // Usar el modal de confirmación elegante
  showConfirm(
    'Eliminar Producto',
    '¿Estás seguro de que quieres eliminar este producto? Esta acción no se puede deshacer.',
    'Eliminar Producto',
    'Cancelar',
    'danger',
    async () => {
      try {
        const token = localStorage.getItem('token')
        await axios.delete(`${getApiUrl('products')}/${id}?admin_id=${usuario.value.id}`, {
          headers: { Authorization: `Bearer ${token}` }
        })
        toast.success('Producto eliminado exitosamente')
        await cargarDatos()
      } catch (error) {
        console.error('Error al eliminar producto:', error)
        toast.error('Error al eliminar el producto')
      }
    }
  )
}

async function toggleUserStatus(user) {
  try {
    const token = localStorage.getItem('token')
    const currentStatus = user.estado || 'activo'
    const newStatus = currentStatus === 'activo' ? 'inactivo' : 'activo'
    
    await axios.put(`${getApiUrl('changeUserStatus')}/${user.id}`, {
      admin_id: usuario.value.id,
      nuevo_estado: newStatus
    }, {
      headers: { Authorization: `Bearer ${token}` }
    })
    toast.success(`Usuario ${currentStatus === 'activo' ? 'desactivado' : 'activado'} exitosamente`)
    await cargarDatos()
  } catch (error) {
    console.error('Error al cambiar estado de usuario:', error)
    toast.error('Error al cambiar el estado del usuario')
  }
}

async function cambiarRolUsuario(user) {
  try {
    const token = localStorage.getItem('token')
    const currentRole = user.rol || 'cliente'
    const newRole = currentRole === 'cliente' ? 'admin' : 'cliente'
    
    await axios.put(`${getApiUrl('changeUserRole')}/${user.id}`, {
      admin_id: usuario.value.id,
      nuevo_rol: newRole
    }, {
      headers: { Authorization: `Bearer ${token}` }
    })
    toast.success(`Rol del usuario cambiado a ${newRole} exitosamente`)
    await cargarDatos()
  } catch (error) {
    console.error('Error al cambiar rol de usuario:', error)
    toast.error('Error al cambiar el rol del usuario')
  }
}

async function eliminarCategoria(id) {
  // Usar el modal de confirmación elegante
  showConfirm(
    'Eliminar Categoría',
    '¿Estás seguro de que quieres eliminar esta categoría? Esta acción no se puede deshacer.',
    'Eliminar Categoría',
    'Cancelar',
    'danger',
    async () => {
      try {
        const token = localStorage.getItem('token')
        await axios.delete(`${getApiUrl('categories')}/${id}`, {
          headers: { Authorization: `Bearer ${token}` }
        })
        toast.success('Categoría eliminada exitosamente')
        await cargarDatos()
      } catch (error) {
        console.error('Error al eliminar categoría:', error)
        toast.error('Error al eliminar la categoría')
      }
    }
  )
}

async function guardarCategoria() {
  try {
    const token = localStorage.getItem('token')
    
    if (editingCategory.value) {
      await axios.put(`${getApiUrl('categories')}/${editingCategory.value.id}`, categoryForm.value, {
        headers: { Authorization: `Bearer ${token}` }
      })
      toast.success('Categoría actualizada exitosamente')
    } else {
      await axios.post(getApiUrl('categories'), categoryForm.value, {
        headers: { Authorization: `Bearer ${token}` }
      })
      toast.success('Categoría creada exitosamente')
    }
    
    showCategoryModal.value = false
    limpiarFormularioCategoria()
    await cargarDatos()
    
  } catch (error) {
    console.error('Error al guardar categoría:', error)
    toast.error('Error al guardar la categoría')
  }
}

function editarCategoria(categoria) {
  editingCategory.value = categoria
  categoryForm.value = {
    nombre: categoria.nombre,
    descripcion: categoria.descripcion || ''
  }
  showCategoryModal.value = true
}

function limpiarFormulario() {
  productForm.value = {
    nombre: '',
    descripcion: '',
    precio: 0,
    stock: 0,
    categoria_id: '',
    imagen: null
  }
  editingProduct.value = null
}

function limpiarFormularioCategoria() {
  categoryForm.value = {
    nombre: '',
    descripcion: ''
  }
  editingCategory.value = null
}

function mostrarModalRestablecerContraseña(user) {
  selectedUser.value = user
  showResetPasswordModal.value = true
  resetPasswordForm.value = {
    nueva_contraseña: '',
    confirmar_contraseña: ''
  }
  passwordError.value = ''
  confirmPasswordError.value = ''
}

async function restablecerContraseña() {
  // Validar que las contraseñas coincidan
  if (resetPasswordForm.value.nueva_contraseña !== resetPasswordForm.value.confirmar_contraseña) {
    toast.error('Las contraseñas no coinciden')
    return
  }

  // Validar longitud mínima de contraseña
  if (resetPasswordForm.value.nueva_contraseña.length < 6) {
    toast.error('La contraseña debe tener al menos 6 caracteres')
    return
  }

  // Usar el modal de confirmación elegante
  showConfirm(
    'Restablecer Contraseña',
    `¿Estás seguro de que quieres restablecer la contraseña para ${selectedUser.value.nombre}?`,
    'Restablecer Contraseña',
    'Cancelar',
    'warning',
    async () => {
      loading.value = true
      try {
        const token = localStorage.getItem('token')
        await axios.put(`${getApiUrl('resetPassword')}/${selectedUser.value.id}`, {
          nueva_contraseña: resetPasswordForm.value.nueva_contraseña,
          admin_id: usuario.value.id
        }, {
          headers: { Authorization: `Bearer ${token}` }
        })
        
        toast.success(`Contraseña restablecida exitosamente para ${selectedUser.value.nombre}`)
        showResetPasswordModal.value = false
        selectedUser.value = null
        resetPasswordForm.value = {
          nueva_contraseña: '',
          confirmar_contraseña: ''
        }
      } catch (error) {
        console.error('Error al restablecer contraseña:', error)
        if (error.response?.status === 403) {
          toast.error('No tienes permisos para restablecer contraseñas')
        } else if (error.response?.status === 404) {
          toast.error('Usuario no encontrado')
        } else if (error.response?.status === 400) {
          toast.error(error.response.data.detail || 'Datos inválidos')
        } else {
          toast.error('Error al restablecer la contraseña')
        }
      } finally {
        loading.value = false
      }
    }
  )
}

function validarContraseña() {
  passwordError.value = ''
  if (resetPasswordForm.value.nueva_contraseña.length > 0 && resetPasswordForm.value.nueva_contraseña.length < 6) {
    passwordError.value = 'La contraseña debe tener al menos 6 caracteres'
  }
  validarConfirmacion()
}

function validarConfirmacion() {
  confirmPasswordError.value = ''
  if (resetPasswordForm.value.confirmar_contraseña.length > 0 && 
      resetPasswordForm.value.nueva_contraseña !== resetPasswordForm.value.confirmar_contraseña) {
    confirmPasswordError.value = 'Las contraseñas no coinciden'
  }
}

function showConfirm(title, message, confirmText, cancelText, type = 'warning', onConfirm = null) {
  confirmModalData.value = {
    title: title,
    message: message,
    confirmText: confirmText,
    cancelText: cancelText,
    type: type,
    onConfirm: onConfirm
  }
  showConfirmModal.value = true
}

function closeConfirmModal() {
  showConfirmModal.value = false
  confirmModalData.value = {
    title: '',
    message: '',
    confirmText: 'Confirmar',
    cancelText: 'Cancelar',
    type: 'warning',
    onConfirm: null
  }
}

async function executeConfirmAction() {
  if (confirmModalData.value.onConfirm) {
    await confirmModalData.value.onConfirm()
  }
  closeConfirmModal()
}

function getConfirmButtonClass() {
  switch (confirmModalData.value.type) {
    case 'warning':
      return 'btn-warning'
    case 'danger':
      return 'btn-error'
    default:
      return 'btn-primary'
  }
}


</script>

<style scoped>
.admin-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem;
  min-height: 100vh;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
  color: white;
}

.admin-header {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 1.5rem;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
  transition: all 0.5s ease;
}

.admin-header:hover {
  transform: translateY(-4px);
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-title {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.header-icon-container {
  width: 64px;
  height: 64px;
  background: linear-gradient(135deg, #a855f7 0%, #9333ea 100%);
  border-radius: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
  transition: all 0.5s ease;
}

.header-icon-container:hover {
  transform: scale(1.1) rotate(5deg);
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
}

.header-icon {
  width: 32px;
  height: 32px;
  color: white;
}

.header-title h1 {
  margin: 0;
  font-size: 2.25rem;
  font-weight: 800;
  background: linear-gradient(135deg, #a855f7 0%, #9333ea 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: -0.025em;
}

.admin-info {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.125rem;
}

.admin-name {
  font-weight: 700;
  color: white;
  font-size: 1.125rem;
}

.admin-role {
  font-size: 0.875rem;
  color: #cbd5e1;
  background: rgba(255, 255, 255, 0.1);
  padding: 0.125rem 0.5rem;
  border-radius: 9999px;
  backdrop-filter: blur(10px);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 1.5rem;
  padding: 2.5rem;
  color: white;
  position: relative;
  overflow: hidden;
  transition: all 0.5s ease;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.stat-card:nth-child(1) {
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.9), rgba(29, 78, 216, 0.9)) !important;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 0 30px rgba(59, 130, 246, 0.3) !important;
}

.stat-card:nth-child(2) {
  background: linear-gradient(135deg, rgba(139, 92, 246, 0.9), rgba(124, 58, 237, 0.9)) !important;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 0 30px rgba(139, 92, 246, 0.3) !important;
}

.stat-card:nth-child(3) {
  background: linear-gradient(135deg, rgba(6, 182, 212, 0.9), rgba(8, 145, 178, 0.9)) !important;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 0 30px rgba(6, 182, 212, 0.3) !important;
}

.stat-card:nth-child(4) {
  background: linear-gradient(135deg, rgba(236, 72, 153, 0.9), rgba(190, 24, 93, 0.9)) !important;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 0 30px rgba(236, 72, 153, 0.3) !important;
}

.stat-card:hover {
  transform: translateY(-12px) scale(1.02);
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
}

.stat-card .stat-icon {
  width: 72px;
  height: 72px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1.5rem;
  backdrop-filter: blur(10px);
  transition: all 0.5s ease;
}

.stat-card:hover .stat-icon {
  transform: scale(1.1) rotate(5deg);
  background: rgba(255, 255, 255, 0.3);
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
}

.stat-card .stat-number {
  font-size: 2.25rem;
  font-weight: 800;
  margin: 0;
  line-height: 1;
  color: white;
}

.stat-card .stat-label {
  font-size: 1.125rem;
  font-weight: 600;
  margin: 0;
  color: rgba(255, 255, 255, 0.9);
}

.admin-nav {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 2rem;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 1rem;
  padding: 0.75rem;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.nav-tab {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem 1.5rem;
  background: transparent;
  border: none;
  border-radius: 0.75rem;
  color: #cbd5e1;
  cursor: pointer;
  transition: all 0.5s ease;
  font-weight: 600;
  position: relative;
  overflow: hidden;
}

.nav-tab:hover {
  color: #3b82f6;
  transform: translateY(-2px);
}

.nav-tab.active {
  color: white;
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
}

.tab-icon {
  width: 20px;
  height: 20px;
  transition: transform 0.5s ease;
}

.nav-tab:hover .tab-icon,
.nav-tab.active .tab-icon {
  transform: scale(1.1);
}

.tab-content {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 1.5rem;
  padding: 2rem;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  transition: all 0.5s ease;
}

.tab-content:hover {
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
}

.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 1.5rem;
}

.dashboard-card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 1.5rem;
  padding: 1.5rem;
  border: 1px solid rgba(255, 255, 255, 0.2);
  transition: all 0.5s ease;
}

.dashboard-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
}

.dashboard-card h3 {
  margin: 0 0 1.5rem 0;
  color: white;
  font-size: 1.25rem;
  font-weight: 700;
}

.recent-items,
.recent-sales {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.recent-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 0.5rem;
}

.item-image {
  width: 40px;
  height: 40px;
  object-fit: cover;
  border-radius: 0.5rem;
}

.item-image-placeholder {
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, #475569 0%, #64748b 100%);
  border-radius: 0.75rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #cbd5e1;
  font-size: 0.625rem;
  text-align: center;
  padding: 8px;
  border: 2px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.item-image-placeholder:hover {
  border-color: rgba(255, 255, 255, 0.3);
  box-shadow: 0 6px 12px -2px rgba(0, 0, 0, 0.15);
  transform: translateY(-2px);
}

.item-image-placeholder span {
  margin-top: 4px;
  font-weight: 500;
  line-height: 1;
}

.item-info h4 {
  margin: 0;
  font-size: 1rem;
  color: white;
}

.item-info p {
  margin: 0;
  color: #cbd5e1;
  font-size: 0.875rem;
}

.sale-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 0.5rem;
}

.sale-info h4 {
  margin: 0;
  font-size: 1rem;
  color: white;
}

.sale-info p {
  margin: 0;
  color: #cbd5e1;
  font-size: 0.875rem;
}

.sale-amount {
  font-weight: 600;
  color: #3b82f6;
}

/* Estilos básicos para tablas y elementos adicionales */
.products-table,
.users-table,
.sales-table {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

th {
  background: rgba(255, 255, 255, 0.1);
  font-weight: 600;
  color: white;
}

.product-thumb {
  width: 40px;
  height: 40px;
  object-fit: cover;
  border-radius: 0.5rem;
}

.stock-badge {
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 500;
  background: #10b981;
  color: white;
}

.stock-badge.low-stock {
  background: #f59e0b;
}

.role-badge {
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 500;
  text-transform: capitalize;
}

.role-badge.admin {
  background: #3b82f6;
  color: white;
}

.role-badge.user {
  background: #475569;
  color: #cbd5e1;
}

.role-dropdown {
  padding: 0.5rem 1rem;
  border: 2px solid rgba(255, 255, 255, 0.2);
  border-radius: 0.75rem;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  color: white;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.5s ease;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 20 20' fill='%23ffffff' class='w-4 h-4'%3E%3Cpath fill-rule='evenodd' d='M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z' clip-rule='evenodd'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 0.5rem center;
  background-size: 1.2em;
  min-width: 100px;
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
}

.role-dropdown:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1), 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  transform: translateY(-1px);
}

.role-dropdown:hover:not(:disabled) {
  border-color: #3b82f6;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.role-dropdown.disabled {
  opacity: 0.5;
  cursor: not-allowed;
  background-color: #475569;
  border-color: rgba(255, 255, 255, 0.2);
}

.role-dropdown.disabled:hover {
  border-color: rgba(255, 255, 255, 0.2);
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  transform: none;
}

.role-dropdown option {
  background: #1e293b;
  color: white;
  padding: 0.5rem;
}

.status-badge {
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 500;
}

.status-badge.active {
  background: #10b981;
  color: white;
}

.status-badge.inactive {
  background: #ef4444;
  color: white;
}

.action-buttons {
  display: flex;
  gap: 0.25rem;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.3s ease-out;
}

.modal-content {
  background: #1e293b;
  border-radius: 0.75rem;
  padding: 2rem;
  width: 90%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
  color: white;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

.modal-header h3 {
  margin: 0;
  color: white;
}

.modal-close {
  background: none;
  border: none;
  cursor: pointer;
  color: #cbd5e1;
  padding: 0.5rem;
}

.modal-close svg {
  width: 20px;
  height: 20px;
}

.product-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.form-group label {
  font-weight: 500;
  color: white;
}

.form-group input,
.form-group textarea,
.form-group select {
  padding: 1rem;
  border: 2px solid rgba(255, 255, 255, 0.2);
  border-radius: 0.5rem;
  background: #334155;
  color: white;
  transition: all 0.15s ease;
}

.form-group input:focus,
.form-group textarea:focus,
.form-group select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgb(59 130 246 / 0.1);
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid rgba(255, 255, 255, 0.2);
}

.btn-error {
  background: #ef4444;
  color: white;
}

.btn-error:hover {
  background: #dc2626;
}

.reset-password-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.reset-password-form .form-group {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.reset-password-form .form-group label {
  font-weight: 500;
  color: white;
}

.reset-password-form .form-group input {
  padding: 1rem;
  border: 2px solid rgba(255, 255, 255, 0.2);
  border-radius: 0.5rem;
  background: #334155;
  color: white;
  transition: all 0.15s ease;
}

.reset-password-form .form-group input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgb(59 130 246 / 0.1);
}

.reset-password-form .form-group input.disabled {
  background-color: #475569;
  color: #cbd5e1;
  cursor: not-allowed;
}

.reset-password-form .form-group input.error {
  border-color: #ef4444;
  box-shadow: 0 0 0 3px rgb(239 68 68 / 0.1);
}

.reset-password-form .form-group input:focus.error {
  border-color: #ef4444;
  box-shadow: 0 0 0 3px rgb(239 68 68 / 0.1);
}

.error-message {
  color: #ef4444;
  font-size: 0.875rem;
  margin-top: 0.25rem;
}

.password-requirements {
  font-size: 0.75rem;
  color: #cbd5e1;
  margin-top: 0.25rem;
}

.loading-spinner {
  border: 4px solid rgba(255, 255, 255, 0.3);
  border-top: 4px solid #3b82f6;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  animation: spin 1s linear infinite;
  margin: 0 auto;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Responsive */
@media (max-width: 768px) {
  .admin-container {
    padding: 1rem;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .admin-nav {
    flex-wrap: wrap;
  }
  
  .nav-tab {
    flex: 1;
    min-width: 120px;
  }
  
  .dashboard-grid {
    grid-template-columns: 1fr;
  }
  
  .header-content {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
  
  .admin-info {
    align-items: center;
  }
}

/* Estilos básicos para categorías y botones */
.categories-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.category-card {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 0.75rem;
  padding: 1.5rem;
  transition: all 0.3s ease;
}

.category-card:hover {
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.category-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.category-header h3 {
  margin: 0;
  color: white;
  font-size: 1.125rem;
}

.category-actions {
  display: flex;
  gap: 0.25rem;
}

.category-stats {
  display: flex;
  gap: 1rem;
}

.stat-item {
  font-size: 0.875rem;
  color: #cbd5e1;
}

.stat-item strong {
  color: #3b82f6;
  font-weight: 600;
}

.no-image {
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, #475569 0%, #64748b 100%);
  border-radius: 0.75rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #cbd5e1;
  font-size: 0.625rem;
  text-align: center;
  padding: 8px;
  border: 2px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.no-image:hover {
  border-color: rgba(255, 255, 255, 0.3);
  box-shadow: 0 6px 12px -2px rgba(0, 0, 0, 0.15);
  transform: translateY(-2px);
}

.no-image span {
  margin-top: 4px;
  font-weight: 500;
  line-height: 1;
}

.btn-warning {
  background: #f59e0b;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: all 0.15s ease;
  font-size: 0.875rem;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.btn-warning:hover {
  background: #d97706;
  transform: translateY(-1px);
}

.btn-warning:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

/* Estilos para el modal de confirmación */
.confirm-modal {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  border-radius: 1.5rem;
  padding: 3rem;
  width: 90%;
  max-width: 500px;
  max-height: 80vh;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 2rem;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
  border: 1px solid rgba(255, 255, 255, 0.2);
  animation: slideInUp 0.3s ease-out;
}

.confirm-modal-header {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

.confirm-modal-icon {
  width: 56px;
  height: 56px;
  background: #475569;
  border-radius: 9999px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.5rem;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}

.confirm-modal-icon.warning {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  color: white;
  box-shadow: 0 0 20px rgba(245, 158, 11, 0.4);
}

.confirm-modal-icon.danger {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: white;
  box-shadow: 0 0 20px rgba(239, 68, 68, 0.4);
}

.confirm-modal-title {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 800;
  color: white;
  background: linear-gradient(135deg, #a855f7 0%, #9333ea 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: -0.025em;
}

.confirm-modal-body {
  text-align: center;
  color: #cbd5e1;
  font-size: 1.125rem;
  line-height: 1.6;
}

.confirm-modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1.5rem;
}

.confirm-modal-actions .btn {
  padding: 1rem 2rem;
  font-size: 0.875rem;
  font-weight: 600;
  border-radius: 0.75rem;
  transition: all 0.5s ease;
  min-width: 120px;
}

.confirm-modal-actions .btn-outline {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.confirm-modal-actions .btn-outline:hover {
  background: #475569;
  border-color: rgba(255, 255, 255, 0.2);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.confirm-modal-actions .btn-warning {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  color: white;
  border: none;
  box-shadow: 0 0 20px rgba(245, 158, 11, 0.4);
}

.confirm-modal-actions .btn-warning:hover {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  box-shadow: 0 0 30px rgba(245, 158, 11, 0.6);
  transform: translateY(-2px);
}

.confirm-modal-actions .btn-error {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: white;
  border: none;
  box-shadow: 0 0 20px rgba(239, 68, 68, 0.4);
}

.confirm-modal-actions .btn-error:hover {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  box-shadow: 0 0 30px rgba(239, 68, 68, 0.6);
  transform: translateY(-2px);
}

/* Animaciones */
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes slideInUp {
  from {
    opacity: 0;
    transform: translateY(30px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.image-container {
  position: relative;
  display: inline-block;
}

.product-thumb {
  width: 40px;
  height: 40px;
  object-fit: cover;
  border-radius: 0.5rem;
  border: 2px solid rgba(255, 255, 255, 0.2);
  transition: all 0.3s ease;
}

.product-thumb:hover {
  transform: scale(1.1);
  border-color: #3b82f6;
}
</style>
