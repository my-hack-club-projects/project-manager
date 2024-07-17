<template>
  <div
    class="bg-gray-100 dark:bg-gray-900 text-gray-800 dark:text-gray-50 w-full h-full flex flex-col items-center justify-center">
    <div class="flex flex-col lg:flex-row items-center justify-center text-6xl font-semibold py-24 w-full gap-4">
      <span class="text-blue-500 font-extrabold glow-light dark:glow-dark">Supercharge</span>your productivity.
    </div>

    <div class="flex flex-col lg:flex-row items-center justify-center gap-4 w-full">

      <div
        class="w-full max-w-sm p-4 bg-white border border-gray-200 rounded-lg shadow sm:p-8 dark:bg-gray-800 dark:border-gray-700">
        <h5 class="mb-4 text-xl font-medium text-gray-500 dark:text-gray-400">Standard plan</h5>
        <div class="flex items-baseline text-gray-900 dark:text-white">
          <span class="text-3xl font-semibold">$</span>
          <span class="text-5xl font-extrabold tracking-tight">49</span>
          <span class="ms-1 text-xl font-normal text-gray-500 dark:text-gray-400">/month</span>
        </div>
        <ul role="list" class="space-y-5 my-7">
          <li class="flex items-center">
            <svg class="flex-shrink-0 w-4 h-4 text-blue-700 dark:text-blue-500" aria-hidden="true"
              xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
              <path
                d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5Zm3.707 8.207-4 4a1 1 0 0 1-1.414 0l-2-2a1 1 0 0 1 1.414-1.414L9 10.586l3.293-3.293a1 1 0 0 1 1.414 1.414Z" />
            </svg>
            <span class="text-base font-normal leading-tight text-gray-500 dark:text-gray-400 ms-3">Some feature
              here</span>
          </li>

        </ul>
        <TextButton color="blue" class="w-full">Choose plan</TextButton>
      </div>
    </div>
  </div>
</template>

<script>
import PricingTable from '@/components/stripe/PricingTable.vue'
import TextButton from '@/components/global/TextButton.vue';

export default {
  components: {
    PricingTable,
    TextButton,
  },
}
</script>

<style>
.glow-dark {
  text-shadow: 0rem 0rem 2rem rgb(2, 2, 255);
}

.glow-light {
  text-shadow: 0rem 0rem 2rem rgb(60, 60, 255);
}
</style>
