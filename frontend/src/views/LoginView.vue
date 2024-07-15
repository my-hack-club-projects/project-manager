<template>
    <!-- todo disable scrolling -->
    <div class="flex flex-col items-center h-screen bg-gray-50">
        <LoginForm type="login"></LoginForm>
    </div>
</template>

<script>
import LoginForm from '@/components/global/LoginForm.vue';

export default {
    components: {
        LoginForm
    }
};
</script>