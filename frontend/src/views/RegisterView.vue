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
            this.$http.post('/accounts/registration', {
                "email": data.email,
                "password1": data.password1,
                "password2": data.password2
            }).then((response) => {
                console.log(response.data);
            }).catch((error) => {
                console.error(error);
            });
        }
    }
};
</script>