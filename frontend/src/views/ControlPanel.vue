<template>
    <v-card height="800px">            
        <v-card-title class="gray--text mt-2">
                <p >
                    Sync status
                </p>
        </v-card-title>        

        <v-row justify="space-around" style="padding: 20px">
            <v-card width="750px">
                <v-data-table
                        :headers="syncTableHeaders"
                        :items="syncEvents"
                        item-key="id"
                        class="elevation-1"
                        :items-per-page="5"
                        :sort-by="['id']"
                        :sort-desc="[true]"
                        height="auto" width="100%"
                        :footer-props="{ itemsPerPageOptions: [ 5, 10, 25] }"
                >
                    <template v-slot:item="{ item }">
                        <tr>
                            <td>{{ item.id }}</td>
                            <td class="truncate">{{ item.start_time }}</td> 
                            <td class="truncate">{{ item.end_time }}</td>                      
                            <td>{{ item.sync_type }}</td>                              
                            <td>{{ item.status }}</td>
                        </tr> 
                    </template> 
                </v-data-table>
            </v-card>
        </v-row>            

        <v-row justify="space-around" style="padding: 20px">
            <v-card width="750px" >
                <v-card-title class="gray--text mt-2">
                    Options
                </v-card-title>
                <v-card-text>
                    <v-list-item>                        
                        <v-list-item-icon>
                            <v-icon :style="[is_syncing == true ? {'color': 'green !important'} : {'color' : 'grey'}]">mdi-sync</v-icon>
                        </v-list-item-icon>
                        <v-list-item-title class="ml-n5">Refresh event list</v-list-item-title>
                        <v-list-item-action>
                            <v-btn color="primary" name="offbtn" @click="refreshTable()">Update</v-btn>
                        </v-list-item-action>                        
                    </v-list-item>                      
                    <v-list-item>
                        <v-list-item-icon>
                            <v-icon :style="[is_syncing == true ? {'color': 'green !important'} : {'color' : 'grey'}]">mdi-sync</v-icon>
                        </v-list-item-icon>
                        <v-list-item-title class="ml-n5" > Start sync: update (~15 min) </v-list-item-title>
                        <v-list-item-action>
                            <v-btn color="primary" name="offbtn" :disabled="is_syncing" @click="confirmManualSync()"> Start </v-btn>
                        </v-list-item-action>
                    </v-list-item> 
                    <v-list-item>
                        <v-list-item-icon>
                            <v-icon :style="[is_syncing == true ? {'color': 'green !important'} : {'color' : 'grey'}]">mdi-sync</v-icon>
                        </v-list-item-icon>
                        <v-list-item-title class="ml-n5" > Start sync: full (~1h) </v-list-item-title>
                        <v-list-item-action>
                            <v-btn color="primary" name="offbtn" :disabled="is_syncing" @click="confirmManualSyncFull()"> Start </v-btn>
                        </v-list-item-action>
                    </v-list-item>                       
                    <v-list-item>
                        <v-list-item-icon>
                            <v-icon :style="[is_syncing == true ? {'color': 'green !important'} : {'color' : 'grey'}]">mdi-sync</v-icon>
                        </v-list-item-icon>
                        <v-list-item-title class="ml-n5" v-text="is_syncing == true ?'A sync event is ongoing' :'Sync is currently idle'"> </v-list-item-title>
                        <v-list-item-action>
                            <v-btn color="primary" name="offbtn" :disabled="!is_syncing" @click="turnOffSync()"> Override</v-btn>
                        </v-list-item-action>
                    </v-list-item>                                             
                </v-card-text>
            </v-card>
        </v-row>
    </v-card>
</template>



