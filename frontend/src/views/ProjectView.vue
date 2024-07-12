<template>
  <div class="h-full py-4">
    <SessionInfo :project="project" />

    <div class="container mx-auto mt-6">
      <h2 class="text-2xl font-bold mb-4 mt-2">Tasks</h2>
      <div class="flex flex-col">
        <TaskContainer v-for="(container, index) in taskContainers" :key="index" :id="container.id"
          :title="container.title" :is_completed="container.is_completed" :tasks="container.tasks"
          @delete="deleteTaskContainer" @edit="editTaskContainer" />
      </div>

      <AddTaskForm :placeholder="'New milestone'" @add-task="addTaskContainer" />
      <div id="bottom-spacer" class="h-64"></div>
    </div>
  </div>
</template>

<script>
import TaskContainer from '../components/task/TaskContainer.vue'
import SessionInfo from '../components/project/SessionInfo.vue'
import AddTaskForm from '../components/task/AddTaskForm.vue';

export default {
  components: {
    TaskContainer,
    AddTaskForm,
    SessionInfo
  },
  data() {
    return {
      project: '',
      taskContainers: []
    }
  },
  methods: {
    addTaskContainer(title) {
      this.$http.post(`/api/taskcontainers/`, {
        project: this.$route.params.projectId,
        title: title,
      }).then(response => {
        const taskContainer = response.data.data

        taskContainer.tasks = []

        this.taskContainers.push(taskContainer)

        // Scroll to the bottom of the page
        document.getElementById('bottom-spacer').scrollIntoView({ behavior: 'smooth' })
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
        const newTitleFromResponse = response.data.data.title
        this.taskContainers[taskContainerIndex].title = newTitleFromResponse
      }).catch(error => {
        alert(error.response.data.message)
      })
    }
  },
  async created() {
    // For testing, add three task containers with varying amounts of tasks
    if (this.$isDevelopment) {
      this.project = {
        id: 1,
        name: 'Project name very loooooooooooong',
      }

      this.taskContainers = [
        {
          id: 0,
          title: 'Test milestone 1',
          is_completed: false,
          tasks: Array.from({ length: 3 }, (_, i) => ({
            id: i,
            title: `Test task ${i + 1}`,
            is_completed: false,
            task_container: 0
          }))
        },
        {
          id: 1,
          title: 'Test milestone 2 with a really really looong name lol',
          is_completed: false,
          tasks: Array.from({ length: 2 }, (_, i) => ({
            id: i,
            title: `Test looooooooooooooooong task ${i + 1}`,
            is_completed: false,
            task_container: 1
          }))
        },
        {
          id: 2,
          title: 'Test milestone 3',
          is_completed: false,
          tasks: Array.from({ length: 1 }, (_, i) => ({
            id: i,
            title: `Test task ${i + 1}`,
            is_completed: false,
            task_container: 2
          }))
        }
      ]

      return
    }

    const categoryId = this.$route.params.categoryId
    const projectId = this.$route.params.projectId

    try {
      const { data: project } = await this.$http.get(`/api/projects/${projectId}`)

      this.project = project

      const { data: containers } = await this.$http.get(`/api/taskcontainers/?project=${projectId}`)
      const containersWithTasks = await Promise.all(containers.map(async container => {
        let { data: tasks } = await this.$http.get(`/api/tasks/?task_container=${container.id}`)

        console.log(tasks)

        return { ...container, tasks }
      }))

      this.taskContainers = containersWithTasks
    } catch (error) {
      console.error('Error fetching data:', error)
    }
  }
}
</script>

<style scoped>
.container {
  max-width: min(800px, 90vw);
}
</style>
