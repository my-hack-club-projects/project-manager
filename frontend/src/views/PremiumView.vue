<template>
  <div
    class="background bg-gray-200 dark:bg-gray-900 text-gray-800 dark:text-gray-50 w-full h-full flex flex-col items-center justify-center">
    <div class="flex flex-col lg:flex-row items-center justify-center text-6xl font-semibold py-24 w-full gap-4">
      <span class="text-blue-500 font-extrabold glow-light dark:glow-dark">Supercharge</span>your productivity.
    </div>

    <PricingTable />

    <div class="flex flex-col items-center justify-center w-full gap-4 mt-16">
      <span class="text-4xl font-semibold">Features</span>
      <span class="text-gray-500">Discover the features that will help you be more productive.</span>
    </div>

    <div
      class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 items-center justify-center gap-4 my-16 px-4 w-full md:w-auto">
      <Feature title="Feature 1" description="Description of feature 1">
        <img src="@/assets/images/test_feature1.png" alt="Feature 1" />
      </Feature>
      <Feature title="Feature 2" description="Description of feature 2">
        <img src="@/assets/images/test_feature1.png" alt="Feature 2" />
      </Feature>
    </div>
  </div>
</template>

<script>
import PricingTable from '@/components/pricing/PricingTable.vue';
import Feature from '@/components/landing/Feature.vue';

export default {
  components: {
    PricingTable,
    Feature,
  },
}
</script>

<style>
.glow-dark {
  text-shadow: 0rem 0rem 4rem rgb(2, 2, 255);
}

.glow-light {
  text-shadow: 0rem 0rem 4rem rgb(87, 132, 255);
}

.background {
  min-height: 100vh;
}
</style>
