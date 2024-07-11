<template>
    <form @submit.prevent="onSubmit">
        <div class="flex mt-4">
            <input v-model="newTask" type="text"
                class="w-full px-4 py-2 mr-2 rounded-lg border-gray-300 focus:outline-none focus:border-blue-500"
                :placeholder="placeholder" required />
            <button class="bg-gradient-to-br from-cyan-400 to-blue-500 text-white font-bold py-2 px-4 rounded-lg">
                Add
            </button>
        </div>
    </form>
</template>

<script>
export default {
    props: {
        placeholder: {
            type: String,
            default: 'Add new task'
        }
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

<style>
/* Add your styles here */
</style>