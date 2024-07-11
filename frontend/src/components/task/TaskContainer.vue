<template>
    <div class="container my-5">
        <div class="w-full">
            <div class="bg-slate-200 rounded-lg shadow-md p-6 w-full">
                <h1 class="text-lg font-bold">{{ title }}</h1>
                <TaskList :tasks="tasks" @delete-task="deleteTask" @edit-task="editTask"
                    @toggle-complete="toggleComplete" />
                <AddTaskForm @add-task="addTask" />
            </div>
        </div>
    </div>
</template>

<script>
import AddTaskForm from './AddTaskForm.vue'
import TaskList from './TaskList.vue'

export default {
    props: {
        title: String,
        tasks: Array
    },
    components: {
        AddTaskForm,
        TaskList,
    },
    methods: {
        addTask(task) {
            this.tasks.push(task)
        },
        deleteTask(taskIndex) {
            this.tasks.splice(taskIndex, 1)
        },
        editTask({ index, newText }) {
            this.tasks.splice(index, 1, { ...this.tasks[index], task: newText })
        },
        toggleComplete(taskIndex) {
            this.tasks[taskIndex].is_completed = !this.tasks[taskIndex].is_completed
        }
    }
}
</script>

<style>
/* Add your styles here */
</style>