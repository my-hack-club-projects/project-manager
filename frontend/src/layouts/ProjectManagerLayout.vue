<template>
  <header class="bg-gray-800 text-white py-4 px-6">
    <div class="flex justify-between items-center">
      <h1 class="text-2xl font-bold">Project Manager Layout</h1>
      <nav>
        <ul class="flex space-x-4">
          <li><router-link to="/projects">Projects</router-link></li>
          <li><router-link to="/projects/analytics">Analytics</router-link></li>
        </ul>
      </nav>
    </div>
  </header>

  <main>
    <router-view></router-view>
  </main>
</template>

<script>
export default {
  name: 'LandingPageLayout',
};
</script>

<style scoped>
</style>
