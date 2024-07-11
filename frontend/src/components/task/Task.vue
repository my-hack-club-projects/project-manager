<template>
    <li class="border-b border-gray-200 bg-slate-100 flex items-center justify-between px-4 py-4 my-2 rounded-2xl">
        <label class="flex items-center">
            <input type="checkbox" class="mr-2" :checked="completed" @change="toggleComplete" />
            <span :class="{ 'completed': completed }">{{ task }}</span>
        </label>
        <div>
            <button class="text-red-500 hover:text-red-700 mr-2" @click="$emit('delete-task')">Delete</button>
            <button class="text-blue-500 hover:text-blue-700" @click="editTask">Edit</button>
        </div>
    </li>
</template>

<script>
export default {
    props: {
        id: Number,
        task: String,
        completed: Boolean
    },
    methods: {
        toggleComplete() {
            this.$emit('toggle-complete')
        },
        editTask() {
            const newText = prompt('Enter new name', this.task)
            if (newText !== null) {
                this.$emit('edit-task', newText.trim())
            }
        }
    }
}
</script>

<style>
.completed {
    text-decoration: line-through;
}
</style>