<template>
    <div @click="onSessionInfoClicked"
        class="container flex items-center justify-between mx-auto p-4 bg-slate-200 rounded-lg shadow-md">
        <div class="flex items-center">
            <h2 class="text-3xl font-bold mb-4 mt-2 w-full">{{ project.name }}</h2>
            <button @click="editProject" class="ml-2">
                <svg class="feather feather-edit" fill="none" height="24" stroke="currentColor" stroke-linecap="round"
                    stroke-linejoin="round" stroke-width="2" viewBox="0 0 24 24" width="24"
                    xmlns="http://www.w3.org/2000/svg">
                    <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" />
                    <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z" />
                </svg>
            </button>
            <button @click="deleteProject" class="ml-2">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
                    <path
                        d="M3 6v18h18v-18h-18zm5 14c0 .552-.448 1-1 1s-1-.448-1-1v-10c0-.552.448-1 1-1s1 .448 1 1v10zm5 0c0 .552-.448 1-1 1s-1-.448-1-1v-10c0-.552.448-1 1-1s1 .448 1 1v10zm5 0c0 .552-.448 1-1 1s-1-.448-1-1v-10c0-.552.448-1 1-1s1 .448 1 1v10zm4-18v2h-20v-2h5.711c.9 0 1.631-1.099 1.631-2h5.315c0 .901.73 2 1.631 2h5.712z" />
                </svg>
            </button>
        </div>
        <div class="flex flex-col items-center p-2 bg-slate-100 rounded-md shadow-sm w-full hover:cursor-pointer">
            <div class="flex items-center justify-start w-full">
                <button @click.stop="onPauseButtonClicked" class="rounded-full p-1 flex items-center justify-center">
                    <div
                        class="p-4 mx-2 flex flex-row items-center gap-2 justify-center bg-gradient-to-br from-cyan-400 to-blue-500 rounded-full shadow-lg hover:cursor-pointer hover:drop-shadow-xl hover:bg-red-600 hover:scale-105">
                        <svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 448 512"
                            class="text-slate-200" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg">
                            <path
                                d="M144 479H48c-26.5 0-48-21.5-48-48V79c0-26.5 21.5-48 48-48h96c26.5 0 48 21.5 48 48v352c0 26.5-21.5 48-48 48zm304-48V79c0-26.5-21.5-48-48-48h-96c-26.5 0-48 21.5-48 48v352c0 26.5 21.5 48 48 48h96c26.5 0 48-21.5 48-48z">
                            </path>
                        </svg>
                    </div>
                </button>
                <div class="flex flex-col ml-2 ">
                    <h3 class="text-lg font-bold">Active session</h3>
                    <p class="text-gray-500">session name here</p>
                </div>
            </div>

            <!-- session progress bar -->
            <div class="w-full bg-slate-300 h-2 rounded-full mt-2">
                <div class="bg-gradient-to-br from-cyan-400 to-blue-500 h-2 rounded-full w-3/12"></div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    props: {
        project: Object,
    },
    methods: {
        onSessionInfoClicked() {
            console.log('Div clicked');
        },
        onPauseButtonClicked(event) {
            console.log('Pause button clicked');

            event.stopPropagation();
        },

        editProject() {
            const projectName = prompt('Enter new project name', this.project.name);

            if (!projectName) {
                return;
            }

            this.$http.put(`/api/projects/${this.project.id}/`, {
                name: projectName,
            }).then(response => {
                this.project.name = response.data.data.name;
            }).catch(error => {
                alert(error.response.data.message);
            });
        },

        deleteProject() {
            if (!confirm('Are you sure you want to delete this project?')) {
                return;
            }

            this.$http.delete(`/api/projects/${this.project.id}/`).then(() => {
                this.$router.push('/projects/');
            }).catch(error => {
                alert(error.response.data.message);
            });
        },
    }
}
</script>

<style scoped>
.hover\:cursor-pointer:hover {
    cursor: pointer;
}
</style>