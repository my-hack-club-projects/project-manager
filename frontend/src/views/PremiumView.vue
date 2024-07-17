<template>
  <div class="bg-gradient-to-br from-gray-800 to-black w-full h-full flex flex-col items-center justify-center">

    <div class="flex items-center justify-center text-6xl font-semibold text-white py-12 w-full">
      <span class="text-blue-500 font-extrabold glow">Supercharge</span>&nbsp;your productivity.
    </div>
  </div>
</template>

<script>
import PricingTable from '@/components/stripe/PricingTable.vue'

export default {
  components: {
    PricingTable
  },
}
</script>

<style>
.glow {
  text-shadow: 0rem 0rem 2rem rgb(2, 2, 255);
}
</style>
