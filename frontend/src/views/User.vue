<template>
    <v-container grid-list>
            <div>       
            </div>
            <UserLightBoard :user_state=this.user_state :project_states=this.project_states />
    </v-container>
</template>


<script>
    import Vue from 'vue'
    import RimsdashAPI from "@/api/RimsdashAPI"
    import VueLogger from 'vuejs-logger'
    import UserLightBoard from '../components/UserLightBoard.vue'

    Vue.use(VueLogger)


    export default {
        name: 'My_account',
        components:{
            UserLightBoard: UserLightBoard
        },
        data() {
            return {
                user_data: {},
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
            user_data: async function() {
                Vue.$log.info("new selection: " + this.user_data.login);
                this.user_state = await this.retrieveUserState(this.user_data.login)
                this.project_states = await this.retrieveUserProjectStates(this.user_data.login)
                return 0
            },
        },
        methods: {

            async retrieveUserByEmail(email) {
                console.log("retrieving user data for  " + email);
                let _user_data = {};

                //retrieve values to populate dropdown
                try {
                    _user_data = await RimsdashAPI.getUserByEmail(email)
                } catch (error) {
                    Vue.$log.info("API call getUserByEmail FAILED")                       
                    _user_data = {};
                }             
                Vue.$log.info("user data retrieved for:  "  + _user_data.login)               
                return _user_data
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
                Vue.$log.info(user_state)                 
                Vue.$log.info("login returned:  "  + user_state.metadata.login) 
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

        },

        created: async function() {
            //retrieve values to populate dropdown

            Vue.$log.info("U initalising")
            this.user_data = await this.retrieveUserByEmail(this.$keycloak.idTokenParsed.email)

            Vue.$log.info("U initalised")            
        }

    } 

</script>