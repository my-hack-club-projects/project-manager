<template>
    <div class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 p-4">
        <div class="bg-white w-full sm:w-5/6 md:w-3/4 p-6 rounded-lg shadow-lg">
            <div class="flex justify-between">
                <h1 class="text-2xl font-bold" v-if="titleEditable" contenteditable="true">{{ title }}</h1>
                <button @click="$emit('close')" class="text-2xl">&times;</button>
            </div>
            <p v-if="descriptionEditable" contenteditable="true">{{ description }}</p>
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
    },
}
</script>