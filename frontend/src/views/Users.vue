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
    </div>
</template>


<script>

    import Vue from 'vue'
    import "v-autocomplete/dist/v-autocomplete.css"
    import RimsdashAPI from "@/api/RimsdashAPI"
    import VueLogger from 'vuejs-logger'
    Vue.use(VueLogger)

    const DEFAULT_STATE = [ 0,0,  0,0,0,0,  0,0,0,0,0,0,0,0,]

    export default {
        name: 'Users',
        components:{
        },
        data() {
            return {
                //api query here
                selected: { search: null, ulogin: null, name: null },
                userlist: [ this.selected, ],
                state: DEFAULT_STATE,
                user_login: null,
            };
        },
        watch: {
            //watcher for update from dropdown
            //TODO link project, board calls here
            selected: async function() {
                Vue.$log.info("new selection: " + this.selected.search);
                await this.retrieveState()
                return 0
            },
        },
        methods: {

            async refreshDropdownValues() {
                console.log("refreshing dropdown");
                //retrieve values to populate dropdown
                try {
                    this.userlist = await RimsdashAPI.getUserList()
                } catch (error) {
                    Vue.$log.info("API call getUserList FAILED")                       
                    this.userlist = null;
                }
                Vue.$log.info("data retrieved, eg:  "  + this.userlist[0].search)                
            },

            async retrieveState() {
                this.user_login = this.selected.ulogin
                console.log("retrieving board state for  " + this.user_login);

                //retrieve values to populate dropdown
                try {
                    this.state = await RimsdashAPI.getState(this.user_login)
                } catch (error) {
                    Vue.$log.info("API call getState FAILED")                       
                    this.state = DEFAULT_STATE;
                }
                Vue.$log.info("state retrieved:  "  + this.state)               
            },
        },
        created: async function() {
            //retrieve values to populate dropdown
            Vue.$log.info("initalising")
            await this.refreshDropdownValues()
        }

    } 

</script>