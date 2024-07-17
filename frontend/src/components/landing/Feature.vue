<template>
    <div class="flex flex-col items-center justify-between w-full gap-2 md:gap-8">
        <WindowMockup>
            <slot></slot>
        </WindowMockup>

        <div class="flex flex-col items-center gap-2 mt-4">
            <span class="text-3xl font-semibold">{{ title }}</span>
            <span class="text-gray-500">{{ description }}</span>
        </div>
    </div>
</template>

<script>
import WindowMockup from '@/components/global/WindowMockup.vue';

export default {
    components: {
        WindowMockup,
    },
    props: {
        title: {
            type: String,
            required: true,
        },
        description: {
            type: String,
            required: true,
        },
        image: {
            type: String,
            required: true,
        },
    },
    slots: ['default']
}
</script>