<template>
    <ul>
        <Task v-for="(task, index) in tasks" :key="index" :task="task" @delete-task="deleteTask(index)"
            @edit-task="editTask(index)" />
    </ul>
</template>

<script>
import Task from './Task.vue'

export default {
    components: {
        Task,
    },
    props: {
        tasks: Array
    },
    methods: {
        deleteTask(index) {
            this.$emit('delete-task', index)
        },
        editTask(index) {
            return newText => {
                this.$emit('edit-task', { index, newText })
            }
        }
    }
}
</script>

<style>
/* Add your styles here */
</style>