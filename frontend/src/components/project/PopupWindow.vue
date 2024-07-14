<template>
    <div class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 p-4">
        <div class="bg-white w-full sm:w-5/6 md:w-3/4 p-6 rounded-lg shadow-lg">
            <div class="flex justify-between mb-2">
                <input class="text-2xl font-bold" placeholder="No title" v-if="titleEditable" v-model="title"
                    @input="$emit('change', title, description)" :maxlength="titleMaxLength" />
                <button @click="$emit('close')" class="text-2xl">&times;</button>
            </div>
            <textarea class="w-full" placeholder="No description" v-if="descriptionEditable" v-model="description"
                @input="$emit('change', title, description)" :maxlength="descriptionMaxLength"></textarea>
            <slot></slot>
        </div>
    </div>
</template>

<script>
export default {
    name: 'PopupWindow',
    slots: ['default'],

    props: {
        title: String,
        description: String,
        titleEditable: Boolean,
        descriptionEditable: Boolean,
        titleMaxLength: {
            type: Number,
            default: 100,
        },
        descriptionMaxLength: {
            type: Number,
            default: 1000,
        },
    },
    data() {
        return {
            title: this.title,
            description: this.description,
        }
    },
}
</script>