<template>
    <!-- todo disable scrolling -->
    <div class="flex flex-col items-center h-screen bg-gray-50">
        <LoginForm @login="registerEmail" type="register" :error="error"></LoginForm>
    </div>
</template>

<script>
import LoginForm from '@/components/global/LoginForm.vue';

export default {
    components: {
        LoginForm
    },
    data() {
        return {
            error: null
        };
    },
    methods: {
        async registerEmail(data) {
            this.$http.post('/accounts/registration/', {
                "email": data.email,
                "password1": data.password1,
                "password2": data.password2
            }).then((response) => {
                if (!response.data.success) {
                    throw new Error(response.data.message || "An error occurred");
                }

                this.$router.push("/email_sent/");
            }).catch((error) => {
                console.error("Register error", error.response.data);

                if (error.response.data.success && error.response.data.data.email !== undefined) {
                    this.error = error.response.data.data.email[0];
                } else {
                    this.$alert(error.response.data);
                }
            });
        }
    }
};
</script>