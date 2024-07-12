<template>
    <div class="container my-5 bg-slate-200 rounded-lg shadow-md p-6 w-full" @mouseenter="isHovered = true"
        @mouseleave="isHovered = false">
        <div class="flex justify-between">
            <div class="flex items-center">
                <h1 class="text-lg font-bold">{{ title }}</h1>
                <button @click="editSelf" class="ml-4 relative">
                    <EditIcon :isHovered="isHovered" />
                </button>
            </div>

            <button @click="deleteSelf" class="mx-2 relative">
                <DeleteIcon :isHovered="isHovered" />
            </button>
        </div>

        <TaskList :tasks="tasks" :disable-drag="is_completed" @delete-task="deleteTask" @edit-task="editTask"
            @toggle-complete="toggleComplete" />
        <AddTaskForm @add-task="addTask" />
    </div>
</template>

<script>
import AddTaskForm from './AddTaskForm.vue';
import TaskList from './TaskList.vue';
import EditIcon from '../icons/EditIcon.vue';
import DeleteIcon from '../icons/DeleteIcon.vue';

export default {
    props: {
        id: Number,
        title: String,
        is_completed: Boolean,
        tasks: Array
    },
    components: {
        AddTaskForm,
        TaskList,
        EditIcon,
        DeleteIcon
    },
    data() {
        return {
            isHovered: false
        };
    },
    methods: {
        addTask(task) {
            this.$http.post(`/api/tasks/`, {
                title: task,
                task_container: this.id,
            }).then(response => {
                this.tasks.push(response.data.data);
            }).catch(error => {
                alert(error.response.data.message);
            });
        },
        deleteTask(taskIndex, taskId) {
            this.$http.delete(`/api/tasks/${taskId}/`).then(() => {
                this.tasks.splice(taskIndex, 1);
            }).catch(error => {
                alert(error.response.data.message);
            });
        },
        editTask(taskIndex, taskId, newText) {
            this.$http.put(`/api/tasks/${taskId}/`, {
                id: this.tasks[taskIndex].id,
                title: newText,
            }).then(response => {
                this.tasks.splice(taskIndex, 1, response.data.data);
            }).catch(error => {
                alert(error.response.data.message);
            });
        },
        toggleComplete(taskIndex, taskId) {
            this.$http.put(`/api/tasks/${taskId}/`, {
                id: this.tasks[taskIndex].id,
                is_completed: true,
            }).then(response => {
                this.tasks.splice(taskIndex, 1, response.data.data);
            }).catch(error => {
                alert(error.response.data.message);
            });
        },
        deleteSelf() {
            this.$emit('delete', this.id);
        },
        editSelf() {
            const newTitle = prompt('Enter new name', this.title);
            if (newTitle !== null) {
                this.$emit('edit', this.id, newTitle.trim());
            }
        }
    }
};
</script>

<style scoped>
/* Add your styles here */
</style>