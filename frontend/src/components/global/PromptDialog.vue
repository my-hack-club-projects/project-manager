<template>
    <div v-if="visible" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 p-4">
        <div class="bg-white w-full sm:w-5/6 md:w-3/4 p-6 rounded-lg shadow-lg">
            <div class="flex justify-between mb-2">
                <h2 class="text-2xl font-bold">{{ title }}</h2>
                <button @click="close(false)" class="text-2xl">&times;</button>
            </div>
            <div>
                <input type="text" class="w-full p-2 border border-gray-300 rounded mb-4" v-model="inputValue"
                    @keyup.enter="confirm" ref="inputField" />
                <div class="flex justify-end">
                    <TextButton @click="confirm" color="blue">Confirm</TextButton>
                </div>
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
            inputValue: '',
            resolve: null,
            reject: null,
        };
    },
    components: {
        TextButton,
    },
    methods: {
        show(title, message) {
            this.title = title;
            this.inputValue = message;
            this.visible = true;

            this.$nextTick(() => {
                this.$refs.inputField.focus();
            });

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