<template>
  <div class="h-full py-4">
    <!-- session info component -->
    <div @click="onSessionInfoClicked"
      class="container flex items-center justify-between mx-auto p-4 bg-slate-200 rounded-lg shadow-md">
      <h2 class="text-3xl font-bold mb-4 mt-2 w-full">A very long descriptive Name of this project</h2>
      <div class="flex flex-col items-center p-2 bg-slate-100 rounded-md shadow-sm w-full hover:cursor-pointer">
        <div class="flex items-center justify-start w-full">
          <button @click.stop="onPauseButtonClicked" class="rounded-full p-1 flex items-center justify-center">
            <div
              class="p-4 mx-2 flex flex-row items-center gap-2 justify-center bg-gradient-to-br from-cyan-400 to-blue-500 rounded-full shadow-lg hover:cursor-pointer hover:drop-shadow-xl hover:bg-red-600 hover:scale-105">
              <svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 448 512"
                class="text-slate-200" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg">
                <path
                  d="M144 479H48c-26.5 0-48-21.5-48-48V79c0-26.5 21.5-48 48-48h96c26.5 0 48 21.5 48 48v352c0 26.5-21.5 48-48 48zm304-48V79c0-26.5-21.5-48-48-48h-96c-26.5 0-48 21.5-48 48v352c0 26.5 21.5 48 48 48h96c26.5 0 48-21.5 48-48z">
                </path>
              </svg>
            </div>
          </button>
          <div class="flex flex-col ml-2 ">
            <h3 class="text-lg font-bold">Active session</h3>
            <p class="text-gray-500">session name here</p>
          </div>
        </div>

        <!-- session progress bar -->
        <div class="w-full bg-slate-300 h-2 rounded-full mt-2">
          <div class="bg-gradient-to-br from-cyan-400 to-blue-500 h-2 rounded-full w-3/12"></div>
        </div>
      </div>
    </div>
    <!-- end session info -->

    <!-- card container -->
    <!-- <div class="container mx-auto mt-6">
      <h2 class="text-2xl font-bold mb-4 mt-2">Tasks</h2>
      <div class="flex flex-col">
        <div class="bg-slate-200 rounded-lg shadow-md px-4 py-2">
          <h3 class="text-sm font-bold mb-2">Some big milestone</h3>

          <div class="flex items-center mb-4">
            <input id="default-checkbox" disabled readonly checked type="checkbox" value="1"
              class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 mr-2">
            <label for="default-checkbox" class="text-sm font-bold">Step one</label>
          </div>

          <div class="flex items-center my-2">
            <input id="default-checkbox" disabled readonly checked type="checkbox" value="1"
              class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 mr-2">
            <span class="text-sm font-bold">Another step</span>
          </div>

          <div class="flex items-center my-2">
            <input id="default-checkbox" disabled readonly checked type="checkbox" value="1"
              class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 mr-2">
            <span class="text-sm font-bold">Almost there!</span>
          </div>
        </div>
      </div>
    </div> -->

    <!-- new card container -->
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

export default {
  components: {
    TaskContainer
  },
  methods: {
    onSessionInfoClicked() {
      console.log('Div clicked');
    },
    onPauseButtonClicked(event) {
      console.log('Pause button clicked');

      event.stopPropagation();
    }
  }
}
</script>

<style scoped>
.container {
  max-width: 800px;
}

.hover\:cursor-pointer:hover {
  cursor: pointer;
}
</style>