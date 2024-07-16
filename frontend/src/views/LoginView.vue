<template>
    <!-- todo disable scrolling -->
    <div class="flex flex-col items-center h-screen bg-gray-50">
        <LoginForm @login="login" type="login" :error="error"></LoginForm>
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
        login(data) {
            this.error = null;

            const email = data.email;
            const password = data.password1;

            this.$http.post('/accounts/login/', {
                email: email,
                password: password
            }).then(response => {
                if (!response.data.success) {
                    throw new Error(response.data.message);
                }

                this.$router.push("/projects/");
            }).catch(error => {
                console.log("Login response:", error.response.data);

                if (error.response.data.success && error.response.data.data.non_field_errors !== undefined) {
                    this.error = error.response.data.data.non_field_errors[0];
                } else {
                    this.$alert(error.response.data);
                }
            });
        }
    }
};
</script>