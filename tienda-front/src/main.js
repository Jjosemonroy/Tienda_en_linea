import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'

const app = createApp(App)
app.use(router)                // 👈 le decís a Vue que use el router
app.mount('#app')