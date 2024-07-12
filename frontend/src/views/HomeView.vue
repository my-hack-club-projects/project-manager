<template>
  <div class="container mx-auto">
    <h1 class="text-4xl font-bold text-center mt-8">Welcome to my Tailwind CSS Page</h1>
    <p class="text-lg text-center mt-4">This is the Home view</p>
    <div class="flex justify-center mt-8">
      <router-link to="/projects/" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
        Go to Projects
      </router-link>
    </div>
  </div>
</template>

<style>
.container {
  max-width: 800px;
}
</style>