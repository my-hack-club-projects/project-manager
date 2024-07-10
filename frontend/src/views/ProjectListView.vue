<script setup>
import ProjectCard from '@/components/project/ProjectCard.vue'
</script>

<template>
  <div class="container mx-auto p-4">
    <h2 class="text-lg font-bold">Your projects</h2>
    <div class="flex flex-col border-t-2 border-black w-full">
      <div class="py-4">
        <h3 class="text-sm font-bold mb-2">Category 1</h3>
        
        <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
          <ProjectCard />
          <ProjectCard />
          <ProjectCard />
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