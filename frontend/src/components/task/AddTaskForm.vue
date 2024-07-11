<template>
    <form @submit.prevent="onSubmit">
        <div class="flex mt-4">
            <input v-model="newTask" type="text"
                class="w-full px-4 py-2 mr-2 rounded-lg border-gray-300 focus:outline-none focus:border-blue-500"
                placeholder="Add new task" required />
            <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
                Add
            </button>
        </div>
    </form>
</template>

<script>
export default {
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