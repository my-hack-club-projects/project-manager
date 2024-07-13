<!-- src/components/global/PromptDialog.vue -->
<template>
    <div v-if="visible" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 p-4">
        <div class="bg-white w-full sm:w-5/6 md:w-3/4 p-6 rounded-lg shadow-lg">
            <div class="flex justify-between mb-2">
                <h2 class="text-2xl font-bold">{{ title }}</h2>
                <button @click="close(false)" class="text-2xl">&times;</button>
            </div>
            <div>
                <p class="text-gray-500 mb-4">{{ message }}</p>
                <input type="text" class="w-full p-2 border border-gray-300 rounded mb-4" v-model="inputValue"
                    @keyup.enter="confirm" />
                <div class="flex justify-end">
                    <button @click="confirm" class="bg-blue-500 text-white px-4 py-2 rounded">Confirm</button>
                </div>
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
            message: '',
            inputValue: '',
            resolve: null,
            reject: null,
        };
    },
    methods: {
        show(title, message) {
            this.title = title;
            this.message = message;
            this.inputValue = '';
            this.visible = true;

            return new Promise((resolve, reject) => {
                this.resolve = resolve;
                this.reject = reject;
            });
        },
        confirm() {
            this.visible = false;
            this.resolve(this.inputValue);
        },
        close(cancelled = true) {
            this.visible = false;
            if (cancelled) {
                this.reject('Prompt was cancelled');
            }
        },
    },
};
</script>