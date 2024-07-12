<script setup>
import ProjectCard from '@/components/project/ProjectCard.vue'
</script>

<template>
  <div class="h-full">
    <div class="container mx-auto p-4">
      <div class="flex items-center">
        <h2 class="text-2xl font-bold mb-4 mt-2">Your projects</h2>
        <button @click="createProject"
          class="bg-gradient-to-br from-cyan-300 to-blue-600 text-white font-bold py-2 px-4 rounded-lg ml-auto">
          Create project
        </button>
      </div>
      <div class="flex flex-col">
        <div v-for="(category, index) in categories" :key="index" class="py-4">
          <h3 class="text-sm font-bold mb-2">{{ category.name }}</h3>

          <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            <ProjectCard v-for="(project, index) in category.projects" :key="index" :category="category"
              :project="project" />
          </div>
        </div>

        <div v-if="categories.length === 0" class="text-center text-gray-500 mt-4">
          You have no projects yet. Click <button @click="createProject" class="text-blue-500">here</button> to create
          one.
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
  methods: {
    createProject() {
      const defaultCategory = this.categories[0] // TODO: Add default_category field to the user endpoint

      this.$http.post('/api/projects/', {
        name: 'New project',
        category: defaultCategory.id
      }).then(response => {
        const project = response.data.data
        this.$router.push(`/projects/${defaultCategory.id}/${project.id}/view`)
      }).catch(error => {
        alert(error.response.data.message)
      })
    }
  },
  async created() {
    // For testing, add a new category with 5 projects.
    if (process.env.NODE_ENV !== 'production') {
      this.categories.push({
        id: 0,
        name: 'Test category',
        projects: Array.from({ length: 5 }, (_, i) => ({
          id: i,
          name: `Test project ${i + 1}`,
          description: 'This is a test project',
          category: 0
        }))
      })
    }

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