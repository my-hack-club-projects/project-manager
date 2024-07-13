// src/global.d.ts or src/types/global.d.ts
import { App } from 'vue';

declare global {
    interface Window {
        vm: App<Element>;
    }
}