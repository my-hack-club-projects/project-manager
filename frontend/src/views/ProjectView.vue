<template>
  <div class="h-full py-4">
    <SessionInfo :archived="locked" :project="project" />

    <div class="container mx-auto mt-6">
      <h2 class="text-2xl font-bold mb-4 mt-2">Tasks</h2>
      <div class="flex flex-col">
        <draggable v-model="taskContainers" @change="onDragEnd" :disabled="locked" :itemKey="container => container.id"
          :options="dragOptions">
          <template #item="{ element }">
            <TaskContainer :locked="locked" :key="element.id" :id="element.id" :title="element.title"
              :is_completed="element.is_completed" :tasks="element.tasks" @delete="deleteTaskContainer"
              @edit="editTaskContainer" />
          </template>
        </draggable>
      </div>

      <AddTaskForm :locked="locked" :placeholder="'New milestone'" @add-task="addTaskContainer" />
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
      locked: true, // locked by default, will be updated in the created hook
      taskContainers: [],
    }
  },
  methods: {
    sort() {
      this.taskContainers.sort((a, b) => a.order - b.order)
    },
    onDragEnd(event) {
      const taskContainersToUpdate = this.taskContainers.map((container, index) => {
        return {
          id: container.id,
          order: index
        }
      })

      this.$http.put(`/api/taskcontainers/bulk_update/`, taskContainersToUpdate).then((response) => {
        for (let i = 0; i < this.taskContainers.length; i++) {
          this.taskContainers[i].order = i
        }

        this.sort()
      });
    },
    addTaskContainer(title) {
      this.$http.post(`/api/taskcontainers/`, {
        project: this.$route.params.projectId,
        title: title,
        order: this.taskContainers.length
      }).then(response => {
        const taskContainer = response.data.data

        taskContainer.tasks = []

        this.taskContainers.push(taskContainer)

        // Scroll to the bottom of the page
        document.getElementById('bottom-spacer').scrollIntoView({ behavior: 'smooth' })

        // Focus on the new task container's add task input
        this.$nextTick(() => {
          const taskContainerElement = document.getElementById(`task-container-${taskContainer.id}`)
          const addTaskInput = taskContainerElement.querySelector('.add-task-input')

          addTaskInput.focus()
        })
      });
    },
    async deleteTaskContainer(taskContainerId) {
      if (!await this.$confirm('Are you sure you want to delete this milestone?', false)) {
        return
      }

      const taskContainerIndex = this.taskContainers.findIndex(container => container.id == taskContainerId)

      this.$http.delete(`/api/taskcontainers/${taskContainerId}/`).then(() => {
        this.taskContainers.splice(taskContainerIndex, 1)
      });
    },
    editTaskContainer(taskContainerId, newTitle) {
      const taskContainerIndex = this.taskContainers.findIndex(container => container.id == taskContainerId)

      this.$http.put(`/api/taskcontainers/${taskContainerId}/`, {
        title: newTitle,
      }).then(response => {
        const newTitleFromResponse = response.data.data.data.title
        this.taskContainers[taskContainerIndex].title = newTitleFromResponse
      });
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
        description: 'Project description very loooooooooooong'
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

    this.$http.get(`/api/projects/${projectId}`).then(project => {
      this.project = project.data.data

      this.$http.get(`/api/taskcontainers/?project=${projectId}`).then(containers => {
        const containersData = containers.data.data

        const containersWithTasks = containersData.map(async container => {
          let tasks = await this.$http.get(`/api/tasks/?task_container=${container.id}`)
          tasks = tasks.data.data

          return { ...container, tasks }
        })

        Promise.all(containersWithTasks).then(containersWithTasks => {
          this.taskContainers = containersWithTasks

          this.sort()
        })
      })
    }).catch(error => {
      if (error.response.status === 404 || error.response.status === 403) {
        this.$router.push('/projects/')
      } else {
        this.$alert('An error occurred while fetching the project data. Please try again later.', error)
      }
    })

    this.$http.get(`/api/categories/${categoryId}/`).then(category => {
      this.locked = category.data.data.locked
    })
  }
}
</script>

<style scoped>
.container {
  max-width: min(800px, 90vw);
}
</style>
