<template>
  <div class="proceso-pago-container">
    <!-- Header -->
    <div class="page-header">
      <div class="header-content">
        <h1 class="page-title">Proceso de Pago</h1>
        <p class="page-subtitle">Completa tu información para finalizar la compra</p>
      </div>
      <div class="header-actions">
        <div class="order-summary">
          <span class="order-total">Q{{ carrito.total_carrito.toFixed(2) }}</span>
          <span class="order-label">Total</span>
        </div>
      </div>
    </div>

    <!-- Contenido principal -->
    <div class="payment-content">
      <div v-if="cargando" class="loading-state">
        <div class="loading-spinner"></div>
        <p>Cargando información...</p>
      </div>

      <div v-else class="payment-steps">
        <!-- Paso 1: Dirección de envío -->
        <div class="step-section">
          <div class="step-header">
            <h2>1. Dirección de envío</h2>
            <button 
              v-if="!mostrarFormularioDireccion" 
              class="btn btn-outline btn-sm" 
              @click="mostrarFormularioDireccion = true"
            >
              Agregar nueva dirección
            </button>
          </div>

          <!-- Lista de direcciones existentes -->
          <div v-if="direcciones.length > 0 && !mostrarFormularioDireccion" class="addresses-list">
            <div 
              v-for="direccion in direcciones" 
              :key="direccion.id"
              class="address-card"
              :class="{ 'selected': direccionSeleccionada?.id === direccion.id }"
              @click="seleccionarDireccion(direccion)"
            >
              <div class="address-info">
                <div class="address-header">
                  <h3 v-if="direccion.alias">{{ direccion.alias }}</h3>
                  <h3 v-else>Dirección {{ direccion.id }}</h3>
                  <span v-if="direccion.es_principal" class="principal-badge">Principal</span>
                </div>
                <p class="recipient-name">{{ direccion.nombre_completo }}</p>
                <p>{{ direccion.direccion }}</p>
                <p>{{ direccion.ciudad }}, {{ direccion.codigo_postal }}</p>
                <p>{{ direccion.telefono }}</p>
              </div>
              <div class="address-actions">
                <input 
                  type="radio" 
                  :value="direccion.id" 
                  v-model="direccionSeleccionada"
                  @change="seleccionarDireccion(direccion)"
                />
              </div>
            </div>
          </div>

          <!-- Formulario de nueva dirección -->
          <div v-if="mostrarFormularioDireccion" class="address-form">
            <h3>Nueva dirección de envío</h3>
            <form @submit.prevent="crearDireccion">
            <div class="form-group">
                <label>Alias de la dirección</label>
                <input 
                  v-model="nuevaDireccion.alias" 
                  type="text" 
                  required 
                  placeholder="Alias de la dirección"
                />
              </div>

              <div class="form-group">
                <label>Nombre completo</label>
                <input 
                  v-model="nuevaDireccion.nombre_completo" 
                  type="text" 
                  required 
                  placeholder="Tu nombre completo"
                />
              </div>
              
              <div class="form-group">
                <label>Dirección</label>
                <textarea 
                  v-model="nuevaDireccion.direccion" 
                  required 
                  placeholder="Dirección completa"
                  rows="3"
                ></textarea>
              </div>
              
              <div class="form-row">
                <div class="form-group">
                  <label>Ciudad</label>
                  <input 
                    v-model="nuevaDireccion.ciudad" 
                    type="text" 
                    required 
                    placeholder="Ciudad"
                  />
                </div>
                
                <div class="form-group">
                  <label>Código postal</label>
                  <input 
                    v-model="nuevaDireccion.codigo_postal" 
                    type="text" 
                    required 
                    placeholder="Código postal"
                  />
                </div>
              </div>
              
              <div class="form-group">
                <label>Teléfono</label>
                <input 
                  v-model="nuevaDireccion.telefono" 
                  type="tel" 
                  required 
                  placeholder="Número de teléfono"
                />
              </div>
              
              <div class="form-group">
                <label class="checkbox-label">
                  <input 
                    v-model="nuevaDireccion.es_principal" 
                    type="checkbox"
                  />
                  Marcar como dirección principal
                </label>
              </div>
              
              <div class="form-actions">
                <button type="submit" class="btn btn-primary">Guardar dirección</button>
                <button type="button" class="btn btn-outline" @click="cancelarFormularioDireccion">
                  Cancelar
                </button>
              </div>
            </form>
          </div>
        </div>

        <!-- Paso 2: Método de pago -->
        <div class="step-section">
          <div class="step-header">
            <h2>2. Método de pago</h2>
          </div>

          <div class="payment-methods">
            <div 
              v-for="metodo in metodosPago" 
              :key="metodo.id"
              class="payment-method-card"
              :class="{ 'selected': metodoPagoSeleccionado?.id === metodo.id }"
              @click="seleccionarMetodoPago(metodo)"
            >
              <div class="method-info">
                <h3>{{ metodo.nombre }}</h3>
                <p>{{ metodo.descripcion }}</p>
              </div>
              <div class="method-actions">
                <input 
                  type="radio" 
                  :value="metodo.id" 
                  v-model="metodoPagoSeleccionado"
                  @change="seleccionarMetodoPago(metodo)"
                />
              </div>
            </div>
          </div>
        </div>

        <!-- Paso 3: Datos de pago -->
        <div v-if="metodoPagoSeleccionado" class="step-section">
          <div class="step-header">
            <h2>3. Datos de pago</h2>
          </div>

          <div class="payment-form">
            <!-- Formulario para tarjeta -->
            <div v-if="metodoPagoSeleccionado.tipo === 'tarjeta'" class="card-form">
              <div class="form-group">
                <label>Número de tarjeta</label>
                <input 
                  v-model="datosPago.numero_tarjeta" 
                  type="text" 
                  placeholder="1234 5678 9012 3456"
                  maxlength="19"
                />
              </div>
              
              <div class="form-row">
                <div class="form-group">
                  <label>Fecha de vencimiento</label>
                  <input 
                    v-model="datosPago.fecha_vencimiento" 
                    type="text" 
                    placeholder="MM/AA"
                    maxlength="5"
                  />
                </div>
                
                <div class="form-group">
                  <label>CVV</label>
                  <input 
                    v-model="datosPago.cvv" 
                    type="text" 
                    placeholder="123"
                    maxlength="4"
                  />
                </div>
              </div>
              
              <div class="form-group">
                <label>Nombre en la tarjeta</label>
                <input 
                  v-model="datosPago.nombre_titular" 
                  type="text" 
                  placeholder="Nombre como aparece en la tarjeta"
                />
              </div>
            </div>

            <!-- Formulario para transferencia -->
            <div v-else-if="metodoPagoSeleccionado.tipo === 'transferencia'" class="transfer-form">
              <div class="form-group">
                <label>Número de cuenta</label>
                <input 
                  v-model="datosPago.numero_cuenta" 
                  type="text" 
                  placeholder="Número de cuenta bancaria"
                />
              </div>
              
              <div class="form-group">
                <label>Banco</label>
                <input 
                  v-model="datosPago.banco" 
                  type="text" 
                  placeholder="Nombre del banco"
                />
              </div>
            </div>

            <!-- Información para PayPal -->
            <div v-else-if="metodoPagoSeleccionado.tipo === 'paypal'" class="paypal-form">
              <div class="form-group">
                <label>Email de PayPal</label>
                <input 
                  v-model="datosPago.email_paypal" 
                  type="email" 
                  placeholder="tu@email.com"
                />
              </div>
            </div>

            <!-- Información para efectivo -->
            <div v-else-if="metodoPagoSeleccionado.tipo === 'efectivo'" class="cash-form">
              <div class="cash-info">
                <p>Pagarás en efectivo al recibir tu pedido.</p>
                <p>El repartidor te contactará para coordinar la entrega.</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Resumen y botón de pago -->
        <div class="step-section">
          <div class="step-header">
            <h2>4. Resumen de compra</h2>
          </div>

          <div class="order-summary-card">
            <div class="summary-content">
              <div class="summary-row">
                <span>Subtotal:</span>
                <span>Q{{ carrito.total_carrito.toFixed(2) }}</span>
              </div>
              <div class="summary-row">
                <span>Envío:</span>
                <span>Gratis</span>
              </div>
              <div class="summary-divider"></div>
              <div class="summary-row total">
                <span>Total:</span>
                <span>Q{{ carrito.total_carrito.toFixed(2) }}</span>
              </div>
            </div>

            <div class="summary-actions">
              <button 
                class="btn btn-primary btn-lg" 
                @click="procesarPago"
                :disabled="!puedeProcesarPago"
              >
                <svg class="btn-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H5a3 3 0 00-3 3v8a3 3 0 003 3z"></path>
                </svg>
                Procesar pago
              </button>
            </div>
          </div>
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
import { getApiUrl } from '../config/api.js'

