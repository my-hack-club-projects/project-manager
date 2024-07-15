<template>
    <!-- todo disable scrolling -->
    <div class="flex flex-col items-center h-screen bg-gray-50">
        <LoginForm @login="registerEmail" type="register"></LoginForm>
    </div>
</template>

<script>
import LoginForm from '@/components/global/LoginForm.vue';

export default {
    components: {
        LoginForm
    },

    methods: {
        async registerEmail(data) {
            this.$http.post('/accounts/registration/', {
                "email": data.email,
                "password1": data.password1,
                "password2": data.password2
            }).then((response) => {
                console.log(response.data);

                if (!response.data.success) {
                    throw new Error(response.data.message || "An error occurred");
                }

                this.$router.push("/email_sent/");
            }).catch((error) => {
                console.error(error);

                this.$alert(error.message);
            });
        }
    }
};
</script>