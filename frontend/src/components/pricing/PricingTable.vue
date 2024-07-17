<template>
    <div class="flex flex-col lg:flex-row items-start justify-center gap-4 w-full">
        <PricingCard title="Standard" price="0" :features="['Feature 1', 'Feature 2', 'Feature 3']" />
        <PricingCard title="Premium" price="9" :features="['Feature 1', 'Feature 2', 'Feature 3', 'Feature 4']" />
    </div>
</template>

<script>
import PricingCard from '@/components/pricing/PricingCard.vue';

export default {
    components: {
        PricingCard,
    },
}
</script>