const router = useRouter()
const toast = useToast()

// Datos reactivos
const usuario = ref(null)
const carrito = ref({ items: [], total_carrito: 0 })
const metodosPago = ref([])
const direcciones = ref([])
const cargando = ref(true)

// Estados del formulario
const direccionSeleccionada = ref(null)
const metodoPagoSeleccionado = ref(null)
const mostrarFormularioDireccion = ref(false)

// Datos de nueva dirección
const nuevaDireccion = ref({
  alias: '',
  nombre_completo: '',
  direccion: '',
  ciudad: '',
  codigo_postal: '',
  telefono: '',
  es_principal: false
})

// Datos de pago
const datosPago = ref({
  numero_tarjeta: '',
  fecha_vencimiento: '',
  cvv: '',
  nombre_titular: '',
  numero_cuenta: '',
  banco: '',
  email_paypal: ''
})

// Computed
const puedeProcesarPago = computed(() => {
  return direccionSeleccionada.value && metodoPagoSeleccionado.value
})

// Métodos
onMounted(async () => {
  usuario.value = JSON.parse(localStorage.getItem('usuario'))
  if (!usuario.value) {
    router.push('/login')
    return
  }
  
  await Promise.all([
    cargarCarrito(),
    cargarMetodosPago(),
    cargarDirecciones()
  ])
  cargando.value = false
})

