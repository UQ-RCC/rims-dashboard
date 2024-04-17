<template>
    <div>
        <v-breadcrumbs
                :items="nav_items" large
                divider=">">
        </v-breadcrumbs>      
        <v-row justify="space-around" style="padding: 20px">
            <v-card width="750px" height="150px">
                <v-card-title class="gray--text mt-2">
                <p >
                    Sync status
                </p>
                </v-card-title>
                <v-card-text>
                    <v-list-item>
                        <v-list-item-icon>
                            <v-icon :style="[is_syncing == true ? {'color': 'green !important'} : {'color' : 'grey'}]">mdi-sync</v-icon>
                        </v-list-item-icon>
                        <v-list-item-title class="ml-n5" v-text="is_syncing == true ?'Sync is currently active' :'Sync is currently idle'"> </v-list-item-title>
                        <v-list-item-action>
                            <v-btn color="primary" name="offbtn" :disabled="!is_syncing" @click="turnOffSync()"> Reset</v-btn>
                        </v-list-item-action>
                    </v-list-item>   
                </v-card-text>
            </v-card>
        </v-row>
    </div>
</template>



<script>
    import Vue from 'vue'
    import VueLogger from 'vuejs-logger'    
    import ControlAPI from "@/api/ControlAPI"
    import VueSimpleAlert from "vue-simple-alert";
    
    Vue.use(VueSimpleAlert);
    Vue.use(VueLogger)
    
    export default {
        components:{
        },
        data: () => ({
            drawer: true,
            is_syncing: false,
            loading: false,
            nav_items: [
                    {
                    text: 'Administration',
                    disabled: false,
                    href: 'admin',
                    }
                ],
        }),
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
            signout: function(){
                // signout
                this.$keycloak.logout({'redirectUri': Vue.prototype.$Config.signoutUrl})
            },
            toggleDrawer(){
                this.drawer = !this.drawer
            },
             
            turnOffSync() { // set the sync option to false
                console.log("Turn off sync")
                this.$fire({
                    title: "Reset RIMS sync status to idle",
                    text: 'Are you sure?',
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

            

        },
         mounted: async function() { // reading initial sync status
            this.last_sync = await ControlAPI.getLastSync()
            this.is_syncing = ( this.last_sync.status != 'in_progress' )
            this.loading = this.is_syncing
        }, 
    }
</script>

<style>
</style>