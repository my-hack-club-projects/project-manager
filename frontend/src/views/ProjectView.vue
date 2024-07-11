<template>
  <div class="h-full py-4">
    <SessionInfo />

    <div class="container mx-auto mt-6">
      <h2 class="text-2xl font-bold mb-4 mt-2">Tasks</h2>
      <div class="flex flex-col">
        <TaskContainer v-for="(container, index) in taskContainers" :key="index" :title="container.title"
          :is_completed="container.is_completed" :tasks="container.tasks" />
      </div>
    </div>
  </div>
</template>

<script>
import TaskContainer from '../components/task/TaskContainer.vue'
import SessionInfo from '../components/project/SessionInfo.vue'
import axios from 'axios'

export default {
  components: {
    TaskContainer,
    SessionInfo
  },
  data() {
    return {
      taskContainers: []
    }
  },
  async created() {
    const projectId = this.$route.params.projectId
    try {
      // Get all task containers
      const { data: containers } = await axios.get(`/api/projects/${projectId}/taskcontainers`)
      // Get all tasks within them
      const containersWithTasks = await Promise.all(containers.map(async container => {
        const { data: tasks } = await axios.get(`/api/taskcontainers/${container.id}/tasks`)
        return { ...container, tasks }
      }))
      // Log the data to the console (formatted as JSON)
      console.log(JSON.stringify(containersWithTasks, null, 2))
      // Set the taskContainers data property to the processed data
      this.taskContainers = containersWithTasks
    } catch (error) {
      console.error('Error fetching data:', error)
    }
  }
}
</script>

<style scoped>
.container {
  max-width: 800px;
}
</style>
