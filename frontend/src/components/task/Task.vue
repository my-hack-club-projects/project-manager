<template>
    <li class="border-b border-gray-200 bg-slate-100 flex items-center justify-between px-4 py-4 my-2 rounded-xl"
        @mouseenter="isHovered = true" @mouseleave="isHovered = false">
        <div class="flex items-center flex-1 mr-4 overflow-hidden">
            <input type="checkbox" class="mr-2 flex-shrink-0" :checked="completed" :disabled="completed"
                @change="toggleComplete" />
            <span class="truncate" :class="{ 'completed': completed }">{{ task }}</span>
        </div>
        <div class="flex-shrink-0 flex items-center">
            <button class="mr-4 relative" @click="editTask">
                <EditIcon :isHovered="isHovered" />
            </button>
            <button class="mx-2 relative">
                <DeleteIcon :isHovered="isHovered" />
            </button>
        </div>
    </li>
</template>

<script>
import DeleteIcon from '../icons/DeleteIcon.vue';
import EditIcon from '../icons/EditIcon.vue';

export default {
    props: {
        id: Number,
        task: String,
        completed: Boolean
    },
    components: {
        EditIcon,
        DeleteIcon
    },
    data() {
        return {
            isHovered: false
        };
    },
    methods: {
        toggleComplete() {
            if (this.completed) return;
            this.$emit('toggle-complete');
        },
        editTask() {
            const newText = prompt('Enter new name', this.task);
            if (newText !== null) {
                this.$emit('edit-task', newText.trim());
            }
        }
    }
}
</script>

<style scoped>
.completed {
    text-decoration: line-through;
}
</style>
