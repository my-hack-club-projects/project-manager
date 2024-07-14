<script setup>
import ProjectCard from '@/components/project/ProjectCard.vue'
import TextButton from '@/components/global/TextButton.vue';
</script>

<template>
  <div class="h-full">
    <div class="container mx-auto p-4">
      <div class="flex items-center">
        <h2 class="text-2xl font-bold mb-4 mt-2">Your projects</h2>
        <TextButton color="blue" class="ml-auto" @click.stop="createProject">
          Create project
        </TextButton>
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
          You have no projects yet. Click <button @click.stop="createProject" class="text-blue-500">here</button> to
          create
          one.
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  components: {
    ProjectCard,
    TextButton,
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
      });
    }
  },
  async created() {
    // For testing, add a new category with 5 projects.
    if (this.$isDevelopment) {
      this.categories.push({
        id: 0,
        name: 'Test category',
        order: 0,
        projects: Array.from({ length: 5 }, (_, i) => ({
          id: i,
          name: `Test looooooooooooooooooong ${i + 1}`,
          description: 'This is a test project',
          category: 0
        }))
      })
    }

    this.$http.get('/api/categories/').then(async categories => {
      const categoriesData = categories.data.data

      for (const category of categoriesData) {
        await this.$http.get(`/api/projects/?category=${category.id}`).then(projects => {
          category.projects = projects.data.data
          this.categories.push(category)
        })
      }

    }).then(() => {
      this.categories.sort((a, b) => a.order - b.order)
    }).catch(error => {
      if (error.response.status === 401 || error.response.status === 403) {
        this.$router.push('/login/')
      }
    })
  }
}
</script>

<style>
.container {
  max-width: 800px;
}
</style>