import './assets/tailwind.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import axiosInstance from './axios';
import ConfirmDialog from './components/global/ConfirmDialog.vue'
import AlertDialog from './components/global/AlertDialog.vue'
import PromptDialog from './components/global/PromptDialog.vue'

const app = createApp(App)

app.use(createPinia())
app.use(router)

// Global components
let confirmDialogInstance: any;
let alertDialogInstance: any;
let promptDialogInstance: any;

app.config.globalProperties.$confirm = (message: string, good = true) => {
    if (!confirmDialogInstance) {
        const confirmDialogContainer = document.createElement('div');
        document.body.appendChild(confirmDialogContainer);

        confirmDialogInstance = createApp(ConfirmDialog).mount(confirmDialogContainer);
    }

    return confirmDialogInstance.show(message, good);
};

app.config.globalProperties.$alert = (title: string, message: string) => {
    if (!alertDialogInstance) {
        const alertDialogContainer = document.createElement('div');
        document.body.appendChild(alertDialogContainer);

        alertDialogInstance = createApp(AlertDialog).mount(alertDialogContainer);
    }

    return alertDialogInstance.show(title, message);
};

app.config.globalProperties.$prompt = (title: string, message: string) => {
    if (!promptDialogInstance) {
        const promptDialogContainer = document.createElement('div');
        document.body.appendChild(promptDialogContainer);

        promptDialogInstance = createApp(PromptDialog).mount(promptDialogContainer);
    }

    return promptDialogInstance.show(title, message);
};

app.config.globalProperties.$http = axiosInstance
app.config.globalProperties.$isDevelopment = process.env.NODE_ENV !== 'production'

app.mount('#app')

// Attach the Vue instance to the window object
window.vm = app;