<script>
    import Vue from 'vue'
    import VueLogger from 'vuejs-logger'    
    import ControlAPI from "@/api/ControlAPI"
    import VueSimpleAlert from "vue-simple-alert";
    import { tablePerPageSetupMixin } from '../mixins/tablePerPageSetupMixin';  

    Vue.use(VueSimpleAlert);
    Vue.use(VueLogger)

    export default {
        name: 'ControlPanel',
        mixins: [tablePerPageSetupMixin], 
        components:{
        },

        data() {
            return {
                is_syncing: false,
                loading: false,

                syncEvents: [],
                syncEventsFull: [],

                syncTableHeaders: [
                    { text: 'Id', value: 'id', width: '10%', sortable: true },
                    { text: 'Started', value: 'start_time', width: '20%', sortable: false },
                    { text: 'Finished', value: 'end_time', width: '20%', sortable: false },
                    { text: 'Type', value: 'sync_type', width: '20%', sortable: false },
                    { text: 'Status', value: 'status', width: '20%', sortable: false },
                ],                
            }
        },
        computed: {
            email: function() {
                return this.$keycloak && this.$keycloak.idTokenParsed ? this.$keycloak.idTokenParsed.email  : ''
            },
            has_dashboard_access: function() {
                return this.$keycloak.hasRealmRole("dashboard")
            },
            name : function () {
                return this.$keycloak && this.$keycloak.idTokenParsed ? this.$keycloak.idTokenParsed.name  : ''
            }
        },

        methods: {

            async refresh(){
                Vue.$log.debug("CP refreshing ...")
                this.loading = true
                this.syncEventsFull = await this.retrieveAllSyncEvents()
                //this.trequests = await TrainingRequestAPI.getTrainingRequests()
                this.loading = false       
                this.syncEvents = this.syncEventsFull
                this.is_syncing = this.syncEvents.some(item => item.status == 'in_progress')
                Vue.$log.debug("CP refresh complete...")
            },            


            async retrieveAllSyncEvents() {
                Vue.$log.debug("retrieving sync events");
                let __syncEvents = [ {} ];

                //retrieve values to populate dropdown
                try {
                    __syncEvents = await ControlAPI.getAllSyncEvents()
                } catch (error) {
                    Vue.$log.error("API call FAILED")                       
                }             
                Vue.$log.debug("first sync:  "  + JSON.stringify(__syncEvents[0]))  
                return __syncEvents
            },


            signout: function(){
                // signout
                this.$keycloak.logout({'redirectUri': Vue.prototype.$Config.signoutUrl})
            },
        
            turnOffSync() { // set the sync option to false
                console.log("Turn off sync")
                this.$fire({
                    title: "Override RIMS sync status",
                    text: 'This will allow a new manual sync to be triggered even if the DB is already syncing. Are you sure?',
                    showConfirmButton: true,
                    showCancelButton: true,
                    cancelButtonText: 'No',
                    confirmButtonText: 'Yes',
                    
                }).then(r => {
                    if (r.value == true) {
                        //AdminAPI.resetSync()
                        this.is_syncing = false
                        this.loading = false
                    }
                });
                
                
            },

           confirmManualSync() {
                console.log("Manual sync press")
                this.$fire({
                    title: "Manual update",
                    text: 'This will start an update sync to the RIMS DB, which updates the project data but does not check the admin users. During this time, data may cease to display, please wait for at least 30 minutes before attempting further sync events. Are you sure you want to sync at this time?',
                    showConfirmButton: true,
                    showCancelButton: true,
                    cancelButtonText: 'No',
                    confirmButtonText: 'Yes',
                }).then(r => {
                    if (r.value == true) {
                        this.startManualSync()
                    }
                });               
            },            

            startManualSync() {
                Vue.$log.info("initiating manual sync: ")     
                let response = ControlAPI.startManualSyncUpdate()

                if (response.status === 204) {
                    Vue.$log.debug('Sync request successful');
                } else {
                    Vue.$log.error('Sync request unsuccessful');
                }

                this.refresh()
                this.is_syncing = true                
            },

            
            confirmManualSyncFull() {
                console.log("Manual sync press")
                this.$fire({
                    title: "Manual full sync",
                    text: 'This will start a full sync to the RIMS DB, which updates all data including admin users. During this time, data may cease to display, please wait at least 2 hours before attempting further sync events. Are you sure you want to perform a full sync now?',
                    showConfirmButton: true,
                    showCancelButton: true,
                    cancelButtonText: 'No',
                    confirmButtonText: 'Yes',
                }).then(r => {
                    if (r.value == true) {
                        this.startManualSync()
                    }
                });               
            },            

            startManualSyncFull() {
                Vue.$log.info("initiating manual full sync: ")     
                let response = ControlAPI.startManualSyncFull()

                if (response.status === 204) {
                    Vue.$log.debug('Sync request successful');
                } else {
                    Vue.$log.error('Sync request unsuccessful');
                }

                this.refresh()
                this.is_syncing = true
            },            

            refreshTable() {
                Vue.$log.info("manual refresh")     
                this.refresh()
            },

        },
        mounted: async function() { // reading initial sync status
            //this.last_sync = await ControlAPI.getLastSync()
            //this.is_syncing = ( this.last_sync.status != 'in_progress' )
            this.refresh()
        }, 
    }
</script>

<style>
</style>