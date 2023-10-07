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
                item-key="metadata.ProjectRef"
                class="elevation-1"
                multi-sort
                :items-per-page="15"
                :sort-by="['metadata.ProjectRef']"
                :sort-desc="[false, true]"
                height="600px" width="100%"
        >            
            <template v-slot:body="{ items }">
                 <tr v-for="item in items" :key="item.metadata.ProjectRef">
                    <td>{{ item.metadata.ProjectRef }}</td>
                    <td class="truncate">{{ item.metadata.ProjectName }}</td>   
                    <td class="truncate">{{ item.metadata.ProjectGroup }}</td>
                    <td>
                        <StatusIndicatorLocal :status="item.indicators[0].value" :pulse="false"/>
                    </td>
                    <td>
                        <StatusIndicatorLocal :status="item.indicators[1].value" :pulse="false"/>
                    </td>   
                    <td>
                        <StatusIndicatorLocal :status="item.indicators[2].value" :pulse="false"/>
                    </td>  
                    <td>
                        <StatusIndicatorLocal :status="item.indicators[3].value" :pulse="false"/>
                    </td>   
                    <td>
                        <StatusIndicatorLocal :status="item.indicators[4].value" :pulse="false"/>
                    </td>                                                           
                    <td>
                        <StatusIndicatorLocal :status="item.indicators[5].value" :pulse="false"/>
                    </td>                   
                </tr> 
            </template>        
        </v-data-table>
    </div>
</template>

<!--
                        <td><v-icon large @click="deleteFob(item)"> mdi-access-point-remove </v-icon>
-->

<script>
    import Vue from 'vue'
    import VueLogger from 'vuejs-logger'
    import RimsdashAPI from "@/api/RimsdashAPI"
    import StatusIndicatorLocal from '../components/StatusIndicatorLocal.vue'    

    Vue.use(VueLogger)

    export default {
        name: 'Projects',
        components:{
            StatusIndicatorLocal: StatusIndicatorLocal
        },           
        data() {
            return {

                loading: false,

                projects: [],

                filteredId: null,
                filteredTitle: null,

                projectsTableHeaders: [
                    { text: 'Id', value: 'metadata.ProjectRef', width: '7%' },
                    { text: 'Title', value: 'metadata.ProjectName', width: '20%' },                    
                    { text: 'Group', value: 'metadata.ProjectGroup', width: '10%' },                 
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
                this.projects = await this.retrieveAllProjectStates()
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

            async retrieveDefaultProjectState() {
                let project_state = [];

                //retrieve values to populate dropdown
                try {
                    project_state = await RimsdashAPI.getDefaultProjectState()
                } catch (error) {
                    Vue.$log.info("API call getState FAILED")                       
                }             
                Vue.$log.info("default project state retrieved")
                Vue.$log.info("retrieved project name:  "  + project_state.metadata.ProjectName)
                return project_state
            },            

            async retrieveAllProjectStates(user_login) {
                console.log("retrieving project states");
                let project_states = [ {} ];

                //retrieve values to populate dropdown
                try {
                    project_states = await RimsdashAPI.getAllProjectStates()
                } catch (error) {
                    Vue.$log.info("API call FAILED")                       
                    project_states = [ this.default_project_state ];
                }             
                Vue.$log.info("project states retrieved for:  "  + user_login) 
                Vue.$log.info("first project name:  "  + project_states[0].metadata.ProjectName)  
                return project_states
            },            
            
            fill_default_headers() {
                //iterate through indicator labels in default state
                //assign headers based on this
                for (const item of this.default_project_state.indicator_labels) {
                    this.projectsTableHeaders.push( { text: item, value: '' } )                
                }
                Vue.$log.info(this.projectsTableHeaders) 
            },
        },
        mounted: async function() {
            Vue.$log.info("waiting")
            this.loading = true
            //sleep 5 sec
            await new Promise(r => setTimeout(r, 2000));

            this.fill_default_headers()

            this.refresh()
            Vue.$log.info("recieved")            
            //Vue.$log.info(this.projects)  
           // Vue.$log.info(this.projects[0].metadata.ProjectName)  
        },     

        created: async function() {
            //retrieve values to populate dropdown
            Vue.$log.info("P initalising")
            this.default_user_state = await this.retrieveDefaultUserState()
            this.default_project_state = await this.retrieveDefaultProjectState()
            Vue.$log.info("P initalised")              
        }        

    }
</script>

<style>
    .truncate200 {
        max-width: 200px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .truncate {
        max-width: 1px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

</style>