async function cargarCarrito() {
  try {
    const token = localStorage.getItem('token')
    const response = await axios.get(`${getApiUrl('cart')}/${usuario.value.id}`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    carrito.value = response.data
  } catch (error) {
    console.error('Error al cargar carrito:', error)
    toast.error('Error al cargar el carrito')
  }
}

async function cargarMetodosPago() {
  try {
    const response = await axios.get(getApiUrl('paymentMethods'))
    metodosPago.value = response.data
  } catch (error) {
    console.error('Error al cargar métodos de pago:', error)
    toast.error('Error al cargar métodos de pago')
  }
}

async function cargarDirecciones() {
  try {
    const token = localStorage.getItem('token')
    const response = await axios.get(`${getApiUrl('shippingAddresses')}/${usuario.value.id}`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    direcciones.value = response.data
    
    // Seleccionar la dirección principal si existe
    const principal = direcciones.value.find(d => d.es_principal)
    if (principal) {
      direccionSeleccionada.value = principal
    }
  } catch (error) {
    console.error('Error al cargar direcciones:', error)
    // No mostrar error si no hay direcciones
  }
}

function seleccionarDireccion(direccion) {
  direccionSeleccionada.value = direccion
}

function seleccionarMetodoPago(metodo) {
  metodoPagoSeleccionado.value = metodo
}

async function crearDireccion() {
  try {
    const token = localStorage.getItem('token')
    
    // Crear el objeto de datos sin usuario_id (se obtiene del token)
    const datosDireccion = {
      alias: nuevaDireccion.value.alias,
      nombre_completo: nuevaDireccion.value.nombre_completo,
      direccion: nuevaDireccion.value.direccion,
      ciudad: nuevaDireccion.value.ciudad,
      codigo_postal: nuevaDireccion.value.codigo_postal,
      telefono: nuevaDireccion.value.telefono,
      es_principal: nuevaDireccion.value.es_principal
    }
    
    const response = await axios.post(getApiUrl('createShippingAddress'), datosDireccion, {
      headers: { Authorization: `Bearer ${token}` }
    })
    
    toast.success('Dirección creada exitosamente')
    await cargarDirecciones()
    cancelarFormularioDireccion()
  } catch (error) {
    console.error('Error al crear dirección:', error)
    toast.error('Error al crear la dirección')
  }
}

function cancelarFormularioDireccion() {
  mostrarFormularioDireccion.value = false
  nuevaDireccion.value = {
    alias: '',
    nombre_completo: '',
    direccion: '',
    ciudad: '',
    codigo_postal: '',
    telefono: '',
    es_principal: false
  }
}

async function procesarPago() {
  if (!puedeProcesarPago.value) {
    toast.warning('Por favor completa todos los campos requeridos')
    return
  }

  try {
    // Primero finalizar la compra usando el endpoint del carrito
    const token = localStorage.getItem('token')
    const ventaResponse = await axios.post(`${getApiUrl('cart')}/finalizar/${usuario.value.id}`, {}, {
      headers: { Authorization: `Bearer ${token}` }
    })

    // Luego procesar el pago
    const pagoResponse = await axios.post(getApiUrl('processPayment'), {
      venta_id: ventaResponse.data.venta_id,
      metodo_pago_id: metodoPagoSeleccionado.value.id,
      datos_pago: datosPago.value,
      direccion_envio_id: direccionSeleccionada.value.id
    }, {
      headers: { Authorization: `Bearer ${token}` }
    })

    toast.success('¡Pago procesado exitosamente!')
    router.push('/carrito')
  } catch (error) {
    console.error('Error al procesar pago:', error)
    toast.error('Error al procesar el pago')
  }
}
</script>

<style scoped>
.proceso-pago-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: var(--spacing-lg);
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-2xl);
  padding: var(--spacing-xl);
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: var(--border-radius-lg);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  color: white;
}

