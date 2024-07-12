<template>
  <div class="h-full py-4">
    <SessionInfo :project="project" />

    <div class="container mx-auto mt-6">
      <h2 class="text-2xl font-bold mb-4 mt-2">Tasks</h2>
      <div class="flex flex-col">
        <draggable v-model="taskContainersCopy" @end="onDragEnd" :itemKey="container => container.id"
          :options="dragOptions">
          <template #item="{ element }">
            <TaskContainer :key="element.id" :id="element.id" :title="element.title"
              :is_completed="element.is_completed" :tasks="element.tasks" @delete="deleteTaskContainer"
              @edit="editTaskContainer" />
          </template>
        </draggable>
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
import draggable from 'vuedraggable';

export default {
  components: {
    TaskContainer,
    AddTaskForm,
    SessionInfo,
    draggable,
  },
  data() {
    return {
      project: '',
      taskContainers: [],
      taskContainersCopy: []
    }
  },
  watch: {
    taskContainers: {
      handler(newVal) {
        this.taskContainersCopy = newVal.slice()
      },
      deep: true,
      immediate: true
    }
  },
  computed: {
    dragOptions() {
      return {
        filter: '.completed',
        disabled: this.taskIsCompleted
      }
    }
  },
  methods: {
    onDragEnd(event) {
      console.log('Dragged task list:', this.taskContainersCopy)
    },
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
    },
    taskIsCompleted() {
      return function (event) {
        const containerId = event.getAttribute('data-id');
        const container = this.taskContainers.find(container => container.id == containerId);
        return container && container.is_completed;
      }
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
          is_completed: true, // Example of a completed container
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
