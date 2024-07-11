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
        id: Number,
        title: String,
        tasks: Array
    },
    components: {
        AddTaskForm,
        TaskList,
    },
    methods: {
        addTask(task) {
            fetch(`http://localhost:8000/api/taskcontainers/${this.id}/tasks/`, {
                method: 'POST',
                body: JSON.stringify({
                    title: task,
                })
            }).then(response => {
                if (response.ok) {
                    return response.json()
                }
                throw new Error('Failed to add task')
            }).then(data => {
                this.tasks.push(data)
            }).catch(error => {
                console.error('Error adding task:', error)
            })
        },
        deleteTask(taskIndex) {
            // There is no delete endpoint lol
            this.tasks.splice(taskIndex, 1)
        },
        editTask({ taskIndex, newText }) {
            fetch(`http://localhost:8000/api/taskcontainers/${this.id}/tasks/`, {
                method: 'PATCH',
                body: JSON.stringify({
                    id: this.tasks[taskIndex].id,
                    title: newText,
                })
            }).then(response => {
                if (response.ok) {
                    return response.json()
                }
                throw new Error('Failed to edit task')
            }).then(data => {
                this.tasks.splice(taskIndex, 1, data)
            }).catch(error => {
                console.error('Error editing task:', error)
            })

            this.tasks.splice(index, 1, { ...this.tasks[index], title: newText })
        },
        toggleComplete(taskIndex) {
            fetch(`http://localhost:8000/api/taskcontainers/${this.id}/tasks/`, {
                method: 'PATCH',
                body: JSON.stringify({
                    id: this.tasks[taskIndex].id,
                    is_completed: true,
                })
            }).then(response => {
                if (response.ok) {
                    return response.json()
                }
                throw new Error('Failed to edit task')
            }).then(data => {
                this.tasks.splice(index, 1, data)
            }).catch(error => {
                console.error('Error editing task:', error)
            })

            this.tasks[taskIndex].is_completed = true
        }
    }
}
</script>

<style>
/* Add your styles here */
</style>