.header-content {
  flex: 1;
}

.page-title {
  font-size: var(--font-size-3xl);
  font-weight: 700;
  color: white;
  margin-bottom: var(--spacing-xs);
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.page-subtitle {
  color: rgba(255, 255, 255, 0.9);
  font-size: var(--font-size-base);
}

.order-summary {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-xs);
  background: rgba(255, 255, 255, 0.2);
  padding: var(--spacing-md);
  border-radius: var(--border-radius);
  backdrop-filter: blur(10px);
}

.order-total {
  font-size: var(--font-size-2xl);
  font-weight: 700;
  color: white;
}

.order-label {
  color: rgba(255, 255, 255, 0.8);
  font-size: var(--font-size-sm);
}

.loading-state {
  text-align: center;
  padding: var(--spacing-2xl);
  color: var(--text-muted);
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #e2e8f0;
  border-top: 4px solid #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto var(--spacing-lg);
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.payment-steps {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-2xl);
}

.step-section {
  background: white;
  border-radius: var(--border-radius-lg);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  overflow: hidden;
  border: 1px solid #e2e8f0;
  transition: all 0.3s ease;
}

.step-section:hover {
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.step-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-lg);
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
  border-bottom: 1px solid #e2e8f0;
}

.step-header h2 {
  margin: 0;
  color: #2d3748;
  font-weight: 600;
}

/* Botones mejorados */
.btn {
  display: inline-flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-md) var(--spacing-lg);
  border: none;
  border-radius: var(--border-radius);
  font-weight: 500;
  text-decoration: none;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: var(--font-size-base);
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  box-shadow: 0 4px 14px rgba(102, 126, 234, 0.4);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
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
}

.btn-outline:hover {
  background: #667eea;
  color: white;
  transform: translateY(-1px);
}

.btn-sm {
  padding: var(--spacing-sm) var(--spacing-md);
  font-size: var(--font-size-sm);
}

.btn-lg {
  padding: var(--spacing-lg) var(--spacing-xl);
  font-size: var(--font-size-lg);
  font-weight: 600;
}

.btn-icon {
  width: 18px;
  height: 18px;
}

/* Direcciones */
.addresses-list {
  padding: var(--spacing-lg);
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.address-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-lg);
  border: 2px solid #e2e8f0;
  border-radius: var(--border-radius);
  cursor: pointer;
  transition: all 0.3s ease;
  background: white;
}

.address-card:hover {
  border-color: #667eea;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15);
  transform: translateY(-1px);
}

.address-card.selected {
  border-color: #667eea;
  background: linear-gradient(135deg, #f0f4ff 0%, #e6f0ff 100%);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
}

.address-info h3 {
  margin: 0 0 var(--spacing-xs) 0;
  color: #2d3748;
  font-weight: 600;
}

.address-info p {
  margin: 0 0 var(--spacing-xs) 0;
  color: #4a5568;
  font-size: var(--font-size-sm);
}

.address-actions input[type="radio"] {
  width: 20px;
  height: 20px;
  accent-color: #667eea;
}

/* Formularios */
.address-form {
  padding: var(--spacing-lg);
  background: #f8fafc;
}

.address-form h3 {
  margin-bottom: var(--spacing-lg);
  color: #2d3748;
  font-weight: 600;
}

.form-group {
  margin-bottom: var(--spacing-lg);
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--spacing-lg);
}

