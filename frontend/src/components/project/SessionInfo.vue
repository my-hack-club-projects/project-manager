    <template>
        <div @click="onSessionInfoClicked"
            class="container grid grid-cols-1 md:grid-cols-2 items-center justify-center mx-auto p-4 gap-4 bg-slate-200 rounded-lg shadow-md hover:cursor-pointer">
            <h2 class="text-3xl truncate font-bold mb-4 mt-2 w-full">{{ project.name }}</h2>

            <div class="flex flex-col items-center p-2 bg-slate-100 rounded-md shadow-sm text-nowrap w-full">
                <div class="flex items-center justify-start w-full">
                    <button @click.stop="onPauseButtonClicked"
                        class="rounded-full p-1 flex items-center justify-center">
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
                    <div class="flex flex-col ml-2 mr-4">
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
import EditIcon from '../icons/EditIcon.vue';

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

        editProject(event) {
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

            event.stopPropagation();
        },

        deleteProject(event) {
            if (!confirm('Are you sure you want to delete this project?')) {
                return;
            }

            this.$http.delete(`/api/projects/${this.project.id}/`).then(() => {
                this.$router.push('/projects/');
            }).catch(error => {
                alert(error.response.data.message);
            });

            event.stopPropagation();
        },
    },
}
</script>

<style scoped>
.hover\:cursor-pointer:hover {
    cursor: pointer;
}
</style>