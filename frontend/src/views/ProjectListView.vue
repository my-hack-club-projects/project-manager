<script setup>
import ProjectCard from '@/components/project/ProjectCard.vue'
</script>

<template>
  <div class="bg-gray-100 h-full">
    <div class="container mx-auto p-4">
      <h2 class="text-2xl font-bold mb-4 mt-2">Your projects</h2>
      <div class="flex flex-col">
        <div class="py-4">
          <h3 class="text-sm font-bold mb-2">Category 1</h3>

          <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            <ProjectCard />
            <ProjectCard />
            <ProjectCard />
          </div>
        </div>

        <div class="py-4">
          <h3 class="text-sm font-bold mb-2">Category 2</h3>

          <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            <ProjectCard />
            <ProjectCard />
            <ProjectCard />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style>
.container {
  max-width: 800px;
}
</style>