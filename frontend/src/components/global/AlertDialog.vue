<template>
    <div v-if="visible" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 p-4">
        <div class="bg-white w-full sm:w-5/6 md:w-1/3 p-6 rounded-lg shadow-lg">
            <div class="mb-4">
                <h2 class="text-xl font-bold">{{ title }}</h2>
                <p class="text-gray-500">{{ message }}</p>
            </div>
            <div class="flex justify-end">
                <button @click="close" class="px-4 py-2 bg-blue-500 text-white rounded">Ok</button>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            visible: false,
            title: '',
            message: ''
        };
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

<style scoped>
/* Add your styles here */
</style>