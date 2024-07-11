<template>
  <div class="h-full py-4">
    <SessionInfo />

    <div class="container mx-auto mt-6">
      <h2 class="text-2xl font-bold mb-4 mt-2">Tasks</h2>
      <div class="flex flex-col">
        <TaskContainer />
        <TaskContainer />
      </div>
    </div>
  </div>
</template>

<script>
import TaskContainer from '../components/task/TaskContainer.vue'
import SessionInfo from '../components/project/SessionInfo.vue'

export default {
  components: {
    TaskContainer,
    SessionInfo
  }
}
</script>

<style scoped>
.container {
  max-width: 800px;
}
</style>