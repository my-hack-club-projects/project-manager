<template>
    <div class="flex items-center justify-center rounded-md pb-4 mb-16">
        <button type="button" @click="monthly = true"
            class="px-4 py-2 text-sm min-w-24 font-medium text-gray-900 bg-white border border-gray-200 rounded-s-lg hover:bg-gray-100 hover:text-blue-700 focus:z-10 focus:ring-2 focus:ring-blue-700 focus:text-blue-700 dark:bg-gray-800 dark:border-gray-700 dark:text-white dark:hover:text-white dark:hover:bg-gray-700 dark:focus:ring-blue-500 dark:focus:text-white">
            Monthly
        </button>
        <button type="button" @click="monthly = false"
            class="px-4 py-2 text-sm min-w-24 font-medium text-gray-900 bg-white border border-gray-200 rounded-e-lg hover:bg-gray-100 hover:text-blue-700 focus:z-10 focus:ring-2 focus:ring-blue-700 focus:text-blue-700 dark:bg-gray-800 dark:border-gray-700 dark:text-white dark:hover:text-white dark:hover:bg-gray-700 dark:focus:ring-blue-500 dark:focus:text-white">
            Yearly
        </button>
    </div>
    <div class="flex flex-col md:flex-row px-4 items-center md:items-start justify-center gap-4 w-full">
        <PricingCard title="Standard" link="/register/" price="0" :monthly="monthly" :features="features.standard" />
        <PricingCard title="Premium" :link="monthly ? paymentLinks.monthly : paymentLinks.yearly"
            :price="monthly ? prices.monthly : prices.yearly" :monthly="monthly" :features="features.premium" />
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

    data: () => ({
        monthly: true,
        paymentLinks: {
            monthly: 'https://buy.stripe.com/test_fZe15y4dw8FigV2fYZ',
            yearly: 'https://buy.stripe.com/test_fZe6pS7pI8Fi0W4aEG',
        },
        customerPortal: "https://billing.stripe.com/p/login/3cs9BE6rzewx1zO288",
        features: {
            standard: ["Some feature", "Another feature"],
            premium: [],
        },
        ids: {
            premium: "prod_QUF92RHM6siBA0",
        },
        prices: {
            monthly: null,
            yearly: null,
        },
    }),

    async mounted() {
        // Fetch the prices from the backend
        this.$http.get("/api/products/list/").then((response) => {
            const premium = response.data.data.find(product => product.id == this.ids.premium);

            this.prices.monthly = premium.prices.find(price => price.recurring.interval == 'month').unit_amount / 100;
            this.prices.yearly = premium.prices.find(price => price.recurring.interval == 'year').unit_amount / 100;

            this.features.premium = premium.metadata.features.split(";");
        });

        // Fetch user status
        this.$http.get("/api/products/is_premium/").then((response) => {
            if (response.data.data.is_premium) {
                this.paymentLinks.monthly = this.customerPortal;
                this.paymentLinks.yearly = this.customerPortal;
            }
        });
    },
}
</script>