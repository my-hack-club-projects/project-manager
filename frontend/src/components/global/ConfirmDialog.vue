<template>
    <div v-if="visible" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 p-4">
        <div class="bg-white w-full sm:w-5/6 md:w-1/3 p-6 rounded-lg shadow-lg">
            <div class="mb-4">
                <p>{{ message }}</p>
            </div>
            <div class="flex justify-end">
                <TextButton :color="yesColor" @click="confirm(true)" class="mr-2 px-4 py-2">Yes</TextButton>
                <TextButton :color="noColor" @click="confirm(false)" class="px-4 py-2">No</TextButton>
            </div>
        </div>
    </div>
</template>

<script>
import TextButton from './TextButton.vue';

export default {
    components: {
        TextButton
    },
    data() {
        return {
            visible: false,
            message: '',
            yesColor: 'red',
            noColor: 'green',
        };
    },
    methods: {
        show(message, good) {
            if (good) {
                this.yesColor = 'green';
                this.noColor = 'red';
            } else {
                this.yesColor = 'red';
                this.noColor = 'green';
            }

            this.message = message;
            this.visible = true;
            return new Promise(resolve => {
                this.resolve = resolve;
            });
        },
        confirm(result) {
            this.visible = false;
            this.resolve(result);
        }
    }
};
</script>