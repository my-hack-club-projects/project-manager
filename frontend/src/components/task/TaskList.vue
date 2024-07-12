<template>
    <draggable v-model="tasksCopy" @end="onDragEnd" :itemKey="task => task.id">
        <template #item="{ element }">
            <Task :key="element.id" :id="element.id" :task="element.title" :completed="element.is_completed"
                @delete-task="deleteTask(index, element.id)" @edit-task="editTask(index, element.id, $event)"
                @toggle-complete="toggleComplete(index, element.id)" />
        </template>
    </draggable>
</template>

<script>
import Task from './Task.vue';
import draggable from 'vuedraggable';

export default {
    props: {
        tasks: Array
    },
    components: {
        Task,
        draggable
    },
    data() {
        return {
            tasksCopy: [] // Use a separate array to bind to v-model
        };
    },
    watch: {
        tasks: {
            immediate: true,
            handler(newVal) {
                // Ensure tasksCopy always reflects the current prop value
                this.tasksCopy = newVal.slice(); // Create a shallow copy
            }
        }
    },
    methods: {
        onDragEnd(event) {
            // Handle the logic to save the updated order of tasks in the database
            console.log('Dragged task list:', this.tasksCopy);
            // Add logic to save the updated order of tasks in the database
            // Call an API or emit an event to parent component to handle saving
        },
        deleteTask(index, taskId) {
            this.$emit('delete-task', index, taskId);
        },
        editTask(index, taskId, newText) {
            this.$emit('edit-task', index, taskId, newText);
        },
        toggleComplete(index, taskId) {
            this.$emit('toggle-complete', index, taskId);
        }
    }
};
</script>

<style>
/* Add your styles here */
</style>
