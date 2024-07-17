<template>
    <div>
        <div v-if="stripePublicKey && stripePricingTableId">
            <stripe-pricing-table :pricing-table-id="stripePricingTableId" :publishable-key="stripePublicKey"
                :client-reference-id="clientReferenceId">
            </stripe-pricing-table>
        </div>
        <div v-else>
            Loading...
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            stripePricingTableId: null,
            stripePublicKey: null,
            clientReferenceId: null,
            isLoaded: false,
        };
    },
    mounted() {
        this.fetchKeys();
    },
    methods: {
        fetchKeys() {
            this.$http.get('/api/products/keys/')
                .then(response => {
                    this.stripePricingTableId = response.data.data.pricing_table_id;
                    this.stripePublicKey = response.data.data.public_key;
                    this.clientReferenceId = response.data.data.client_reference_id;

                    this.loadStripe();
                })
                .catch(error => {
                    console.error('Error fetching keys:', error);
                });
        },
        loadStripe() {
            if (!window.Stripe) {
                const script = document.createElement('script');
                script.src = "https://js.stripe.com/v3/pricing-table.js";
                script.async = true;
                script.onload = this.initializeStripe;
                document.head.appendChild(script);
            } else {
                this.initializeStripe();
            }
        },
        initializeStripe() {
            this.isLoaded = true;
        }
    }
}
</script>