<template>
    <ul>
        <Task v-for="(task, index) in tasks" :key="task.id" :id="task.id" :task="task.title"
            :completed="task.is_completed" @delete-task="$emit('delete-task', index, task.id)"
            @edit-task="(newText) => $emit('edit-task', index, task.id, newText)"
            @toggle-complete="$emit('toggle-complete', index, task.id)" />
    </ul>
</template>

<script>
import Task from './Task.vue'

export default {
    props: {
        tasks: Array
    },
    components: {
        Task
    }
}
</script>

<style>
/* Add your styles here */
</style>