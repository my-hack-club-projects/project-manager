<template>
    <div class="flex flex-col items-center h-screen bg-gray-50">
        <div>
            <div class="flex flex-col items-center">
                <h1 class="text-3xl font-bold mt-8">
                    <span v-if="success">Success!</span>
                    <span v-else>Error!</span>
                </h1>

                <div v-if="success" class="flex flex-col items-center text-gray-500 mt-4">
                    <p class="mt-4">Your email was confirmed successfully.</p>
                    <p class="mt-4">You can now <RouterLink to="/login/" class="text-blue-500">sign in</RouterLink>.</p>
                </div>
                <div v-else class="flex flex-col items-center text-gray-500 mt-4">
                    <p class="mt-4">The link has expired.</p>
                    <p class="mt-4">Please try generating a new one by <RouterLink to="/register/"
                            class="text-blue-500">
                            signing up</RouterLink> again.</p>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'EmailConfirmed',

    data() {
        return {
            success: this.$route.params.success == 'success'
        };
    }
};
</script>