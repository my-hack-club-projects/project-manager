<template>
    <div class="container my-5">
        <div class="w-full">
            <div class="bg-slate-200 rounded-lg shadow-md p-6 w-full">
                <h1 class="text-lg font-bold">
                    Some milestone
                </h1>
                <TaskList :tasks="tasks" @delete-task="deleteTask" @edit-task="editTask" />
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
    data() {
        return {
            title: '',
            tasks: []
        }
    },
    methods: {
        addTask(task) {
            this.tasks.push(task)
        },
        deleteTask(taskIndex) {
            this.tasks.splice(taskIndex, 1)
        },
        editTask({ index, newText }) {
            this.tasks.splice(index, 1, newText)
        }
    }
}
</script>

<style>
/* Add your styles here */
</style>