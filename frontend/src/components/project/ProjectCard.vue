<!-- ProjectCard.vue -->

<template>
    <router-link :to="`${category.id}/${project.id}/view`"
        :class="`${this.colors[this.color]} text-white hover:bg-transparent font-semibold py-2 px-4 border border-transparent rounded shadow-md aspect-video`">
        <h3 class="text-lg font-bold h-full">{{ project.name }}</h3>
    </router-link>
</template>

<script>
export default {
    props: {
        category: Object,
        project: Object,
        color: {
            type: String,
            default: "blue"
        },
    },
    data() {
        return {
            colors: {
                "red": "bg-red-500 hover:text-red-500 hover:border-red-500",
                "green": "bg-green-500 hover:text-green-500 hover:border-green-500",
                "blue": "bg-blue-500 hover:text-blue-500 hover:border-blue-500",
                "teal": "bg-teal-500 hover:text-teal-500 hover:border-teal-500",
                "yellow": "bg-yellow-500 hover:text-yellow-500 hover:border-yellow-500",
                "orange": "bg-orange-500 hover:text-orange-500 hover:border-orange-500",
                "indigo": "bg-indigo-500 hover:text-indigo-500 hover:border-indigo-500",
                "purple": "bg-purple-500 hover:text-purple-500 hover:border-purple-500",
                "pink": "bg-pink-500 hover:text-pink-500 hover:border-pink-500",
                "gray": "bg-gray-500 hover:text-gray-500 hover:border-gray-500",
                "black": "bg-black hover:text-black hover:border-black",
                "white": "bg-white hover:text-white hover:border-white",
            }
        };
    }
}
</script>