<template>
    <v-container grid-list>
            <div>
                <v-autocomplete 
                    v-model="selected" 
                    :items="userlist"            
                    item-text="search"
                    return-object>
                </v-autocomplete>            
            </div>
            <UserLightBoard :user_state=this.user_state :project_states=this.project_states />
    </v-container>
</template>


<script>
    import Vue from 'vue'
    import "v-autocomplete/dist/v-autocomplete.css"
    import RimsdashAPI from "@/api/RimsdashAPI"
    import VueLogger from 'vuejs-logger'
    import UserLightBoard from '../components/UserLightBoard.vue'

    Vue.use(VueLogger)

    const DEFAULT_USER_STATE = { 
            metadata: {
                name: "Unknown"
            },
            state_labels: {

            },
            state: {
                overall: 'off',
                account: 'off',
                access_aibn: 'off',
                access_hawken: 'off',
                access_chemistry: 'off',
                access_qbp: 'off',
            }
        }
        
    const DEFAULT_PROJECT_STATES = [
        {     
            metadata: {
                ProjectName: 'N/A',
            },     
            state_labels: {

            },       
            state: {
                overall: 'off',
                active: 'off',                
                financial: 'off', 
                OHS: 'off', 
                RDM: 'off', 
                phase: 'off',                 
            },
        }
    ]

    

    export default {
        name: 'Users',
        components:{
            UserLightBoard: UserLightBoard
        },
        data() {
            return {
                //api query here
                selected: { search: null, ulogin: null, name: null },
                userlist: [ this.selected, ],
                user_state: {},
                project_states: [{},],
            };
        },
        watch: {
            //watcher for update from dropdown
            //TODO link project, board calls here
            selected: async function() {
                Vue.$log.info("new selection: " + this.selected.search);
                this.user_state = await this.retrieveUserState(this.selected.ulogin)
                this.project_states = await this.retrieveUserProjectStates(this.selected.ulogin)
                return 0
            },
        },
        methods: {

            async refreshDropdownValues() {
                //retrieve values to populate dropdown
                console.log("refreshing dropdown");
                let userlist = null;

                try {
                    userlist = await RimsdashAPI.getUserList()
                } catch (error) {
                    Vue.$log.info("API call getUserList FAILED")                       
                    userlist = null;
                }
                Vue.$log.info("data retrieved, eg:  "  + userlist[0].search)                
                return userlist
            },

            async retrieveUserState(user_login) {
                console.log("retrieving user state for  " + user_login);
                let user_state = DEFAULT_USER_STATE;

                //retrieve values to populate dropdown
                try {
                    user_state = await RimsdashAPI.getState(user_login)
                } catch (error) {
                    Vue.$log.info("API call getState FAILED")                       
                    user_state = DEFAULT_USER_STATE;
                }             
                Vue.$log.info("user state retrieved:  "  + user_state)  
                return user_state
            },


            async retrieveUserProjectStates(user_login) {
                console.log("retrieving project states for user: " + user_login);
                let project_states = DEFAULT_PROJECT_STATES;

                //retrieve values to populate dropdown
                try {
                    project_states = await RimsdashAPI.getUserProjectStates(user_login)
                } catch (error) {
                    Vue.$log.info("API call getState FAILED")                       
                    project_states = DEFAULT_PROJECT_STATES
                }             
                Vue.$log.info("user state retrieved:  "  + user_login)  
                return project_states
            },            
        },
        created: async function() {
            //retrieve values to populate dropdown
            Vue.$log.info("initalising")
            this.userlist = await this.refreshDropdownValues()

                       
        }

    } 

</script>