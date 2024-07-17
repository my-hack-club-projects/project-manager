<template>
    <div
        class="w-full max-w-sm p-8 bg-white border border-gray-200 rounded-lg shadow dark:bg-gray-800 dark:border-gray-700">
        <h5 class="mb-4 text-xl font-medium text-gray-500 dark:text-gray-400">{{ title }}</h5>
        <div class="flex items-baseline text-gray-900 dark:text-white">
            <span class="text-3xl font-semibold">$</span>
            <span class="text-5xl font-extrabold tracking-tight">{{ price }}</span>
            <span class="ms-1 text-xl font-normal text-gray-500 dark:text-gray-400">/month</span>
        </div>
        <ul role="list" class="space-y-5 my-7">
            <PricingFeature v-for="feature in features" :key="feature" :feature="feature" />
        </ul>

        <TextButton color="blue" class="w-full">Choose plan</TextButton>
    </div>
</template>

<script>
import TextButton from '@/components/global/TextButton.vue';
import PricingFeature from './PricingFeature.vue';

export default {
    components: {
        TextButton,
        PricingFeature,
    },
    props: {
        title: {
            type: String,
            required: true,
        },
        price: {
            type: Number,
            required: true,
        },
        features: {
            type: Array,
            required: true,
        },
    }
}
</script>