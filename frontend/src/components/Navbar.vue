<template>
    <div>
        <v-app-bar
            :clipped-left="$vuetify.breakpoint.lgAndUp"
            app
            dark
            color="#49075e"
        >
            <v-app-bar-nav-icon @click.stop="toggleDrawer" class="mr-0"></v-app-bar-nav-icon>
            <v-toolbar-title>
                <v-btn text href="https://github.com/UQ-RCC/rims-dashboard">
                    <span class="headline">Dashboard</span>
                </v-btn>
            </v-toolbar-title>
            <div class="flex-grow-1"></div>

            <div v-if="$vuetify.breakpoint.smAndUp">
                <span>{{ this.email }}</span>
                <v-menu
                    left
                    bottom
                >
                    <template v-slot:activator="{ on, attrs }">
                    <v-btn
                        icon
                        v-bind="attrs"
                        v-on="on"
                    >
                        <v-icon>mdi-menu-down</v-icon>
                    </v-btn>
                    </template>

                    <v-list dense>
                        <v-list-item
                            @click="signout()"
                        >
                        <v-list-item-icon>
                            <v-icon>mdi-logout</v-icon>
                        </v-list-item-icon>
                        <v-list-item-title>Logout</v-list-item-title>
                    </v-list-item>
                    </v-list>
                </v-menu>

            </div>
        </v-app-bar>
        
        <v-navigation-drawer v-model="drawer" fixed app :clipped="$vuetify.breakpoint.lgAndUp">
            <v-list>
                <v-list-item to="/">
                    <v-list-item-icon>
                        <v-icon>mdi-home</v-icon>
                    </v-list-item-icon>
                    <v-list-item-title class="ml-n5">Home</v-list-item-title>
                </v-list-item>

                <v-list-item to="/projects" v-if="this.has_admin">
                    <v-list-item-icon>
                        <v-icon>mdi-poll-box</v-icon>
                    </v-list-item-icon>
                    <v-list-item-title class="ml-n5">Projects</v-list-item-title>
                </v-list-item>

                <v-list-item to="/trainingrequests" v-if="this.has_admin">
                    <v-list-item-icon>
                        <v-icon>mdi-school</v-icon>
                    </v-list-item-icon>
                    <v-list-item-title class="ml-n5">Training</v-list-item-title>
                </v-list-item>

                <v-list-item to="/administration" v-if="this.has_superadmin">
                    <v-list-item-icon>
                        <v-icon>mdi-settings</v-icon>
                    </v-list-item-icon>
                    <v-list-item-title class="ml-n5">Admin</v-list-item-title>
                </v-list-item>
                
            </v-list>
            <br />
            <!-- <div align="right" justify="right">
                <v-btn fab medium depressed bottom right title="Report bug" @click="openBugDialog">
                    <v-icon>mdi-bug</v-icon>
                </v-btn>
            </div> -->
        </v-navigation-drawer>
    </div>
</template>

<script>
    import Vue from 'vue'
    import PublicAPI from "@/api/PublicAPI"
    import NavbarAPI from "@/api/NavbarAPI"

    import VueLogger from 'vuejs-logger'

    Vue.use(VueLogger)

    export default {
        components:{
        },
        data: () => ({
            drawer: true,
            user: { admin: "User"},
            adminstatus: false,
            superadminstatus: false,       
        }),

        computed: {
            email: function() {
                //note: this is an if-else using ? :
                return this.$keycloak && this.$keycloak.idTokenParsed ? this.$keycloak.idTokenParsed.email  : ''
            },

            has_admin(){
               if ( ( this.adminstatus.ok == true ) ) {
                    return true
                }
                else {
                    return false
                }
            },

            has_superadmin(){
               if ( ( this.superadminstatus.ok == true ) ) {
                    return true
                }
                else {
                    return false
                }
            },            

        },

        methods: {
            signout: function(){
                // signout
                this.$keycloak.logout({'redirectUri': Vue.prototype.$Config.signoutUrl})
            },
            toggleDrawer(){
                this.drawer = !this.drawer
            },

        },

        mounted: async function() {
        },

        created: async function() {

            const backend_ok = await PublicAPI.checkBackendReady()
            Vue.$log.info("NB backend connection OK: " + backend_ok.ok);      
            const db_ok = await PublicAPI.checkDBConnected()
            Vue.$log.info("NB db connection OK: " + db_ok.ok); 
            const db_populated = await PublicAPI.checkDBPopulated()            
            Vue.$log.info("NB db populated OK: " + db_populated.ok); 



            Vue.$log.info("NB retrieving userdata from keycloak token: " + this.$keycloak.idTokenParsed.email);
            
            try {
                const __user = await NavbarAPI.getUserByToken()
                this.user = __user
                Vue.$log.info("NB got userdata: " + __user.email);
            }
            catch (error) {
                if (error.response && error.response.status === 401) {
                    Vue.$log.error('Authentication error: Invalid token');      
                } else {
                    Vue.$log.error('Authentication error: ' + error.response);
                }
                //this.user = { email: this.$keycloak.idTokenParsed.email, admin: false }
            }

            try {
                this.adminstatus = await NavbarAPI.getAdminByToken()

                Vue.$log.info("NB got admin: " + this.adminstatus.ok);
            }  catch (error) {
                if (error.response && error.response.status === 401) {
                    Vue.$log.error('Authentication error: Invalid token');      
                } else {
                    Vue.$log.error('Authentication error: ' + error.response);
                }
            }            

            try {
                this.superadminstatus = await NavbarAPI.getSuperAdminByToken()

                Vue.$log.info("NB got superadmin: " + this.superadminstatus.ok);
            }  catch (error) {
                if (error.response && error.response.status === 401) {
                    Vue.$log.error('Authentication error: Invalid token');      
                } else {
                    Vue.$log.error('Authentication error: ' + error.response);
                }
            }


 

        },
    }

</script>

<style>
</style>

``
<!---
    async is_rims_admin: function() {
                result = await NavbarAPI.getDefaultUserState()
                return result
            }          
-->