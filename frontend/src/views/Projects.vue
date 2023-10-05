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
                </v-col>            
            </v-row>                    
        </div>
    </div>
</template>

<script>
    import Vue from 'vue'
    import VueLogger from 'vuejs-logger'
    import RimsdashAPI from "@/api/RimsdashAPI"

    Vue.use(VueLogger)

    export default {
        name: 'Projects',
        data() {
            return {

                loading: false,

                projects: [],

                filteredId: null,
                filteredTitle: null,

                projectsTableHeaders: [
                    { text: 'Project Id', value: 'projectlink' },
                    { text: 'Core Id', value: 'coreid' },
                    { text: 'Collection', value: 'collectionlink' },
                    { text: 'Title', value: 'name' },
                ],

                numberRules: [
                    value => value && value >= 0 || 'Must be 0 or a positive number'
                ],

            }
        },
        methods: {
            async refresh(){
                Vue.$log.info("P refreshing ...")
                this.loading = true
                this.projects = await this.retrieveUserProjectStates('myusername')
                //this.projects = await ProjectAPI.getProjects()
                this.loading = false       
                Vue.$log.info("P refresh complete...")                                         
                Vue.$log.info(this.projects)  
                Vue.$log.info(this.projects[0].metadata.ProjectName)                 
            },

            async retrieveDefaultUserState() {
                let user_state = { };

                //retrieve values to populate dropdown
                try {
                    user_state = await RimsdashAPI.getDefaultUserState()
                } catch (error) {
                    Vue.$log.info("API call getState FAILED")                       
                }             
                Vue.$log.info("default user state retrieved:  " ) 
                Vue.$log.info("retrieved user name:  "  + user_state.metadata.name)  
                return user_state
            }, 

            async retrieveDefaultUserProjectStates() {
                let project_states = [];

                //retrieve values to populate dropdown
                try {
                    project_states = await RimsdashAPI.getDefaultProjectStates()
                } catch (error) {
                    Vue.$log.info("API call getState FAILED")                       
                }             
                Vue.$log.info("default project state retrieved")
                Vue.$log.info("retrieved project name:  "  + project_states[0].metadata.ProjectName)
                return project_states
            },            

            async retrieveUserProjectStates(user_login) {
                console.log("retrieving project states for  " + user_login);
                let project_states = [ {} ];

                //retrieve values to populate dropdown
                try {
                    project_states = await RimsdashAPI.getUserProjectStates(user_login)
                } catch (error) {
                    Vue.$log.info("API call getState FAILED")                       
                    project_states = this.default_project_states;
                }             
                Vue.$log.info("project states retrieved for:  "  + user_login) 
                Vue.$log.info("first project name:  "  + project_states[0].metadata.ProjectName)  
                return project_states
            },            
            
        },
        mounted: async function() {
            Vue.$log.info("waiting")
            await new Promise(r => setTimeout(r, 5000));
            this.refresh()
            Vue.$log.info("recieved")            
            //Vue.$log.info(this.projects)  
           // Vue.$log.info(this.projects[0].metadata.ProjectName)  
        },     

        created: async function() {
            //retrieve values to populate dropdown
            Vue.$log.info("P initalising")
            this.default_user_state = await this.retrieveDefaultUserState()
            this.default_project_states = await this.retrieveDefaultUserProjectStates()
            Vue.$log.info("P initalised")              
        }        

    }
</script>