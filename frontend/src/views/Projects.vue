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
                        v-model="filteredGroup"
                        append-icon="mdi-magnify"
                        label="Search By Group"
                        single-line
                        hide-details
                        @keydown.enter.prevent="filterByGroup"
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
                :items-per-page="15"
                :sort-by="['id']"
                :sort-desc="[false, true]"
                height="600px" width="100%"
        >            
            <template v-slot:body="{ items }">
                 <tr v-for="item in items" :key="item.id">
                    <td>{{ item.id }}</td>
                    <td class="truncate">{{ item.title }}</td>   
                    <td class="truncate">{{ item.group }}</td>
                    <td>
                        <StatusIndicatorLocal :status="item.project_state[0].ok" :pulse="false"/>
                    </td>
                    <td>
                        <StatusIndicatorLocal :status="item.project_state[0].active" :pulse="false"/>
                    </td>   
                    <td>
                        <StatusIndicatorLocal :status="item.project_state[0].billing" :pulse="false"/>
                    </td>  
                    <td>
                        <StatusIndicatorLocal :status="item.project_state[0].ohs" :pulse="false"/>
                    </td>   
                    <td>
                        <StatusIndicatorLocal :status="item.project_state[0].rdm" :pulse="false"/>
                    </td>                                                           
                    <td>
                        <StatusIndicatorLocal :status="item.project_state[0].phase" :pulse="false"/>
                    </td>                   
                </tr> 
            </template>        
        </v-data-table>
    </div>
</template>

<!--
    search field clear button
    https://stackoverflow.com/questions/2803532/how-do-i-put-a-clear-button-inside-my-html-text-input-box-like-the-iphone-does
    maybe just use v-autocomplete or v-search?
    eg. https://codepen.io/AndrewThian/pen/QdeOVa
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
                projectsFull: [],
                filteredId: null,
                filteredTitle: null,
                filteredGroup: null,

                projectsTableHeaders: [
                    { text: 'Id', value: 'id', width: '4%' },
                    { text: 'Title', value: 'title', width: '20%' },                    
                    { text: 'Group', value: 'group', width: '10%' },                 
                    { text: 'OK', value: '', width: '4%' },                     
                    { text: 'Active', value: '', width: '4%' },  
                    { text: 'Billing', value: '', width: '4%' },  
                    { text: 'OHS', value: '', width: '4%' },  
                    { text: 'RDM', value: '', width: '4%' },                                                                                  
                    { text: 'Phase', value: '', width: '4%' },                     
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
                this.projectsFull = await this.retrieveAllProjects()
                //this.projects = await ProjectAPI.getProjects()
                this.loading = false       
                this.projects = this.projectsFull
                Vue.$log.info("P refresh complete...")                                         
                Vue.$log.info(this.projects)  
                Vue.$log.info(this.projects[0].title)                 
            },

            async filterById(){
                this.projects = []
                if (this.filteredId){
                    this.filteredTitle = null
                    this.filteredGroup = null                    
                    this.projectsFull.forEach(aproj => {
                    if(aproj.id === parseInt(this.filteredId))
                        this.projects = [aproj]
                    })
                } else {
                    this.projects = this.projectsFull
                }
            },

            async filterByTitle(){
                this.projects = []
                if (this.filteredTitle){
                    this.filteredId = null
                    this.filteredGroup = null
                    this.projectsFull.forEach(aproj => {
                    if(aproj.title.toLowerCase().includes(this.filteredTitle.toLowerCase()) )
                        this.projects.push(aproj)
                    })
                } else {
                    this.projects = this.projectsFull
                }
            },

            async filterByGroup(){
                this.projects = []
                if (this.filteredGroup){
                    this.filteredId = null
                    this.filteredTitle = null
                    this.projectsFull.forEach(aproj => {
                        if(aproj.group.toLowerCase().includes(this.filteredGroup.toLowerCase()) )
                            this.projects.push(aproj)
                    })
                } else {
                    this.projects = this.projectsFull
                }
            },

            async retrieveAllProjects() {
                console.log("retrieving project states");
                let __projects = [ {} ];

                //retrieve values to populate dropdown
                try {
                    __projects = await RimsdashAPI.getAllProjectsWithStates()
                } catch (error) {
                    Vue.$log.info("API call FAILED")                       
                }             
                Vue.$log.info("first project title:  "  + __projects[0].title)  
                return __projects
            },            
            
            caseCompare(a, b) {
                return typeof a === 'string' && typeof b === 'string'
                    ? a.localeCompare(b, undefined, { sensitivity: 'accent' }) === 0
                    : a === b;
           },
        },
        mounted: async function() {
            Vue.$log.info("P waiting")
            this.loading = true
            //sleep 100ms
            await new Promise(r => setTimeout(r, 100));

            this.refresh()
            Vue.$log.info("P recieved")            
        },     

        created: async function() {
            Vue.$log.info("P initalising")
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