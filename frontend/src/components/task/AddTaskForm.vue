<template>
    <form @submit.prevent="onSubmit">
        <div class="flex mt-4">
            <input ref="input" v-model="newTask" type="text"
                class="add-task-input w-full px-4 py-2 mr-2 rounded border-gray-300 focus:outline-none focus:border-blue-500"
                :placeholder="disabled ? 'This project is archived' : placeholder" required :disabled="disabled"
                :maxlength="maxLength" />
            <TextButton v-if="!disabled" color="blue">
                Add
            </TextButton>
        </div>
    </form>
</template>

<script>
import TextButton from '../global/TextButton.vue';

export default {
    props: {
        placeholder: {
            type: String,
            default: 'Add new task'
        },
        maxLength: {
            type: Number,
            default: 100
        },
        disabled: {
            type: Boolean,
            default: false
        },
    },
    components: {
        TextButton,
    },
    data() {
        return {
            newTask: ''
        }
    },
    methods: {
        onSubmit() {
            this.$emit('add-task', this.newTask)
            this.newTask = ''
        }
    }
}
</script>