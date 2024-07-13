<template>
    <div class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 p-4">
        <div class="bg-white w-full sm:w-5/6 md:w-3/4 p-6 rounded-lg shadow-lg">
            <div class="flex justify-between mb-2">
                <input class="text-2xl font-bold" v-if="titleEditable" v-model="title"
                    @input="$emit('change', title, description)" />
                <button @click="$emit('close')" class="text-2xl">&times;</button>
            </div>
            <textarea class="w-full" v-if="descriptionEditable" v-model="description"
                @input="$emit('change', title, description)" />
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
    data() {
        return {
            title: this.title,
            description: this.description,
        }
    },
}
</script>