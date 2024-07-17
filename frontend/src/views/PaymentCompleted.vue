<template>
    <div class="flex flex-col items-center h-screen bg-gray-50">
        <div class="flex flex-col items-center py-8">
            <svg v-if="success" width="128" height="128" viewBox="0 0 1024 1024" class="icon" version="1.1"
                xmlns="http://www.w3.org/2000/svg">
                <path
                    d="M905.92 237.76a32 32 0 0 0-52.48 36.48A416 416 0 1 1 96 512a418.56 418.56 0 0 1 297.28-398.72 32 32 0 1 0-18.24-61.44A480 480 0 1 0 992 512a477.12 477.12 0 0 0-86.08-274.24z"
                    fill="#15da00" />
                <path
                    d="M630.72 113.28A413.76 413.76 0 0 1 768 185.28a32 32 0 0 0 39.68-50.24 476.8 476.8 0 0 0-160-83.2 32 32 0 0 0-18.24 61.44zM489.28 86.72a36.8 36.8 0 0 0 10.56 6.72 30.08 30.08 0 0 0 24.32 0 37.12 37.12 0 0 0 10.56-6.72A32 32 0 0 0 544 64a33.6 33.6 0 0 0-9.28-22.72A32 32 0 0 0 505.6 32a20.8 20.8 0 0 0-5.76 1.92 23.68 23.68 0 0 0-5.76 2.88l-4.8 3.84a32 32 0 0 0-6.72 10.56A32 32 0 0 0 480 64a32 32 0 0 0 2.56 12.16 37.12 37.12 0 0 0 6.72 10.56zM230.08 467.84a36.48 36.48 0 0 0 0 51.84L413.12 704a36.48 36.48 0 0 0 51.84 0l328.96-330.56A36.48 36.48 0 0 0 742.08 320l-303.36 303.36-156.8-155.52a36.8 36.8 0 0 0-51.84 0z"
                    fill="#15da00" />
            </svg>
            <svg v-else fill="#fa1201" width="128" height="128" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path
                    d="M15.71,8.29a1,1,0,0,0-1.42,0L12,10.59,9.71,8.29A1,1,0,0,0,8.29,9.71L10.59,12l-2.3,2.29a1,1,0,0,0,0,1.42,1,1,0,0,0,1.42,0L12,13.41l2.29,2.3a1,1,0,0,0,1.42,0,1,1,0,0,0,0-1.42L13.41,12l2.3-2.29A1,1,0,0,0,15.71,8.29Zm3.36-3.36A10,10,0,1,0,4.93,19.07,10,10,0,1,0,19.07,4.93ZM17.66,17.66A8,8,0,1,1,20,12,7.95,7.95,0,0,1,17.66,17.66Z" />
            </svg>
            <h1 class="text-3xl font-bold mt-8">
                <span v-if="success">Success!</span>
                <span v-else>Something went wrong!</span>
            </h1>

            <div v-if="success" class="flex flex-col items-center text-gray-500 mt-1">
                <p class="mt-4">Thank you for purchasing Premium!</p>
            </div>
            <div v-else class="flex flex-col items-center text-gray-500 mt-1">
                <p class="mt-4">The callback url is invalid or the session expired.</p>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'PaymentCompleted',

    data() {
        return {
            success: this.$route.params.success == 'success'
        };
    }
};
</script>