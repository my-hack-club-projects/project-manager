<template>
  <div class="h-full py-4">
    <SessionInfo :project_name="project_name" />

    <div class="container mx-auto mt-6">
      <h2 class="text-2xl font-bold mb-4 mt-2">Tasks</h2>
      <div class="flex flex-col">
        <TaskContainer v-for="(container, index) in taskContainers" :key="index" :id="container.id"
          :title="container.title" :is_completed="container.is_completed" :tasks="container.tasks"
          @delete="deleteTaskContainer" @edit="editTaskContainer" />
      </div>

      <AddTaskForm :placeholder="'New milestone'" @add-task="addTaskContainer" />
    </div>
  </div>
</template>

<script>
import TaskContainer from '../components/task/TaskContainer.vue'
import SessionInfo from '../components/project/SessionInfo.vue'
import AddTaskForm from '@/components/task/AddTaskForm.vue';
import { assert } from 'console';

export default {
  components: {
    TaskContainer,
    AddTaskForm,
    SessionInfo
  },
  data() {
    return {
      project_name: '',
      taskContainers: []
    }
  },
  methods: {
    addTaskContainer(title) {
      this.$http.post(`/api/taskcontainers/`, {
        project: this.$route.params.projectId,
        title: title,
      }).then(response => {
        this.taskContainers.push(response.data.data)
      }).catch(error => {
        alert(error.response.data.message)
      })
    },
    deleteTaskContainer(taskContainerId) {
      const taskContainerIndex = this.taskContainers.findIndex(container => container.id == taskContainerId)

      this.$http.delete(`/api/taskcontainers/${taskContainerId}/`).then(() => {
        this.taskContainers.splice(taskContainerIndex, 1)
      }).catch(error => {
        alert(error.response.data.message)
      })
    },
    editTaskContainer(taskContainerId, newTitle) {
      const taskContainerIndex = this.taskContainers.findIndex(container => container.id == taskContainerId)

      this.$http.put(`/api/taskcontainers/${taskContainerId}/`, {
        title: newTitle,
      }).then(response => {
        this.taskContainers.splice(taskContainerIndex, 1, response.data.data)
      }).catch(error => {
        alert(error.response.data.message)
      })
    }
  },
  async created() {
    const categoryId = this.$route.params.categoryId
    const projectId = this.$route.params.projectId

    try {
      const { data: project } = await this.$http.get(`/api/projects/${projectId}`)

      this.project_name = project.name

      const { data: containers } = await this.$http.get(`/api/taskcontainers/?project=${projectId}`)
      const containersWithTasks = await Promise.all(containers.map(async container => {
        const { data: tasks } = await this.$http.get(`/api/tasks/?task_container=${container.id}`)
        return { ...container, tasks }
      }))

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
