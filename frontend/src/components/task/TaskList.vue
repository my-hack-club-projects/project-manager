<template>
    <draggable v-model="tasksCopy" @end="onDragEnd" :itemKey="task => task.id" :disabled="disableDrag">
        <template #item="{ element, index }">
            <Task :key="element.id" :id="element.id" :task="element.title" :completed="element.is_completed"
                @delete-task="deleteTask(index, element.id)" @edit-task="editTask(index, element.id, $event)"
                @toggle-complete="toggleComplete(index, element.id)" :draggable="!element.is_completed" />
        </template>
    </draggable>
</template>

<script>
import Task from './Task.vue';
import draggable from 'vuedraggable';

export default {
    components: {
        Task,
        draggable
    },
    props: {
        tasks: Array,
        disableDrag: Boolean
    },
    data() {
        return {
            tasksCopy: [...this.tasks] // Initialize tasksCopy with a copy of tasks
        };
    },
    watch: {
        tasks: {
            handler(newVal) {
                this.tasksCopy = [...newVal]; // Update tasksCopy when tasks prop changes
            },
            immediate: true // Ensure tasksCopy is initialized immediately
        }
    },
    methods: {
        onDragEnd(event) {
            console.log('Dragged task list:', this.tasksCopy);
        },
        deleteTask(index, taskId) {
            // Implement deleteTask logic using index and taskId
            this.$emit('delete-task', index, taskId); // Emit event to parent component if needed
        },
        editTask(index, taskId, newText) {
            // Implement editTask logic using index, taskId, and newText
            this.$emit('edit-task', index, taskId, newText); // Emit event to parent component if needed
        },
        toggleComplete(index, taskId) {
            // Implement toggleComplete logic using index and taskId
            this.$emit('toggle-complete', index, taskId); // Emit event to parent component if needed
        }
    }
};
</script>
