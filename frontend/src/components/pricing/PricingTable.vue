<template>
    <div class="flex items-center justify-center rounded-md pb-4 mb-16">
        <button type="button"
            class="px-4 py-2 text-sm min-w-24 font-medium text-gray-900 bg-white border border-gray-200 rounded-s-lg hover:bg-gray-100 hover:text-blue-700 focus:z-10 focus:ring-2 focus:ring-blue-700 focus:text-blue-700 dark:bg-gray-800 dark:border-gray-700 dark:text-white dark:hover:text-white dark:hover:bg-gray-700 dark:focus:ring-blue-500 dark:focus:text-white">
            Monthly
        </button>
        <button type="button"
            class="px-4 py-2 text-sm min-w-24 font-medium text-gray-900 bg-white border border-gray-200 rounded-e-lg hover:bg-gray-100 hover:text-blue-700 focus:z-10 focus:ring-2 focus:ring-blue-700 focus:text-blue-700 dark:bg-gray-800 dark:border-gray-700 dark:text-white dark:hover:text-white dark:hover:bg-gray-700 dark:focus:ring-blue-500 dark:focus:text-white">
            Yearly
        </button>
    </div>
    <div class="flex flex-col md:flex-row px-4 items-center md:items-start justify-center gap-4 w-full">
        <PricingCard title="Standard" price="0" :features="['Feature 1', 'Feature 2', 'Feature 3']" />
        <PricingCard title="Premium" price="9" :features="['Feature 1', 'Feature 2', 'Feature 3', 'Feature 4']" />
    </div>
</template>

<script>
import PricingCard from '@/components/pricing/PricingCard.vue';
import TextButton from '../global/TextButton.vue';

export default {
    components: {
        PricingCard,
        TextButton,
    },
}
</script>