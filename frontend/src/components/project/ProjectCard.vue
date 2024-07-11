<!-- ProjectCard.vue -->

<template>
    <router-link :to="`${category.id}/${project.id}/view`"
        class="bg-gradient-to-br from-cyan-300 to-blue-600 rounded-lg shadow-lg p-4 aspect-video text-left">
        <h3 class="text-lg text-white font-bold h-full">{{ project.name }}</h3>
    </router-link>
</template>

<script>
export default {
    props: {
        category: Object,
        project: Object
    }
}
</script>