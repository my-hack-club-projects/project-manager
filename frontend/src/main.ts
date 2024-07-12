import './assets/tailwind.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import axiosInstance from './axios';

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.config.globalProperties.$http = axiosInstance
app.config.globalProperties.$isDevelopment = process.env.NODE_ENV !== 'production'

app.mount('#app')
