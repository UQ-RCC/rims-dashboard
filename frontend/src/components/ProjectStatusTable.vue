<template>
    <v-card class="style-expanded-table-card" style="font-size:0.8em">
        <v-data-table    
            :headers="projectsTableHeaders"
            :items="projects"
            item-key="id"
            class="elevation-1"
            :items-per-page="10"
            :sort-by="['id']"
            :sort-desc="[true]"
            height="auto" width="50%"
            hide-default-footer
            >
                <template v-slot:item="{ item }">
                    <tr>
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
                        <td>
                            <StatusIndicatorLocal :status="item.project_state.ok_all" :pulse="false"/>
                        </td>                      
                        <td class="col_lh-divider">
                            <StatusIndicatorLocal :status="item.project_state.active" :pulse="false"/>
                        </td>   
                        <td>
                            <StatusIndicatorLocal :status="item.project_state.billing" :pulse="false"/>
                        </td>  
                        <td>
                            <StatusIndicatorLocal :status="item.project_state.ohs" :pulse="false"/>
                        </td>   
                        <td>
                            <StatusIndicatorLocal :status="item.project_state.rdm" :pulse="false"/>
                        </td>                                                           
                        <td>
                            <StatusIndicatorLocal :status="item.project_state.phase" :pulse="false"/>
                        </td>
                        <td>
                            <StatusIndicatorLocal :status="item.project_state.ok_project" :pulse="false"/>
                        </td>                              
                    </tr>
                </template>
        </v-data-table>
    </v-card>
</template>

<script>
import Vue from 'vue'
import VueLogger from 'vuejs-logger'
import StatusIndicatorLocal from '../components/StatusIndicatorLocal.vue'    
import FeeForServiceIcon from '../components/FeeForServiceIcon.vue' 

Vue.use(VueLogger)

export default {
    name: 'ProjectStatusTable',
    props: {
        projects: {
            type: Array,
            required: false
        },
    },
    data() {
        return {
            projectsTableHeaders: [
                    { text: 'Id', value: 'id', width: '5%', sortable: false },
                    { text: 'Title', value: 'title', width: '30%', sortable: false },
                    { text: 'Group', value: 'group', width: '10%', sortable: false },
                    { text: 'Type', value: 'type', width: '7%', sortable: false },
                    { text: 'Ready', value: 'active', width: '7%', sortable: false },
                    { text: 'Active', value: 'active', width: '7%', sortable: false },
                    { text: 'Billing', value: 'billing', width: '7%', sortable: false },
                    { text: 'OHS', value: 'ohs', width: '7%', sortable: false },
                    { text: 'RDM', value: 'rdm', width: '7%', sortable: false },
                    { text: 'Phase', value: 'phase', width: '7%', sortable: false },
                    { text: 'Project', value: 'user', width: '7%', sortable: false },            
                ],
        }
    },
    components:{
        StatusIndicatorLocal: StatusIndicatorLocal,
        FeeForServiceIcon : FeeForServiceIcon,
    },  
}

</script>

<style scoped>
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

    .style-expanded-card-title {
        line-height: 0.9em;
    }  
    
    .style-expanded-card-text {
        line-height: 0.8em;
    }

    .col_lh-divider {
        border-left: 1.5px solid lightgray;
    }    

</style>