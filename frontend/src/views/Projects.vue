<template>
    <v-card>        
        <v-progress-linear
            color="primary accent-4"
            indeterminate
            rounded
            height="4"
            :active="loading"
        ></v-progress-linear>
        <v-card-title>
            <v-row>
                <v-col cols="2">
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
                <v-col cols="4">
                    <v-text-field
                        v-model="filteredTitle"
                        append-icon="mdi-magnify"
                        label="Search By Title"
                        single-line
                        hide-details
                        @keydown.enter.prevent="filterByTitle"
                    ></v-text-field>
                </v-col>              
                <v-col cols="2">
                    <v-text-field
                        v-model="filteredGroup"
                        append-icon="mdi-magnify"
                        label="Search By Group"
                        single-line
                        hide-details
                        @keydown.enter.prevent="filterByGroup"
                    ></v-text-field>
                </v-col>
                <v-col cols="2">
                    <v-text-field
                        v-model="filteredFullName"
                        append-icon="mdi-magnify"
                        label="Search By User"
                        single-line
                        hide-details
                        @keydown.enter.prevent="filterByFullName"
                    ></v-text-field>
                </v-col>                            
            </v-row>                    
        </v-card-title>
        <v-data-table
                :headers="projectsTableHeaders"
                :items="projects"
                item-key="id"
                class="elevation-1"
                :items-per-page="15"
                :sort-by="['id']"
                :sort-desc="[true]"
                height="auto" width="100%"
                show-expand
                :expanded.sync="expanded"
                :footer-props="{ itemsPerPageOptions: [15, 30, 50, 100, -1] }"
        >
            <template v-slot:item="{ item, expand, isExpanded }">
                 <tr @click="expand(!isExpanded)">
                    <td></td>
                    <td>{{ item.id }}</td>
                    <td class="truncate">{{ item.title }}</td>   
                    <td class="truncate">{{ item.group }}</td>
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
                    <td>
                        <StatusIndicatorLocal :status="item.project_state[0].ok" :pulse="false"/>
                    </td>                    
                </tr> 
            </template> 
            
            <template v-slot:expanded-item="{ item, headers }">
                <td :colspan="headers.length">
                    <v-card class="style-expanded-table-card" style="font-size:0.8em">
                        <div class="mx-6">
                            <v-row>
                                <v-col cols="6">
                                    <v-card class="mx-2 my-4">
                                        <v-card-title class="style-expanded-card-title">Project details</v-card-title> 
                                        <v-card-text class="style-expanded-table-text">
                                            <div>
                                                <strong>Title</strong>:  {{ item.title }}
                                            </div>
                                            <div>
                                                <strong>Group</strong>:  {{ item.group }}
                                            </div>
                                            <div>
                                                <strong>Type</strong>:  {{ item.type }}
                                            </div>
                                            <div>
                                                <strong>Active</strong>:  {{ item.active }}
                                            </div>                                            
                                            <div>
                                                <strong>Bcode</strong>:  {{ item.project_account[0].bcode }}
                                            </div>
                                            <div>
                                                <strong>Affiliation</strong>:  {{ item.affiliation }}
                                            </div>
                                            <div>
                                                <strong>RDM</strong>:  {{ item.qcollection }}
                                            </div>
                                            <div>
                                                <strong>Phase</strong>:  {{ item.phase }}
                                            </div>
                                            <div>
                                                <strong>Status</strong>:  {{ item.status }}
                                            </div>
                                        </v-card-text>
                                    </v-card>
                                    <v-card class="mx-2 my-4">
                                        <v-card-title class="style-expanded-card-title">Description</v-card-title>
                                        <v-card-text>
                                            <div>
                                                {{ item.description }}
                                            </div>
                                        </v-card-text>
                                    </v-card>
                                </v-col>
                                <v-col cols="6">
                                    <v-card class="mx-2 my-4">
                                        <v-card-title class="style-expanded-card-title">Users</v-card-title>                                    
                                        <v-data-table    
                                        :headers="usersTableHeaders"
                                        :items="item.user_rights"
                                        item-key="userright.username"
                                        class="elevation-1"
                                        :items-per-page="10"
                                        :sort-by="['userright.admin','userright.username']"
                                        height="300px" width="50%"
                                        hide-default-footer
                                        >
                                            <template v-slot:item="{ item }">
                                                <tr :class="itemRowBackground(item)">
                                                    <td>{{ item.user.name }}</td>
                                                    <td>{{ item.user.username }}</td>
                                                    <td>
                                                        <StatusIndicatorLocal :status="item.user.user_state[0].active" :pulse="false"/>
                                                    </td>   
                                                    <td>
                                                        <StatusIndicatorLocal :status="item.user.user_state[0].access_aibn" :pulse="false"/>
                                                    </td>  
                                                    <td>
                                                        <StatusIndicatorLocal :status="item.user.user_state[0].access_hawken" :pulse="false"/>
                                                    </td>   
                                                    <td>
                                                        <StatusIndicatorLocal :status="item.user.user_state[0].access_chem" :pulse="false"/>
                                                    </td>                                                           
                                                    <td>
                                                        <StatusIndicatorLocal :status="item.user.user_state[0].access_qbp" :pulse="false"/>
                                                    </td>
                                                    <td>
                                                        <StatusIndicatorLocal :status="item.user.user_state[0].ok" :pulse="false"/>
                                                    </td>                                                    
                                                </tr>
                                            </template>
                                        </v-data-table>
                                    </v-card>
                                </v-col>                    
                            </v-row>
                        </div>
                    </v-card>
                </td>
            </template>


        </v-data-table>
    </v-card>
