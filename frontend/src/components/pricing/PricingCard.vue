<template>
    <div
        class="w-full max-w-sm p-8 bg-white border border-gray-200 rounded-lg shadow dark:bg-gray-800 dark:border-gray-700">
        <h5 class="mb-4 text-xl font-medium text-gray-500 dark:text-gray-400">{{ title }}</h5>
        <div class="flex items-baseline text-gray-900 dark:text-white">
            <span class="text-3xl font-semibold">$</span>
            <span v-if="price != null" class="text-5xl font-extrabold tracking-tight">{{ price }}</span>
            <div v-else class="w-6 h-10 bg-gray-200 dark:bg-gray-700 rounded"></div>
            <span class="ms-1 text-xl font-normal text-gray-500 dark:text-gray-400">
                <span v-if="monthly">/month</span>
                <span v-else>/year</span>
            </span>
        </div>
        <ul role="list" class="space-y-5 my-7">
            <PricingFeature v-for="feature in features" :key="feature" :feature="feature" />
        </ul>

        <TextButton @click="redirect(link)" color="blue" class="w-full">Choose plan</TextButton>
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
            type: Number | null,
            required: true,
        },
        features: {
            type: Array,
            required: true,
        },
        link: {
            type: String,
            required: true,
        },
        monthly: {
            type: Boolean,
            required: true,
        },
    },
    methods: {
        async redirect(path) {
            if (path.startsWith("http")) {
                window.location.href = path;
            } else {
                await this.$router.push(path);
            }
        },
    }
}
</script>