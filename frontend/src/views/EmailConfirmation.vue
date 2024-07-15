<template>
    <div class="flex flex-col items-center h-screen bg-gray-50">
        <div>
            <div v-if="!confirmed" class="flex flex-col items-center">
                <h1 class="text-3xl font-bold mt-8">Confirming your email</h1>
                <p class="text-gray-500 mt-4">Sending a request to the server.</p>
            </div>
            <div v-else class="flex flex-col items-center">
                <h1 class="text-3xl font-bold mt-8">Email confirmed</h1>
                <p class="text-gray-500 mt-4">You have successfully confirmed your email address.</p>
                <p class="text-gray-500">You can now login to your account.</p>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            confirmed: false
        }
    },
    mounted() {
        this.confirmEmail();
    },
    methods: {
        confirmEmail() {
            console.log("Confirmation string: " + this.$route.params.confirmationString);
            console.log("Sending to: " + `/accounts/rest-auth/registration/account-confirm-email/${this.$route.params.confirmationString}`);

            this.$http.post(`/accounts/rest-auth/registration/account-confirm-email/${this.$route.params.confirmationString}/`).then((response) => {
                console.log(response.data);
                this.confirmed = true;
            }).catch((error) => {
                console.error(error);
            });
        }
    }
};
</script>