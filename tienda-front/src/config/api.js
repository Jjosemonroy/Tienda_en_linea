// Configuración de la API
const API_CONFIG = {
  // URL base de la API - simplificada para evitar problemas
  getBaseUrl() {
    const hostname = window.location.hostname
    const port = window.location.port
    
    // Si estamos en localhost o 127.0.0.1, usar localhost
    if (hostname === 'localhost' || hostname === '127.0.0.1') {
      return 'http://localhost:8000'
    }
    
    // Si estamos en una IP local, usar esa IP
    if (hostname.startsWith('192.168.') || hostname.startsWith('10.') || hostname.startsWith('172.')) {
      return `http://${hostname}:8000`
    }
    
    // Para otros casos, usar la misma URL que el frontend
    return `http://${hostname}:8000`
  },
  
  // URLs específicas
  urls: {
    // Usuarios
    login: '/usuarios/login',
    register: '/usuarios/registrar',
    updateProfile: '/usuarios/actualizar',
    changePassword: '/usuarios/cambiar-contraseña',
    resetPassword: '/usuarios/restablecer-contraseña',
    users: '/usuarios',
    changeUserRole: '/usuarios/cambiar-rol',
    changeUserStatus: '/usuarios/cambiar-estado',
    
    // Productos
    products: '/productos',
    categories: '/categorias',
    
    // Carrito
    cart: '/carrito',
    addToCart: '/carrito/agregar',
    updateCart: '/carrito/actualizar',
    removeFromCart: '/carrito/eliminar',
    
    // Ventas
    sales: '/ventas',
    createSale: '/ventas/crear',
   
    // Pagos
    paymentMethods: '/pagos/metodos-pago',
    shippingAddresses: '/pagos/direcciones',
    createShippingAddress: '/pagos/direcciones',
    processPayment: '/pagos/procesar',
    paymentHistory: '/pagos/historial',
    purchaseHistory: '/pagos/historial-completo',
  }
}

// Función helper para construir URLs completas
export function getApiUrl(endpoint) {
  const baseUrl = API_CONFIG.getBaseUrl()
  const url = API_CONFIG.urls[endpoint] || endpoint
  return `${baseUrl}${url}`
}

// Función helper para construir URLs de imágenes
export function getImageUrl(imagePath) {
  if (!imagePath) {
    return null
  }
  
  const baseUrl = API_CONFIG.getBaseUrl()
  
  // Si la imagen ya tiene http, devolverla tal como está
  if (imagePath.startsWith('http')) {
    return imagePath
  }
  
  // Si la imagen empieza con /, concatenar con la base URL
  if (imagePath.startsWith('/')) {
    return `${baseUrl}${imagePath}`
  }
  
  // Si no, asumir que es un path relativo
  return `${baseUrl}/${imagePath}`
}

// Función alternativa más simple para imágenes
export function getSimpleImageUrl(imagePath) {
  if (!imagePath) return null
  
  // Detectar valores de imagen inválidos
  const invalidValues = ['no hay', 'sin imagen', 'null', 'undefined', 'none', '']
  if (invalidValues.includes(imagePath.toLowerCase().trim())) {
    return null
  }
  
  const baseUrl = API_CONFIG.getBaseUrl()
  
  // Si ya es una URL completa
  if (imagePath.startsWith('http')) {
    return imagePath
  }
  
  // Si empieza con /, es relativa al servidor
  if (imagePath.startsWith('/')) {
    return `${baseUrl}${imagePath}`
  }
  
  // Si no, es relativa al directorio de imágenes
  return `${baseUrl}/static/imagenes/${imagePath}`
}

// Exportar la configuración
export default API_CONFIG
