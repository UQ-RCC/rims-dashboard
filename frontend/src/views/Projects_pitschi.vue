<template>
    <div>
        <v-progress-linear
            color="primary accent-4"
            indeterminate
            rounded
            height="4"
            :active="loading"
        ></v-progress-linear>
        <div>
            <v-breadcrumbs
                :items="nav_items" large
                divider=">"
            ></v-breadcrumbs>
            <div>
                <v-row>
                    <v-col cols="20" sm="8" md="5">
                        <v-text-field
                            v-model="filteredTitle"
                            append-icon="mdi-magnify"
                            label="Search By Title"
                            single-line
                            hide-details
                            @keydown.enter.prevent="filterByTitle"
                        ></v-text-field>
                    </v-col>
                    <v-col cols="12" sm="6" md="3">
                        <v-text-field
                            v-model="filteredCollection"
                            append-icon="mdi-magnify"
                            label="Search By Collection"
                            single-line
                            hide-details
                            @keydown.enter.prevent="filterByCollection"
                        ></v-text-field>
                    </v-col>
                    <v-col cols="12" sm="6" md="3">
                        <v-text-field
                            v-model="filteredId"
                            append-icon="mdi-magnify"
                            label="Search By ID"
                            single-line
                            hide-details
                            @keydown.enter.prevent="filterById"
                            :rules="numberRules"
                        ></v-text-field>
                    </v-col>
                </v-row>
            </div>
            <v-data-table
                :headers="projectsTableHeaders"
                :items="projects"
                item-key="id"
                class="elevation-1"
                multi-sort
                :items-per-page="10"
                :sort-by="['id']"
                :sort-desc="[false, true]"
                height="400px" width="100%"
            >
                <template #item.projectlink="{ item }">
                    <a :href="item.projectlink">
                    {{ item.id }}
                    </a>
                </template>

                <template #item.collectionlink="{ item }">
                    <a :href="item.collectionlink">
                    {{ item.collection }}
                    </a>
                </template>
            </v-data-table>
        </div>
        <br />
        <div align="center">
            <v-btn color="primary" :disabled="is_syncing" @click="syncProjects">
                Manually sync projects with PPMS
            </v-btn>
        </div>
    </div>
</template>

<script>
    import Vue from 'vue'
    import ProjectAPI from "@/api/ProjectAPI"

    export default {
        name: 'Projects',

        data() {
            return {
                nav_items: [
                    {
                    text: 'Projects',
                    disabled: false,
                    href: 'projects',
                    }
                ],
                allprojects: [],
                projects: [],
                loading: false,
                pitschionly: true,
                filteredId: null,
                filteredTitle: null,
                filteredCollection: null,
                is_syncing: false,
                projectsTableHeaders: [
                    { text: 'Project Id', value: 'projectlink' },
                    { text: 'Core Id', value: 'coreid' },
                    { text: 'Collection', value: 'collectionlink' },
                    { text: 'Title', value: 'name' },
                ],
                numberRules: [
                    value => value && value >= 0 || 'Must be 0 or a positive number'
                ],
                timer: null,
            }
        },
        methods: {
            async refresh(){
                Vue.$log.info("refresh ...")
                if (this.$keycloak.hasRealmRole("dashboard")){
                    this.loading = true
                    this.allprojects = await ProjectAPI.getProjects()
                    this.allprojects.forEach(aproj => {
                        // this is slow, move it to backend ? 
                        aproj.projectlink = this.$router.resolve({path: '/project'}).href + '?id=' + aproj.id
                        if(aproj.collection){
                            aproj.collectionlink = this.$router.resolve({path: '/collection'}).href + '?id=' + aproj.collection
                        }
                    });
                    if (this.pitschionly) {
                        let pitchiedOnlyProjects = []
                        this.allprojects.forEach(aproj => {
                            if(aproj.collection){
                                pitchiedOnlyProjects.push(aproj)    
                            }
                        });
                        this.projects = pitchiedOnlyProjects
                    } else {
                        this.projects = this.allprojects 
                    }
                    this.loading = false               
                }
                else {
                    Vue.$log.info("not has dashboard access ...")
                }
            },

        

            syncProjects(){
                console.log("Start manual sync")
                ProjectAPI.manualSync()
                this.is_syncing = true
                this.loading = true
                console.log("Finish manual sync")
            }, 

            async filterById(){
                this.projects = []
                if (this.filteredId){
                    this.filteredTitle = null
                    this.filteredCollection = null
                    this.allprojects.forEach(aproj => {
                    if(aproj.id === parseInt(this.filteredId))
                        this.projects = [aproj]
                    })
                } else {
                    this.projects = this.allprojects
                }
            },


            async filterByTitle(){
                this.projects = []
                if (this.filteredTitle){
                    this.filteredId = null
                    this.filteredCollection = null
                    this.allprojects.forEach(aproj => {
                    if(aproj.name.includes(this.filteredTitle )  )
                        this.projects.push(aproj)
                    })
                } else {
                    this.projects = this.allprojects
                }
            },


            async filterByCollection(){
                this.projects = []
                if (this.filteredCollection){
                    this.filteredId = null
                    this.filteredTitle = null
                    this.allprojects.forEach(aproj => {
                    if(aproj.collection.includes(this.filteredCollection) )
                        this.projects.push(aproj)
                    })
                } else {
                    this.projects = this.allprojects
                }
            }

        },
        mounted: async function() {
            this.refresh()
            this.is_syncing = await ProjectAPI.isSyncing()
            this.loading = this.is_syncing
        },
        created: function() {
            this.timer = setInterval(async() => {
                this.is_syncing = await ProjectAPI.isSyncing()
                this.loading = this.is_syncing
            }, 60000)
        },
        destroyed() {
            delete this.timer
        },


    }
</script>