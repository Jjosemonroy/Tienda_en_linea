import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import Toast from 'vue-toastification'
import 'vue-toastification/dist/index.css'
import vuetify from './plugins/vuetify'
import './assets/styles.css'

const app = createApp(App)

// Configuración de notificaciones simplificada
const toastOptions = {
  position: 'top-right',
  timeout: 4000,
  closeOnClick: true,
  pauseOnFocusLoss: true,
  pauseOnHover: true,
  draggable: true,
  hideProgressBar: false,
  closeButton: 'button',
  icon: true,
  maxToasts: 5,
  newestOnTop: true
}

app.use(router)
app.use(Toast, toastOptions)
app.use(vuetify)

app.mount('#app')