</template>




<!--
    <template v-slot:body="{ items }">
        <tr>v-for="item in items" :key="item.id"

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

                expanded: [],
                expanded_data: {},
                singleExpand: true,

                loading: false,

                projects: [],
                projectsFull: [],
                filteredId: null,
                filteredTitle: null,
                filteredGroup: null,
                filteredFullName: null,

                projectsTableHeaders: [
                    { text: 'Id', value: 'id', width: '5%', sortable: false },
                    { text: 'Title', value: 'title', width: '30%', sortable: false },
                    { text: 'Group', value: 'group', width: '10%', sortable: false },
                    { text: 'Active', value: 'active', width: '7%', sortable: false },
                    { text: 'Billing', value: 'billing', width: '7%', sortable: false },
                    { text: 'OHS', value: 'ohs', width: '7%', sortable: false },
                    { text: 'RDM', value: 'rdm', width: '7%', sortable: false },
                    { text: 'Phase', value: 'phase', width: '7%', sortable: false },
                    { text: 'OK', value: 'ok', width: '7%', sortable: false },                    
                ],

                usersTableHeaders: [
                    { text: 'Name', value: 'name', width: '25%' },
                    { text: 'Username', value: 'username', width: '8%' },
                    { text: 'Active', value: 'active', width: '8%', sortable: false },
                    { text: 'AIBN', value: 'aibn', width: '8%', sortable: false },
                    { text: 'Hawken', value: 'hawken', width: '8%', sortable: false },
                    { text: 'Chem', value: 'chem', width: '8%', sortable: false },
                    { text: 'QBP', value: 'qbp', width: '8%', sortable: false },
                    { text: 'OK', value: 'ok', width: '8%', sortable: false },                    
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
                Vue.$log.info(this.projects[0])
            },

            async filterById(){
                this.projects = []
                if (this.filteredId){
                    this.filteredTitle = null
                    this.filteredGroup = null
                    this.filteredFullName = null                                 
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
                    this.filteredFullName = null                    
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
                    this.filteredFullName = null                    
                    this.projectsFull.forEach(aproj => {
                        if(aproj.group.toLowerCase().includes(this.filteredGroup.toLowerCase()) )
                            this.projects.push(aproj)
                    })
                } else {
                    this.projects = this.projectsFull
                }
            },

            async filterByFullName(){
                this.projects = []

                if (this.filteredFullName){
                    Vue.$log.info("filtering by fullname " + this.filteredFullName)                     
                    this.filteredId = null
                    this.filteredTitle = null
                    this.filteredGroup = null
                    this.projectsFull.forEach(aproj => {
                        if(aproj.user_rights.some(item => item.user.name.toLowerCase().includes(this.filteredFullName.toLowerCase()))                        )
                            this.projects.push(aproj)
                    })
                } else {
                    this.projects = this.projectsFull
                }
            },

            userFilter(items, search) {
                return items.filter(user_rights => user_rights.some(item => item.user.name.toLowerCase().indexOf(search.toLowerCase())) !== -1)
            },


            async retrieveAllProjects() {
                console.log("retrieving project states");
                let __projects = [ {} ];

                //retrieve values to populate dropdown
                try {
                    __projects = await RimsdashAPI.getAllProjectsWithFullStates()
                } catch (error) {
                    Vue.$log.info("API call FAILED")                       
                }             
                Vue.$log.info("first project title:  "  + __projects[0].title)  
                return __projects
            },            

            async retrieveProjectDetails(project_id) {
                console.log("retrieving project details for " + project_id);

                let project_details = {}

                try {
                    project_details = await RimsdashAPI.getProjectDetails(project_id)
                } catch (error) {
                    Vue.$log.info("API call getProjectDetails FAILED")                       
                }             
                
                this.expanded_data = project_details

                Vue.$log.info("retrieved details:  "  + this.expanded_data.status)                  
            },

            caseCompare(a, b) {
                return typeof a === 'string' && typeof b === 'string'
                    ? a.localeCompare(b, undefined, { sensitivity: 'accent' }) === 0
                    : a === b;
           },

            itemRowBackground: function (item) {
                return item.user.admin == false ? 'style-row-user' : 'style-row-admin'
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


    .style-row-user {
        background: rgb(255,255,255) !important;
    }
    .style-row-user:hover {
        background: rgb(250,240,250) !important;
    }    

    .style-row-admin {
        background: rgb(230,230,230) !important;        
    }
    .style-row-admin:hover {
        background: rgb(225,220,225) !important;        

    }    

    .style-expanded-table-card {
        background: rgb(238,238,238) !important;        

    } 

    .style-expanded-card-text {
        line-height: 0.8em;
    }

    .style-expanded-card-title {
        line-height: 0.9em;
    }    

</style>