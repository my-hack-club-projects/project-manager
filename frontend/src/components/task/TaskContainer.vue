<template>
    <div class="container my-5">
        <div class="w-full">
            <div class="bg-slate-200 rounded-lg shadow-md p-6 w-full">
                <div class="flex justify-between">
                    <div class="flex items-center">
                        <h1 class="text-lg font-bold">{{ title }}</h1>
                        <button class="ml-2">
                            <svg class="feather feather-edit" fill="none" height="24" stroke="currentColor"
                                stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewBox="0 0 24 24"
                                width="24" xmlns="http://www.w3.org/2000/svg">
                                <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" />
                                <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z" />
                            </svg>
                        </button>
                    </div>

                    <button class="mr-2">
                        <svg class="feather feather-edit" height="16" width="16" fill="#000000" version="1.1"
                            xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
                            viewBox="0 0 490 490" xml:space="preserve">
                            <polygon points="456.851,0 245,212.564 33.149,0 0.708,32.337 212.669,245.004 0.708,457.678 33.149,490 245,277.443 456.851,490 
        489.292,457.678 277.331,245.004 489.292,32.337 " />
                        </svg>
                    </button>
                </div>
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