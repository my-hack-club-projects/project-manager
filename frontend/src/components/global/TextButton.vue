<template>
    <!-- previously used :class="`bg-transparent hover:bg-[${this.color}] text-[${this.color}] font-semibold hover:text-white py-2 px-4 border border-[${this.color}] hover:border-transparent rounded shadow-md`"> -->
    <button @click="this.emit('click')"
        :class="`bg-transparent ${this.colors[this.color]} font-semibold hover:text-white py-2 px-4 border hover:border-transparent rounded shadow-md`">
        <slot></slot>
    </button>
</template>

<script>
export default {
    name: 'TextButton',
    slots: ['default'],
    props: {
        disabled: Boolean,
        color: String,
    },
    data() {
        return {
            colors: {
                "red": "hover:bg-red-500 text-red-500 border-red-500",
                "green": "hover:bg-green-500 text-green-500 border-green-500",
                "blue": "hover:bg-blue-500 text-blue-500 border-blue-500",
                "teal": "hover:bg-teal-500 text-teal-500 border-teal-500",
                "yellow": "hover:bg-yellow-500 text-yellow-500 border-yellow-500",
                "orange": "hover:bg-orange-500 text-orange-500 border-orange-500",
                "indigo": "hover:bg-indigo-500 text-indigo-500 border-indigo-500",
                "purple": "hover:bg-purple-500 text-purple-500 border-purple-500",
                "pink": "hover:bg-pink-500 text-pink-500 border-pink-500",
                "gray": "hover:bg-gray-500 text-gray-500 border-gray-500",
                "black": "hover:bg-black text-black border-black",
                "white": "hover:bg-white text-white border-white",
            }
        };
    }
}
</script>