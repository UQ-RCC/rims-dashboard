<template>
    <div>        
        <div>
            <v-autocomplete 
                v-model="selected" 
                :items="userlist"            
                item-text="search"
                return-object>
            </v-autocomplete>            
        </div>    
        <div>        
            <UserLightBoard :state=this.state />
        </div>  
    </div>
</template>


<script>

    import Vue from 'vue'
    import "v-autocomplete/dist/v-autocomplete.css"
    import RimsdashAPI from "@/api/RimsdashAPI"
    import VueLogger from 'vuejs-logger'
    import UserLightBoard from '../components/UserLightBoard.vue'

    Vue.use(VueLogger)

    //const DEFAULT_STATE = { 
    //    core: [0,0,],  
    //    user: [0,0,0,0,],  
    //    projects: [[0,0,0,0,0,0,0,0,],],
    //}

    const DEFAULT_STATE = { 
        core: [1,1,],  
        user: [2,2,2,2,],  
        projects: [[3,4,1,0,0,0,0,0,],],
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
                let _userlist = null;

                try {
                    _userlist = await RimsdashAPI.getUserList()
                } catch (error) {
                    Vue.$log.info("API call getUserList FAILED")                       
                    _userlist = null;
                }
                Vue.$log.info("data retrieved, eg:  "  + _userlist[0].search)                
                return _userlist
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
                Vue.$log.info("state retrieved, core values:  "  + _state.core)  
                return _state
            },
        },
        created: async function() {
            //retrieve values to populate dropdown
            Vue.$log.info("initalising")
            Vue.$log.info("U default state  " + DEFAULT_STATE.core + "/" + DEFAULT_STATE.user + "/" + DEFAULT_STATE.projects)
            Vue.$log.info("U this.state  " + this.state.core + "/" + this.state.user + "/" + this.state.projects)

            this.userlist = await this.refreshDropdownValues()

                       
        }

    } 

</script>