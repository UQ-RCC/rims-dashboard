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
            <UserLightBoard :state=this.state />
    </v-container>
</template>


<script>

    import Vue from 'vue'
    import "v-autocomplete/dist/v-autocomplete.css"
    import RimsdashAPI from "@/api/RimsdashAPI"
    import VueLogger from 'vuejs-logger'
    import UserLightBoard from '../components/UserLightBoard.vue'

    Vue.use(VueLogger)

    const DEFAULT_STATE = { 
        user: {
            overall: 'off',
            account: 'off',
            access: {
                aibn: 'off',
                hawken: 'off',
                chemistry: 'off',
                qbp: 'off',
            },
        },  
        projects: [     
            {
                overall: 'off',
                active: 'off',                
                financial: 'off', 
                OHS: 'off', 
                RDM: 'off', 
                phase: 'off',                 
            },
        ],
    }
    

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
                state: DEFAULT_STATE,
            };
        },
        watch: {
            //watcher for update from dropdown
            //TODO link project, board calls here
            selected: async function() {
                Vue.$log.info("new selection: " + this.selected.search);
                this.state = await this.retrieveState(this.selected.ulogin)
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

            async retrieveState(_user_login) {
                console.log("retrieving board state for  " + _user_login);
                let _state = DEFAULT_STATE;

                //retrieve values to populate dropdown
                try {
                    _state = await RimsdashAPI.getState(_user_login)
                } catch (error) {
                    Vue.$log.info("API call getState FAILED")                       
                    _state = DEFAULT_STATE;
                }             
                Vue.$log.info("user state retrieved:  "  + _state)  
                return _state
            },
        },
        created: async function() {
            //retrieve values to populate dropdown
            Vue.$log.info("initalising")
            this.userlist = await this.refreshDropdownValues()

                       
        }

    } 

</script>