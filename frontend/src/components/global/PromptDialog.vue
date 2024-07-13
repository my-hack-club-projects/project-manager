<template>
    <div v-if="visible" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 p-4">
        <div class="bg-white w-full sm:w-5/6 md:w-3/4 p-6 rounded-lg shadow-lg">
            <div class="flex justify-between mb-2">
                <h2 class="text-2xl font-bold">{{ title }}</h2>
                <button @click="close(false)" class="text-2xl">&times;</button>
            </div>
            <div>
                <input v-model="inputValue" type="text"
                    class="w-full p-2 border rounded mb-4 focus:ring-0 focus:outline-none"
                    :class="{ 'text-red-500 border-red-500': inputValue.length >= maxLength }" @keyup.enter="confirm"
                    ref="inputField" :maxlength="maxLength" />
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
            maxLength: 100,
            resolve: null,
            reject: null,
        };
    },
    components: {
        TextButton,
    },
    methods: {
        show(title, message, maxLength = 100) {
            this.title = title;
            this.inputValue = message;
            this.maxLength = maxLength;
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