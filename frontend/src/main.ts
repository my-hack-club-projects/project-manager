import './assets/tailwind.css'

import { createApp, h } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import axiosInstance from './axios';
import ConfirmDialog from './components/global/ConfirmDialog.vue'

const app = createApp(App)

app.use(createPinia())
app.use(router)

// Global components
let confirmDialogInstance: any;

app.config.globalProperties.$confirm = (message: string, good = true) => {
    if (!confirmDialogInstance) {
        const confirmDialogContainer = document.createElement('div');
        document.body.appendChild(confirmDialogContainer);

        confirmDialogInstance = createApp(ConfirmDialog).mount(confirmDialogContainer);
    }

    return confirmDialogInstance.show(message, good);
};

app.config.globalProperties.$http = axiosInstance
app.config.globalProperties.$isDevelopment = process.env.NODE_ENV !== 'production'

app.mount('#app')
