<template>
    <div v-if="visible" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 p-4">
        <div class="bg-white w-full sm:w-5/6 md:w-1/3 p-6 rounded-lg shadow-lg">
            <div class="mb-4">
                <h2 class="text-xl font-bold">{{ title }}</h2>
                <p class="text-gray-500">{{ message }}</p>
            </div>
            <div class="flex justify-end">
                <TextButton @click="close" color="blue">Ok</TextButton>
            </div>
        </div>
    </div>
</template>

<script>
import TextButton from './TextButton.vue';

export default {
    data() {
        return {
            visible: false,
            title: '',
            message: ''
        };
    },
    components: {
        TextButton
    },
    methods: {
        show(title, message) {
            this.title = title;
            this.message = message;
            this.visible = true;
            return new Promise(resolve => {
                this.resolve = resolve;
            });
        },
        close() {
            this.visible = false;
            this.resolve();
        }
    }
};
</script>