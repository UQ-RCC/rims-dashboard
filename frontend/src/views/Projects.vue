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
                <v-col cols="4">
                    <v-text-field
                        ref="titleTextField"                    
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
                        ref="groupTextField"                     
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
                :headers="projectsTableHeaders"
                :items="projects"
                item-key="id"
                class="elevation-1"
                height="auto" width="100%"
                :items-per-page="tableItemsPerPage"
                :sort-by.sync="sortBy"
                :sort-desc.sync="sortDesc"
                show-expand
                :single-expand="true"
                :expanded.sync="expanded"
                :footer-props="{ itemsPerPageOptions: tableRowOptions }"
                @click:row="handleRowClick"
                @item-expanded="fetchProjectDetails($event)"
        >
            <template v-slot:item="{ item, expand, isExpanded }">
                 <tr class="style-row-project" @click="handleRowClick(expand, isExpanded)" >
                    <td></td>
                    <td>
                        <a :href="`${item.url}`" target="_blank">
                            {{ item.id }}
                        </a>
                    </td>
                    <td class="truncate">{{ item.title }}</td>   
                    <td class="truncate">{{ item.group }}</td>
                    <td>
                        <FeeForServiceIcon :value="item.type" />
                    </td>
                    <td class="col_both-divider centre-content .sync_pulses">
                        <StatusIndicatorLocal :status="item.project_state.ok_all" :pulse="false" :border="false"/>
                    </td>                      
                    <td >
                        <StatusIndicatorLocal :status="item.project_state.active" :pulse="false"/>
                    </td>   
                    <td >
                        <StatusIndicatorLocal :status="item.project_state.billing" :pulse="false"/>
                    </td>  
                    <td >
                        <StatusIndicatorLocal :status="item.project_state.ohs" :pulse="false"/>
                    </td>   
                    <td >
                        <StatusIndicatorLocal :status="item.project_state.rdm" :pulse="false"/>
                    </td>                                                           
                    <td >
                        <StatusIndicatorLocal :status="item.project_state.phase" :pulse="false" :label="item.phase.toString()"/>
                    </td>
                    <td >
                        <StatusIndicatorLocal :status="item.project_state.ok_project" :pulse="false"/>
                    </td> 
                    <td class="col_both-divider centre-content">
                        <StatusIndicatorLocal :status="item.project_state.ok_user" :pulse="false"/>
                    </td> 
                </tr> 
            </template> 
            
            <template v-slot:expanded-item="{ item, headers }">
                <td :colspan="headers.length">
                    <ProjectCardExpanded :item="item"></ProjectCardExpanded>
                </td>
            </template>

        </v-data-table>
    </v-card>
</template>


