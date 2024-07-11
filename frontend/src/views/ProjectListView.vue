<script setup>
import ProjectCard from '@/components/project/ProjectCard.vue'
</script>

<template>
  <div class="h-full">
    <div class="container mx-auto p-4">
      <h2 class="text-2xl font-bold mb-4 mt-2">Your projects</h2>
      <div class="flex flex-col">
        <!-- Inside this container are the categories such as the one below -->
        <!-- <div class="py-4">
          <h3 class="text-sm font-bold mb-2">Category 1</h3>

          <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            <ProjectCard />
            <ProjectCard />
            <ProjectCard />
          </div>
        </div> -->

        <!-- Iterate through this.categories and hydrate the html -->

        <div v-for="(category, index) in categories" :key="index" class="py-4">
          <h3 class="text-sm font-bold mb-2">{{ category.name }}</h3>

          <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            <ProjectCard v-for="(project, index) in category.projects" :key="index" :project="project" />
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