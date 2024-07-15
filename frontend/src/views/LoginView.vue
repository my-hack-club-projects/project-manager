<template>
    <!-- todo disable scrolling -->
    <div class="flex flex-col items-center h-screen bg-gray-50">
        <LoginForm @login="login" type="login"></LoginForm>
    </div>
</template>

<script>
import LoginForm from '@/components/global/LoginForm.vue';

export default {
    components: {
        LoginForm
    },

    methods: {
        login(data) {
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
                console.log(error.response.data);

                this.$alert(error.response.data)
            });
        }
    }
};
</script>