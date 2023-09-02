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

    export default {
        name: 'Users',
        components:{
        },
        data() {
            return {
                //api query here
                selected: { search: null, ulogin: null, name: null },
                userlist: [ this.selected, ],
            };
        },
        watch: {
            //watcher for update from dropdown
            //TODO link project, board calls here
            selected: function() {
                Vue.$log.info("new selection: " + this.selected.search);
                return 0
            },
        },
        methods: {        
            refreshDropdownValues() {
                console.log("placeholder for dropdown refresh");
            },
               
        },
        created: async function() {
            //retrieve values to populate dropdown
            try {
                Vue.$log.info("before api")
                this.userlist = await RimsdashAPI.getUserList()
            } catch (error) {
                Vue.$log.info("API call getUserList FAILED")                       
                this.userlist = null;
            }
            Vue.$log.info("data retrieved, eg:  "  + this.userlist[0].search)
        }

    } 

</script>