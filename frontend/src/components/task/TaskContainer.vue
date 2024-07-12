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
            @toggle-complete="toggleComplete" @sort-tasks="sortTasks" />
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
                order: this.tasks.length
            }).then(response => {
                this.tasks.splice(response.data.data.order, 0, response.data.data);
            }).catch(error => {
                alert(error.response.data.message);
            });
        },
        deleteTask(taskIndex, taskId) {
            this.$http.delete(`/api/tasks/${taskId}/`).then(() => {
                for (let i = 0; i < this.tasks.length; i++) {
                    if (this.tasks[i].id === taskId) {
                        this.tasks.splice(i, 1);
                        break;
                    }
                }
            }).catch(error => {
                alert(error.response.data.message);
            });
        },
        editTask(taskIndex, taskId, newText) {
            this.$http.put(`/api/tasks/${taskId}/`, {
                id: taskId,
                title: newText,
            }).then(response => {
                for (let i = 0; i < this.tasks.length; i++) {
                    if (this.tasks[i].id === taskId) {
                        this.tasks[i].title = newText;
                        break;
                    }
                }
            }).catch(error => {
                alert(error.response.data.message);
            });
        },
        toggleComplete(taskIndex, taskId) {
            this.$http.put(`/api/tasks/${taskId}/`, {
                id: taskId,
                is_completed: true,
            }).then(response => {
                for (let i = 0; i < this.tasks.length; i++) {
                    if (this.tasks[i].id === taskId) {
                        this.tasks[i].is_completed = true;
                        break;
                    }
                }
            }).catch(error => {
                alert(error.response.data.message);
            });
        },
        sortTasks(newTasks) {
            const tasksToUpdate = []

            for (let i = 0; i < newTasks.length; i++) {
                tasksToUpdate.push({
                    id: newTasks[i].id,
                    order: i
                });
            }

            this.$http.put(`/api/tasks/bulk_update/`, tasksToUpdate).then(response => {
                this.tasks = response.data.data
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