<template>
    <v-card class="style-expanded-table-card" style="font-size:0.8em">
        <div class="mx-6">
            <v-row>
                <v-col cols="6">
                    <v-card class="mx-2 my-4">
                        <v-card-title class="style-expanded-card-title">Project details</v-card-title> 
                        <v-card-text class="style-expanded-table-text" v-if="item.user_rights">
                            <div>
                                <strong>Title</strong>:  {{ item.title }}
                            </div>
                            <div>
                                <strong>Group</strong>:  {{ item.group }}
                            </div>
                            <div>
                                <strong>Type</strong>:  {{ item.type }}
                                <FeeForServiceIcon :value="item.type" :size="'large'"/>
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
                            <div v-if="item.user_rights">
                                {{ item.description }}
                            </div>
                            <div v-else>
                                ...
                            </div>
                        </v-card-text>
                    </v-card>
                </v-col>
                <v-col cols="6">
                    <v-card class="mx-2 my-4" v-if="item.user_rights">
                        <v-card-title class="style-expanded-card-title">Users</v-card-title>                                    
                        <v-data-table    
                        :headers="usersTableHeaders"
                        :items="item.user_rights"
                        item-key="username"
                        class="elevation-1"
                        :items-per-page="10"
                        :sort-by="['user.admin']"
                        :sort-desc="[true]"
                        height="300px" width="50%"
                        hide-default-footer
                        >
                            <template v-slot:item="{ item }">
                                <tr :class="itemRowBackground(item)">
                                    <td class="truncate">{{ item.user.name }}</td>                                      
                                    <td>
                                        <a :href="`${item.user.url}`" target="_blank">
                                        {{ item.user.username }}
                                        </a>
                                    </td>
                                    <td class="col_lh-divider">
                                        <StatusIndicatorLocal :status="item.user.user_state.active" :pulse="false"/>
                                    </td>   
                                    <td>
                                        <StatusIndicatorLocal :status="item.user.user_state.access_aibn" :pulse="false"/>
                                    </td>  
                                    <td>
                                        <StatusIndicatorLocal :status="item.user.user_state.access_hawken" :pulse="false"/>
                                    </td>   
                                    <td>
                                        <StatusIndicatorLocal :status="item.user.user_state.access_chem" :pulse="false"/>
                                    </td>                                                           
                                    <td>
                                        <StatusIndicatorLocal :status="item.user.user_state.access_qbp" :pulse="false"/>
                                    </td>
                                    <td>
                                        <StatusIndicatorLocal :status="item.user.user_state.access_pitschi" :pulse="false"/>
                                    </td>
                                    <td class="col_lh-divider">
                                        <StatusIndicatorLocal :status="item.user.user_state.ok_user" :pulse="false"/>
                                    </td>                                                             
                                </tr>
                            </template>
                        </v-data-table>
                    </v-card>
                    <v-card class="style-expanded-table-card" style="font-size:0.8em" v-else>
                        <v-card-text class="style-expanded-table-text">...</v-card-text>
                    </v-card>
                </v-col>                    
            </v-row>
        </div>
    </v-card>

</template>

<script>
import Vue from 'vue'
import VueLogger from 'vuejs-logger'
import StatusIndicatorLocal from '../components/StatusIndicatorLocal.vue'    
import FeeForServiceIcon from '../components/FeeForServiceIcon.vue'   

Vue.use(VueLogger)

export default {
    name: 'Projects',
    props: {
        item: {
            type: Object,
            required: false
        },
    },
    data() {
        return {
            usersTableHeaders: [
                        { text: 'Name', value: 'user.name', width: '25%', sortable: true },
                        { text: 'Username', value: 'user.username', width: '8%', sortable: true },
                        { text: 'Active', value: 'user_state.active', width: '8%', sortable: false },
                        { text: 'AIBN', value: 'user_state.access_aibn', width: '8%', sortable: false },
                        { text: 'Hawken', value: 'user_state.access_hawken', width: '8%', sortable: false },
                        { text: 'Chem', value: 'user_state.access_chem', width: '8%', sortable: false },
                        { text: 'QBP', value: 'user_state.access_qbp', width: '8%', sortable: false },
                        { text: 'Pitschi', value: 'user_state.access_pitschi', width: '8%', sortable: false },
                        { text: 'User', value: 'user_state.ok_user', width: '8%', sortable: false },
                        { text: '', value: 'user.admin', class: 'd-none', sortable: true }, // hidden column for sort, not working yet, class: 'd-none',
                    ],
        }
    },
    components:{
        StatusIndicatorLocal: StatusIndicatorLocal,
        FeeForServiceIcon: FeeForServiceIcon
    },  
    methods: {
        itemRowBackground: function (item) {
                return ( item.user.admin == "Admin" || item.user.admin == "PreviousAdmin" ) ? 'style-row-admin' : 'style-row-user'
            },
    }
}

</script>

<style scoped>

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

    .style-expanded-card-title {
        line-height: 0.9em;
    }  
    
    .style-expanded-card-text {
        line-height: 0.8em;
    }

    .col_lh-divider {
        border-left: 1.5px solid lightgray;
    }

    .d-none {
        display: none;
    }

</style>