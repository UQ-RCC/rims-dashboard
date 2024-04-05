<template>
    <v-card class="style-expanded-table-card" style="font-size:0.8em">
        <v-data-table    
            :headers="usersTableHeaders"
            :items="[user]"
            item-key="username"
            class="elevation-1"
            :items-per-page="10"
            :sort-by="['username']"
            height="auto" width="50%"
            hide-default-footer
            >
                <template v-slot:item="{ item }">
                    <tr :class="itemRowBackground(item)">
                        <td>
                            <a :href="`${item.url}`" target="_blank">
                            {{ item.username }}
                            </a>
                        </td>
                        <td>{{ item.name }}</td>                           
                        <td>
                            <StatusIndicatorLocal :status="item.user_state.active" :pulse="false"/>
                        </td>   
                        <td>
                            <StatusIndicatorLocal :status="item.user_state.access_aibn" :pulse="false"/>
                        </td>  
                        <td>
                            <StatusIndicatorLocal :status="item.user_state.access_hawken" :pulse="false"/>
                        </td>   
                        <td>
                            <StatusIndicatorLocal :status="item.user_state.access_chem" :pulse="false"/>
                        </td>                                                           
                        <td>
                            <StatusIndicatorLocal :status="item.user_state.access_qbp" :pulse="false"/>
                        </td>
                        <td>
                            <StatusIndicatorLocal :status="item.user_state.access_pitschi" :pulse="false"/>
                        </td>
                        <td>
                            <StatusIndicatorLocal :status="item.user_state.ok_project" :pulse="false"/>
                        </td>                                                                                                         
                        <td>
                            <StatusIndicatorLocal :status="item.user_state.all_ok" :pulse="false"/>
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

Vue.use(VueLogger)

export default {
    name: 'UserStatusTable',
    props: {
        user: {
            type: Object,
            required: false
        },
    },
    data() {
        return {
            usersTableHeaders: [
                        { text: 'Username', value: 'username', width: '8%', sortable: false },
                        { text: 'Name', value: 'name', width: '25%', sortable: false },
                        { text: 'Active', value: 'active', width: '8%', sortable: false },
                        { text: 'AIBN', value: 'aibn', width: '8%', sortable: false },
                        { text: 'Hawken', value: 'hawken', width: '8%', sortable: false },
                        { text: 'Chem', value: 'chem', width: '8%', sortable: false },
                        { text: 'QBP', value: 'qbp', width: '8%', sortable: false },
                        { text: 'Pitschi', value: 'pitschi', width: '8%', sortable: false },                    
                        { text: 'Project', value: 'project', width: '8%', sortable: false },                     
                        { text: 'OK', value: 'ok', width: '8%', sortable: false },                    
                    ],
        }
    },
    components:{
        StatusIndicatorLocal: StatusIndicatorLocal,
    },  
    methods: {
        itemRowBackground: function (item) {
                return item.admin == false ? 'style-row-user' : 'style-row-admin'
            },
    }
}

</script>

<style>
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

</style>