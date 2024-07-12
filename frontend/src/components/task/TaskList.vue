<template>
    <draggable v-model="tasksCopy" @change="onDragEnd" :itemKey="task => task.id" :disabled="disableDrag">
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
        this.sort(this.tasks);
        return {
            tasksCopy: [...this.tasks]
        };
    },
    watch: {
        tasks: {
            handler(newVal) {
                this.tasksCopy = [...newVal];
            },
            deep: true,
            immediate: true
        }
    },
    methods: {
        sort(tasks) {
            tasks.sort((a, b) => a.order - b.order);
        },
        setOrder(tasks) {
            tasks.forEach((task, index) => {
                task.order = index;
            });
        },
        onDragEnd(event) {
            this.setOrder(this.tasksCopy);

            // copy the Order from each task to the original tasks array
            this.tasksCopy.forEach((task, index) => {
                this.tasks.find(t => t.id === task.id).order = index;
            });

            this.sort(this.tasks);

            this.$emit('sort-tasks', this.tasksCopy);
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
