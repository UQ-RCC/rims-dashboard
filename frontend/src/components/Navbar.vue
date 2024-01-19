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

                <v-list-item to="/projects" v-if="this.has_access">
                    <v-list-item-icon>
                        <v-icon>mdi-poll-box</v-icon>
                    </v-list-item-icon>
                    <v-list-item-title class="ml-n5">Projects</v-list-item-title>
                </v-list-item>

                <v-list-item to="/trainingrequests" v-if="this.has_access">
                    <v-list-item-icon>
                        <v-icon>mdi-school</v-icon>
                    </v-list-item-icon>
                    <v-list-item-title class="ml-n5">Training</v-list-item-title>
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
    import RimsdashAPI from "@/api/RimsdashAPI"
    import VueLogger from 'vuejs-logger'

    Vue.use(VueLogger)

    export default {
        components:{
        },
        data: () => ({
            drawer: true,
            has_rims_admin: false,
        }),

        computed: {
            email: function() {
                //note: this is an if-else using ? :
                return this.$keycloak && this.$keycloak.idTokenParsed ? this.$keycloak.idTokenParsed.email  : ''
            },
            has_dashboard_access: function() {
                return this.$keycloak.hasRealmRole("dashboard")
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

            has_access(){
                if ( ( this.has_rims_admin ) || this.has_dashboard_access ) {
                    return true
                }
                else {
                    return false
                }
            }
        },

        mounted: async function() {
        },

        created: async function() {

            const backend_ok = await RimsdashAPI.checkBackend()
            Vue.$log.info("NB backend connection OK: " + backend_ok.ok);      

            Vue.$log.info("NB retrieving userdata: " + this.$keycloak.idTokenParsed.email);
            const user_response = await RimsdashAPI.getUserByEmail(this.$keycloak.idTokenParsed.email)
            this.user_data = user_response
            Vue.$log.info("NB got userdata: " + user_response.email);

            Vue.$log.info("NB retrieving admin: " + this.$keycloak.idTokenParsed.email);            
            const admin_response = await RimsdashAPI.checkEmailIsAdmin(this.$keycloak.idTokenParsed.email)
            this.has_rims_admin = admin_response.admin
            Vue.$log.info("NB has admin: " + this.has_rims_admin)
            
        },
        

    }

</script>

<style>
</style>


<!---
    async is_rims_admin: function() {
                result = await RimsdashAPI.getDefaultUserState()
                return result
            }          
-->