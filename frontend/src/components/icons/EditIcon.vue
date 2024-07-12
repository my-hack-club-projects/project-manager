<template>
    <svg v-show="isHovered"
        class="feather feather-edit absolute top-0 right-0 transform translate-x-2/4 -translate-y-2/4" fill="none"
        height="24" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
        viewBox="0 0 24 24" width="24" xmlns="http://www.w3.org/2000/svg">
        <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" />
        <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z" />
    </svg>
</template>

<script>
export default {
    props: ['isHovered'],
};
</script>
