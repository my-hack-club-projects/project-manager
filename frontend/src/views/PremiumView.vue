<template>
  <div
    class="bg-gray-100 dark:bg-gray-900 text-gray-800 dark:text-gray-50 w-full h-full flex flex-col items-center justify-center">
    <div class="flex flex-col lg:flex-row items-center justify-center text-6xl font-semibold py-24 w-full gap-4">
      <span class="text-blue-500 font-extrabold glow-light dark:glow-dark">Supercharge</span>your productivity.
    </div>

    <PricingTable />
  </div>
</template>

<script>
import PricingTable from '@/components/pricing/PricingTable.vue';

export default {
  components: {
    PricingTable,
  },
}
</script>

<style>
.glow-dark {
  text-shadow: 0rem 0rem 2rem rgb(2, 2, 255);
}

.glow-light {
  text-shadow: 0rem 0rem 2rem rgb(87, 132, 255);
}
</style>
