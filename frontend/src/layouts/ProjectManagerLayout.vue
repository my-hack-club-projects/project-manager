<template>
  <div class="flex h-screen flex-col">
    <header class="bg-gray-800 text-white py-4 px-6">
      <div class="flex justify-between items-center">
        <div class="flex items-center">
          <h1 class="text-2xl font-bold mr-4">Project Manager</h1>
          <nav class="hidden sm:block">
            <ul class="flex space-x-4">
              <li><router-link to="/projects/">Projects</router-link></li>
              <li><router-link to="/projects/analytics/">Analytics</router-link></li>
            </ul>
          </nav>
        </div>
        <button class="rounded-full bg-white w-8 h-8"></button>
      </div>
    </header>

    <main class="flex-1 bg-gray-100">
      <router-view></router-view>
    </main>
  </div>
</template>

<script>
export default {
  name: 'ProjectManagerLayout',
};
</script>

<style scoped></style>
