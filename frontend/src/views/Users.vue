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


    export default {
        name: 'Users',
        components:{
            UserLightBoard: UserLightBoard
        },
        data() {
            return {
                //api query here
                selected: { search: null, login: null, name: null },
                userlist: [ this.selected, ],
                //empty default user                
                user_state: { 
                    metadata: { login: '', name: ''}, 
                    indicators: [{key: '', label: '', value: ''}]
                },
                //empty default project                
                project_states: [{ 
                    metadata: { ProjectName: '', CoreFacilityRef: 0}, 
                    indicators: [{key: '', label: '', value: ''}]
                },],
            };
        },
        watch: {
            //watcher for update from dropdown
            //TODO link project, board calls here
            selected: async function() {
                Vue.$log.info("new selection: " + this.selected.search);
                this.user_state = await this.retrieveUserState(this.selected.login)
                this.project_states = await this.retrieveUserProjectStates(this.selected.login)
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
                let user_state = {};

                //retrieve values to populate dropdown
                try {
                    user_state = await RimsdashAPI.getUserState(user_login)
                } catch (error) {
                    Vue.$log.info("API call getState FAILED")                       
                    user_state = this.default_user_state;
                }             
                Vue.$log.info("user state retrieved for:  "  + user_login) 
                Vue.$log.info("retrieved user name:  "  + user_state.metadata.name)  
                return user_state
            },


            async retrieveUserProjectStates(user_login) {
                console.log("retrieving project states for  " + user_login);
                let project_states = [ {} ];

                //retrieve values to populate dropdown
                try {
                    project_states = await RimsdashAPI.getUserProjectStates(user_login)
                } catch (error) {
                    Vue.$log.info("API call getState FAILED")                       
                    project_states = this.default_project_states;
                }             
                Vue.$log.info("project states retrieved for:  "  + user_login) 
                Vue.$log.info("first project name:  "  + project_states[0].metadata.ProjectName)  
                return project_states
            },


            async retrieveDefaultUserState() {
                let user_state = { };

                //retrieve values to populate dropdown
                try {
                    user_state = await RimsdashAPI.getDefaultUserState()
                } catch (error) {
                    Vue.$log.info("API call getState FAILED")                       
                }             
                Vue.$log.info("default user state retrieved:  " ) 
                Vue.$log.info("retrieved user name:  "  + user_state.metadata.name)  
                return user_state
            },  

            async retrieveDefaultUserProjectStates() {
                let project_states = [];

                //retrieve values to populate dropdown
                try {
                    project_states = await RimsdashAPI.getDefaultProjectStates()
                } catch (error) {
                    Vue.$log.info("API call getState FAILED")                       
                }             
                Vue.$log.info("default project state retrieved")
                Vue.$log.info("retrieved project name:  "  + project_states[0].metadata.ProjectName)
                return project_states
            },

        },
        created: async function() {
            //retrieve values to populate dropdown
            Vue.$log.info("U1 initalising")
            this.userlist = await this.refreshDropdownValues()
            this.default_user_state = await this.retrieveDefaultUserState()
            this.default_project_states = await this.retrieveDefaultUserProjectStates()
            Vue.$log.info("U1 initalised")              
        }

    } 

</script>