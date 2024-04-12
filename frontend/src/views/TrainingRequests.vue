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
                        ref="idTextField"
                        v-model="filteredId"
                        append-icon="mdi-magnify"
                        label="Search By ID"
                        single-line
                        hide-details
                        @keydown.enter.prevent="filterById"
                        :rules="numberRules"
                    ></v-text-field>
                </v-col> 
                <v-col cols="2">
                    <v-text-field
                        ref="typeTextField"                    
                        v-model="filteredRequestType"
                        append-icon="mdi-magnify"
                        label="Search By Type"
                        single-line
                        hide-details
                        @keydown.enter.prevent="filterByRequestType"
                    ></v-text-field>
                </v-col>              
                <v-col cols="3">
                    <v-text-field
                        ref="fullNameTextField" 
                        v-model="filteredFullName"
                        append-icon="mdi-magnify"
                        label="Search By User"
                        single-line
                        hide-details
                        @keydown.enter.prevent="filterByFullName"
                    ></v-text-field>
                </v-col>     
                <v-col cols="2">
                    <v-btn class="align-clear-btn" color="deep-purple-lighten-4" density="compact" small @click="clearFilters">
                        <v-icon left>mdi-close</v-icon>
                        Clear filters
                    </v-btn>
                </v-col>
            </v-row>                    
        </v-card-title>
        <v-data-table
                :headers="trequestsTableHeaders"
                :items="trequests"
                item-key="id"
                class="elevation-1"
                :items-per-page="tableItemsPerPage"
                :sort-by="['id']"
                :sort-desc="[true]"
                height="auto" width="100%"
                show-expand
                :single-expand="true"
                :expanded.sync="expanded"
                :footer-props="{ itemsPerPageOptions: tableRowOptions }"
                @item-expanded="fetchTrainingRequestDetails($event)"
        >
            <template v-slot:item="{ item, expand, isExpanded }">
                 <tr @click="expand(!isExpanded)">
                    <td></td>
                    <td>
                        <a :href="`${item.url}`" target="_blank">
                            {{ item.id }}
                        </a>
                    </td>
                    <td class="truncate">{{ item.date }}</td>   
                    <td>
                        <a :href="`${item.url}`" target="_blank">
                            {{ item.user.username }}
                        </a>
                    </td>                    
                    <td class="truncate">{{ item.type }}</td>
                    <td class="truncate">{{ item.user.name }}</td>
                    <td>
                        <StatusIndicatorLocal :status="item.state" :pulse="false"/>
                    </td>
                </tr> 
            </template> 
            
            <template v-slot:expanded-item="{ item, headers }">
                <td :colspan="headers.length">
                    <v-card class="style-expanded-table-card" style="font-size:0.8em">
                        <div class="mx-6">
                            <v-row>
                                <v-col cols="4">
                                    <v-card class="mx-2 my-4">     
                                        <v-card-title class="style-expanded-card-title">Request details</v-card-title>                       
                                        <v-card-text class="style-expanded-table-text">
                                            <div>
                                                <strong>ID</strong>:  {{ item.id }}
                                            </div>
                                            <div>
                                                <strong>Date</strong>:  {{ item.date }}
                                            </div>
                                            <div>
                                                <strong>New</strong>:  {{ item.new }}
                                            </div>
                                            <div>
                                                <strong>Type</strong>:  {{ item.type }}
                                            </div>                                            
                                            <div>
                                                <strong>form_name</strong>:  {{ item.form_name }}
                                            </div>
                                            <div>
                                                <strong>username</strong>:  {{ item.username }}
                                            </div>                           
                                        </v-card-text> 
                                    </v-card>
                                    <v-card v-if="item.form_data">    
                                        <v-card-title class="style-expanded-card-title">Form content</v-card-title>                                                                  
                                        <v-card-text class="style-expanded-table-text">                
                                            <div v-for="(value, key) in item.form_data" :key="key">
                                                <div>
                                                    <strong>{{ key }}</strong> : {{ value }}
                                                </div>
                                            </div>
                                        </v-card-text>                            
                                    </v-card>
                                </v-col>
                                <v-col cols="8">
                                    <v-card>    
                                        <v-card-title class="style-expanded-card-title">User</v-card-title>                              
                                        <UserStatusTable :user="item.user"/>                          
                                    </v-card> 
                                    <v-card>    
                                        <v-card-title class="style-expanded-card-title">Projects</v-card-title>                              
                                        <ProjectStatusTable :projects="item.projects"/>                          
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