<script>
    import Vue from 'vue'
    import VueLogger from 'vuejs-logger'
    //import RimsdashAPI from "@/api/RimsdashAPI"
    import ProjectsAPI from "@/api/ProjectsAPI"
    import StatusIndicatorLocal from '../components/StatusIndicatorLocal.vue'    
    import FeeForServiceIcon from '../components/FeeForServiceIcon.vue'   
    import ProjectCardExpanded from '../components/ProjectCardExpanded.vue'   

    import { tablePerPageSetupMixin } from '../mixins/tablePerPageSetupMixin';

    Vue.use(VueLogger)

    export default {
        name: 'Projects',
        mixins: [tablePerPageSetupMixin],
        components:{
            StatusIndicatorLocal: StatusIndicatorLocal,
            FeeForServiceIcon: FeeForServiceIcon,
            ProjectCardExpanded: ProjectCardExpanded,
        },           
        data() {
            return {


                //initialisation
                loading: false,

                projects: [],
                projectsFull: [],
                filteredId: null,
                filteredTitle: null,
                filteredGroup: null,
                filteredFullName: null,

                //datatable setup
                expanded: [],
                singleExpand: true,

                defaultSortBy: ['id'],
                sortBy: ['id'],

                defaultSortDesc: [true],                
                sortDesc: [true],

                projectsTableHeaders: [
                    { text: 'Id', value: 'id', width: '4%', sortable: true },
                    { text: 'Title', value: 'title', width: '25%', sortable: true },
                    { text: 'Group', value: 'group', width: '10%', sortable: true },
                    { text: 'Type', value: 'type', width: '6%', sortable: true },
                    { text: 'Ready', value: 'project_state.ok_all', width: '6%', sortable: true, align: 'center' },
                    { text: 'Active', value: 'project_state.active', width: '6%', sortable: true, align: 'left' },
                    { text: 'Billing', value: 'project_state.billing', width: '6%', sortable: true, align: 'left' },
                    { text: 'OHS', value: 'project_state.ohs', width: '6%', sortable: true, align: 'left' },
                    { text: 'RDM', value: 'project_state.rdm', width: '6%', sortable: true, align: 'left' },
                    { text: 'Phase', value: 'phase', width: '6%', sortable: true, align: 'left' },
                    { text: 'Project', value: 'project_state.ok_project', width: '6%', sortable: true, align: 'left' },             
                    { text: 'User', value: 'project_state.ok_user', width: '6%', sortable: true, align: 'center' },   
                ],

                numberRules: [
                    value => ( value === null || value && ( value >= 0 || value === '' )) || 'Must be 0 or a positive number'
                ],

            }
        },
        watch: {
            sortBy(newVal) {
                if (newVal.length === 0) {
                    this.sortBy = [ ...this.defaultSortBy ];
                }
            },
            sortDesc(newVal) {
                if (newVal.length === 0) {
                    this.sortDesc = [...this.defaultSortDesc ];
                }            
            },
        },
        methods: {

            handleRowClick(expand, isExpanded) {
                //allows @click.row to be separated from @click expand, preventing table from re-rendering
                expand(!isExpanded);
            },

            async refresh(){
                Vue.$log.debug("P refreshing ...")
                this.loading = true
                this.projectsFull = await this.retrieveAllProjects()
                //this.projects = await ProjectAPI.getProjects()
                this.loading = false       
                this.projects = this.projectsFull
                Vue.$log.debug("P refresh complete...")
                Vue.$log.debug(this.projects[0])
            },

            async filterById(){
                this.projects = []
                if (this.filteredId){
                    this.filteredTitle = null
                    this.filteredGroup = null
                    this.filteredFullName = null
                    this.loading = true
                    this.projects = await ProjectsAPI.getProjectById(this.filteredId)
                    this.loading = false
                    //this.projectsFull.forEach(aproj => {
                    //if(aproj.id === parseInt(this.filteredId))
                    //    this.projects = [aproj]
                    //})
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
                    this.loading = true
                    this.projects = await ProjectsAPI.getProjectsByTitle(this.filteredTitle)                    
                    this.loading = false
                    //this.projectsFull.forEach(aproj => {
                    //if(aproj.title.toLowerCase().includes(this.filteredTitle.toLowerCase()) )
                    //    this.projects.push(aproj)
                    //})
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
                    this.loading = true
                    this.projects = await ProjectsAPI.getProjectsByGroup(this.filteredGroup) 
                    this.loading = false           
                    //this.projectsFull.forEach(aproj => {
                    //    if(aproj.group.toLowerCase().includes(this.filteredGroup.toLowerCase()) )
                    //        this.projects.push(aproj)
                    //})
                } else {
                    this.projects = this.projectsFull
                }
            },

            async filterByFullName(){
                this.projects = []

                if (this.filteredFullName){
                    Vue.$log.debug("filtering by fullname " + this.filteredFullName)                     
                    this.filteredId = null                     
                    this.filteredTitle = null
                    this.filteredGroup = null
                    this.loading = true
                    this.projects = await ProjectsAPI.getProjectsByUser(this.filteredFullName) 
                    this.loading = false 
                    //this.projectsFull.forEach(aproj => {
                    //    if(aproj.user_rights.some(item => item.user.name.toLowerCase().includes(this.filteredFullName.toLowerCase()))                        )
                    //        this.projects.push(aproj)
                    //})
                } else {
                    this.projects = this.projectsFull
                }
            },

            async clearFilters(){
                Vue.$log.debug("clearing filters")                     
                this.filteredId = null
                //reset the id field to avoid triggering validation
                if (this.$refs.idTextField) {
                    this.$refs.idTextField.resetValidation();
                    //  not actually needed, numberRules now accepts null                    
                }                
                this.filteredTitle = null
                this.filteredGroup = null
                this.filteredFullName = null
                this.projects = this.projectsFull
            },


            userFilter(items, search) {
                return items.filter(user_rights => user_rights.some(item => item.user.name.toLowerCase().indexOf(search.toLowerCase())) !== -1)
            },


            async retrieveAllProjects() {
                console.log("retrieving project states");
                let __projects = [ {} ];

                //retrieve values to populate dropdown
                try {
                    __projects = await ProjectsAPI.getAllProjectsWithStates()
                } catch (error) {
                    Vue.$log.error("API call FAILED")                       
                }             
                Vue.$log.debug("first project title:  "  + __projects[0].title)  
                return __projects
            },            

            async retrieveProjectDetails(project_id) {
                Vue.$log.debug("retrieving project details for " + project_id);

                let project_details = {}

                try {
                    project_details = await ProjectsAPI.getProjectDetails(project_id)
                    Vue.$log.debug("retrieved details:  "  + project_details.id)
                } catch (error) {
                    Vue.$log.debug("API call getProjectDetails FAILED")                       
                }             

                return project_details
                
            },

            async fetchProjectDetails(event) {
                const item = event.item; 

                Vue.$log.debug("fetching details for " + item.id);
                Vue.$log.debug("expanded " + this.expanded);
                let project_details = {}

                this.loading = true
                project_details = await this.retrieveProjectDetails(item.id)
                this.loading = false

                const index = this.projects.indexOf(item);
                
                //replace the project data with the fetched details incl. extra fields
                //WARNING: these objects need to remain compatible
                this.$set(this.projects, index, project_details);
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
            Vue.$log.debug("P recieved")            
        },     

        created: async function() {
            Vue.$log.debug("P initalising")
        }        

    }
</script>

<style>
    /*scoped causes last col, first row to be out of scope. must be global for now */

    .truncate200 {
        /* unused */        
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

    .centre-content {
        /* not centering correctly */
        display: flex;
        justify-content: center;    
        align-items: center;
    }    

    .align-clear-btn {
        height: auto; /* Adjust the button height as needed */
        margin-top: 18px;
    }

    .col_lh-divider {
        border-left: 1.5px solid lightgray;
    }

    .col_rh-divider {
        /* unused */        
        border-right: 1px solid lightgray;
    }

    .sync_pulses {
        /* no styles, class exists to tag for watcher */
    }

    .col_both-divider {     
        border-left: 1px solid lightgray;
        border-right: 1px solid lightgray;
    }    
    
    .style-row-project {
        background: rgb(255,255,255) !important;
    }
    .style-row-project:hover {
        background: rgb(250,240,250) !important;
    }  

</style>