.form-group label {
  display: block;
  margin-bottom: var(--spacing-xs);
  color: #2d3748;
  font-weight: 500;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: var(--spacing-md);
  border: 2px solid #e2e8f0;
  border-radius: var(--border-radius);
  font-size: var(--font-size-base);
  transition: all 0.2s ease;
  background: white;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  cursor: pointer;
  color: #4a5568;
}

.checkbox-label input[type="checkbox"] {
  width: 18px;
  height: 18px;
  accent-color: #667eea;
}

.form-actions {
  display: flex;
  gap: var(--spacing-md);
  margin-top: var(--spacing-lg);
}

/* Métodos de pago */
.payment-methods {
  padding: var(--spacing-lg);
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: var(--spacing-lg);
}

.payment-method-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-lg);
  border: 2px solid #e2e8f0;
  border-radius: var(--border-radius);
  cursor: pointer;
  transition: all 0.3s ease;
  background: white;
}

.payment-method-card:hover {
  border-color: #667eea;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15);
  transform: translateY(-1px);
}

.payment-method-card.selected {
  border-color: #667eea;
  background: linear-gradient(135deg, #f0f4ff 0%, #e6f0ff 100%);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
}

.method-info h3 {
  margin: 0 0 var(--spacing-xs) 0;
  color: #2d3748;
  font-weight: 600;
}

.method-info p {
  margin: 0;
  color: #4a5568;
  font-size: var(--font-size-sm);
}

.method-actions input[type="radio"] {
  width: 20px;
  height: 20px;
  accent-color: #667eea;
}

/* Formulario de pago */
.payment-form {
  padding: var(--spacing-lg);
  background: #f8fafc;
}

.card-form,
.transfer-form,
.paypal-form {
  background: white;
  padding: var(--spacing-lg);
  border-radius: var(--border-radius);
  border: 1px solid #e2e8f0;
}

.cash-form {
  background: linear-gradient(135deg, #f0fff4 0%, #e6fffa 100%);
  padding: var(--spacing-lg);
  border-radius: var(--border-radius);
  border: 1px solid #9ae6b4;
  text-align: center;
}

.cash-info p {
  margin: 0 0 var(--spacing-sm) 0;
  color: #2f855a;
  font-weight: 500;
}

/* Resumen de compra */
.order-summary-card {
  padding: var(--spacing-lg);
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
}

.summary-content {
  margin-bottom: var(--spacing-lg);
  background: white;
  padding: var(--spacing-lg);
  border-radius: var(--border-radius);
  border: 1px solid #e2e8f0;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-md);
  color: #4a5568;
}

.summary-row.total {
  font-size: var(--font-size-lg);
  font-weight: 700;
  color: #2d3748;
  padding-top: var(--spacing-md);
  border-top: 2px solid #e2e8f0;
}

.summary-divider {
  height: 1px;
  background: #e2e8f0;
  margin: var(--spacing-lg) 0;
}

.summary-actions {
  display: flex;
  justify-content: center;
}

/* Responsive */
@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    gap: var(--spacing-lg);
    text-align: center;
  }
  
  .form-row {
    grid-template-columns: 1fr;
  }
  
  .payment-methods {
    grid-template-columns: 1fr;
  }
  
  .form-actions {
    flex-direction: column;
  }
  
  .address-card,
  .payment-method-card {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--spacing-md);
  }
  
  .address-actions,
  .method-actions {
    align-self: flex-end;
  }
}

/* Animaciones adicionales */
.step-section {
  animation: fadeInUp 0.6s ease-out;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Estados de validación */
.form-group input:invalid {
  border-color: #e53e3e;
}

.form-group input:valid {
  border-color: #38a169;
}

/* Mejoras de accesibilidad */
.btn:focus,
.address-card:focus,
.payment-method-card:focus {
  outline: 2px solid #667eea;
  outline-offset: 2px;
}

/* Indicadores de progreso */
.step-header h2::before {
  content: '';
  display: inline-block;
  width: 8px;
  height: 8px;
  background: #667eea;
  border-radius: 50%;
  margin-right: var(--spacing-sm);
}

.address-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-xs);
}

.address-header h3 {
  margin: 0;
  color: #2d3748;
  font-weight: 600;
}

.principal-badge {
  background: #667eea;
  color: white;
  padding: var(--spacing-xs) var(--spacing-sm);
  border-radius: var(--border-radius);
  font-size: var(--font-size-xs);
  font-weight: 500;
}

.recipient-name {
  font-weight: 500;
  color: #4a5568;
  margin-bottom: var(--spacing-xs);
}
</style>