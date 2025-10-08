import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'

// Tema personalizado para tienda en línea
const lightTheme = {
  dark: false,
  colors: {
    primary: '#1976D2',      // Azul principal
    secondary: '#424242',    // Gris oscuro
    accent: '#FF6B35',       // Naranja para llamadas a la acción
    error: '#D32F2F',        // Rojo para errores
    info: '#0288D1',         // Azul info
    success: '#388E3C',      // Verde para éxito
    warning: '#F57C00',      // Naranja para advertencias
    surface: '#FFFFFF',      // Blanco para superficies
    background: '#F5F5F5',   // Gris claro para fondo
    'on-primary': '#FFFFFF',
    'on-secondary': '#FFFFFF',
    'on-surface': '#000000',
    'on-background': '#000000',
  }
}

const darkTheme = {
  dark: true,
  colors: {
    primary: '#42A5F5',      // Azul claro para modo oscuro
    secondary: '#9E9E9E',    // Gris medio
    accent: '#FF8A65',       // Naranja claro
    error: '#EF5350',        // Rojo claro
    info: '#42A5F5',         // Azul info
    success: '#66BB6A',      // Verde claro
    warning: '#FFB74D',      // Naranja claro
    surface: '#121212',      // Negro para superficies
    background: '#000000',   // Negro para fondo
    'on-primary': '#000000',
    'on-secondary': '#000000',
    'on-surface': '#FFFFFF',
    'on-background': '#FFFFFF',
  }
}

export default createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: 'lightTheme',
    themes: {
      lightTheme,
      darkTheme
    }
  },
  defaults: {
    VCard: {
      rounded: 'lg',
      elevation: 2
    },
    VBtn: {
      rounded: 'lg',
      elevation: 1
    },
    VTextField: {
      variant: 'outlined',
      density: 'comfortable'
    },
    VSelect: {
      variant: 'outlined',
      density: 'comfortable'
    }
  }
})
