<script setup>
import ProjectCard from '@/components/project/ProjectCard.vue'
</script>

<template>
  <div class="h-full">
    <div class="container mx-auto p-4">
      <div class="flex items-center">
        <h2 class="text-2xl font-bold mb-4 mt-2">Your projects</h2>
        <button class="bg-gradient-to-br from-cyan-300 to-blue-600 text-white font-bold py-2 px-4 rounded-lg ml-auto">
          Create project
        </button>
      </div>
      <div class="flex flex-col">
        <div v-for="(category, index) in categories" :key="index" class="py-4">
          <h3 class="text-sm font-bold mb-2">{{ category.name }}</h3>

          <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            <ProjectCard v-for="(project, index) in category.projects" :key="index" :category="category" :project="project" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  components: {
    ProjectCard
  },
  data() {
    return {
      categories: []
    }
  },
  async created() {
    const categories = await this.$http.get('/api/categories/')

    for (const category of categories.data) {
      const projects = await this.$http.get(`/api/projects/?category=${category.id}`)
      category.projects = projects.data

      this.categories.push(category)
    }
  }
}
</script>

<style>
.container {
  max-width: 800px;
}
</style>