<script>
    import Vue from 'vue'
    import VueLogger from 'vuejs-logger'
    //import RimsdashAPI from "@/api/RimsdashAPI"
    import TrainingRequestsAPI from "@/api/TrainingRequestsAPI"
    import StatusIndicatorLocal from '../components/StatusIndicatorLocal.vue'    
    import UserStatusTable from '../components/UserStatusTable.vue'   
    import ProjectStatusTable from '../components/ProjectStatusTable.vue'      
    import { tablePerPageSetupMixin } from '../mixins/tablePerPageSetupMixin';  


    Vue.use(VueLogger)

    export default {
        name: 'TrainingRequests',
        mixins: [tablePerPageSetupMixin],        
        components:{
            StatusIndicatorLocal: StatusIndicatorLocal,
            UserStatusTable: UserStatusTable,
            ProjectStatusTable: ProjectStatusTable,
            //TrainingRequestCardExpanded: TrainingRequestCardExpanded,
        },           
        data() {
            return {

                expanded: [],
                //expanded_data: {},
                singleExpand: true,

                loading: false,

                trequests: [],
                trequestsFull: [],
                filteredId: null,
                filteredRequestType: null,
                filteredFullName: null,

                trequestsTableHeaders: [
                    { text: 'Id', value: 'id', width: '10%', sortable: false },
                    { text: 'Requested', value: 'date', width: '20%', sortable: false },
                    { text: 'Username', value: 'username', width: '20%', sortable: false },
                    { text: 'Type', value: 'type', width: '10%', sortable: false },
                    { text: 'Name', value: 'name', width: '30%', sortable: false },
                    { text: 'OK', value: 'ok', width: '10%', sortable: false },
                ],

                numberRules: [
                    value => ( value === null || value && ( value >= 0 || value === '' )) || 'Must be 0 or a positive number'
                ],

            }
        },
        methods: {
            async refresh(){
                Vue.$log.debug("TR refreshing ...")
                this.loading = true
                this.trequestsFull = await this.retrieveAllTrainingRequests()
                //this.trequests = await TrainingRequestAPI.getTrainingRequests()
                this.loading = false       
                this.trequests = this.trequestsFull
                Vue.$log.debug("TR refresh complete...")
            },

            async filterById(){
                this.trequests = []
                if (this.filteredId){
                    this.filteredRequestType = null
                    this.filteredFullName = null
                    this.loading = true
                    this.trequests = await TrainingRequestsAPI.getTrainingRequestsById(this.filteredId)
                    this.loading = false
                } else {
                    this.trequests = this.trequestsFull
                }
            },

            async filterByRequestType(){
                this.trequests = []
                if (this.filteredRequestType){
                    this.filteredId = null                  
                    this.filteredFullName = null
                    this.loading = true
                    this.trequests = await TrainingRequestsAPI.getTrainingRequestsByRequestType(this.filteredRequestType)                    
                    this.loading = false
                } else {
                    this.trequests = this.trequestsFull
                }
            },

            async filterByFullName(){
                this.trequests = []

                if (this.filteredFullName){
                    Vue.$log.debug("filtering by fullname " + this.filteredFullName)                     
                    this.filteredId = null                     
                    this.filteredRequestType = null
                    this.loading = true
                    this.trequests = await TrainingRequestsAPI.getTrainingRequestsByUser(this.filteredFullName) 
                    this.loading = false 
                } else {
                    this.trequests = this.trequestsFull
                }
            },

            async clearFilters(){
                Vue.$log.debug("clearing filters")                     
                this.filteredId = null
                this.filteredRequestType = null
                this.filteredFullName = null
                this.trequests = this.trequestsFull
                this.loading = false
            },


            userFilter(items, search) {
                return items.filter(user_rights => user_rights.some(item => item.user.name.toLowerCase().indexOf(search.toLowerCase())) !== -1)
            },


            async retrieveAllTrainingRequests() {
                console.log("retrieving trequest states");
                let __trequests = [ {} ];

                //retrieve values to populate dropdown
                try {
                    __trequests = await TrainingRequestsAPI.getAllTrainingRequestsWithUsers()
                } catch (error) {
                    Vue.$log.error("API call FAILED")                       
                }             
                Vue.$log.debug("first trequest type:  "  + __trequests[0].type)  
                return __trequests
            },

            async retrieveTrainingRequestDetails(trequest_id) {
                Vue.$log.debug("retrieveTrainingRequestDetails start " + trequest_id);

                let trequest_details = {}

                try {
                    Vue.$log.debug("awaiting details:  "  + trequest_id)
                    //trequest_details = await TrainingRequestsAPI.getAllTrainingRequests()[0]
                    trequest_details = await TrainingRequestsAPI.getTrainingRequestDetails(trequest_id)
                    Vue.$log.debug("retrieved details:  "  + trequest_details.username)
                } catch (error) {
                    Vue.$log.debug("API call getTrainingRequestDetails FAILED")                       
                }             

                return trequest_details
                
            },

            async retrieveProjectsForUser(username) {
                Vue.$log.debug("retrieveProjectsForUser start " + username);

                let user_projects = []

                try {
                    Vue.$log.debug("awaiting project details:  "  + username)
                    //trequest_details = await TrainingRequestsAPI.getAllTrainingRequests()[0]
                    user_projects = await TrainingRequestsAPI.getProjectsForUser(username)
                } catch (error) {
                    Vue.$log.debug("API call retrieveProjectsForUser FAILED")                       
                }             
                Vue.$log.debug("retrieved project details:  "  + user_projects[0].id)
                return user_projects
            },            

            async fetchTrainingRequestDetails(event) {
                const item = event.item; 

                Vue.$log.debug("fetching details for " + item.id);
                let trequest_details = {}
                let projects = []

                this.loading = true
                trequest_details = await this.retrieveTrainingRequestDetails(item.id)
                this.loading = false
                this.loading = true
                projects = await this.retrieveProjectsForUser(item.username)
                this.loading = false

                trequest_details.projects = projects

                const index = this.trequests.indexOf(item);

                //replace the trequest data with the fetched details incl. extra fields
                //WARNING: these objects need to remain compatible
                this.$set(this.trequests, index, trequest_details);
           },

            caseCompare(a, b) {
                return typeof a === 'string' && typeof b === 'string'
                    ? a.localeCompare(b, undefined, { sensitivity: 'accent' }) === 0
                    : a === b;
           },

        },
        mounted: async function() {
            Vue.$log.info("TR waiting")
            this.loading = true
            //sleep 100ms
            await new Promise(r => setTimeout(r, 100));

            this.refresh()
            Vue.$log.debug("TR recieved")            
        },     

        created: async function() {
            Vue.$log.debug("TR initalising")
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

    .align-clear-btn {
        height: auto; /* Adjust the button height as needed */
        margin-top: 18px;
    }

</style>