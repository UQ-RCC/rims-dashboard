<template>
    <div>        
        <div>
            <Dropdown
                :options="options"
                v-on:selected="validateSelection"
                v-on:filter="getDropdownValues"
                :disabled="false"
                placeholder="Select a user">
            </Dropdown>
        </div>
    </div>
</template>

<script>
    import Vue from 'vue'
    import Dropdown from 'vue-simple-search-dropdown'
    import RimsdashAPI from "@/api/RimsdashAPI"

    Vue.use(Dropdown);

    export default {
        name: 'Users',
        components:{
            Dropdown: Dropdown
        },
        data() {
            return {
                //api query here
                options: [
                    { name: "John Smith", id: "j.smith" },
                    { name: "Bob Jenkins", id: "b.jenkins" }
                ],
            
                selected: { name: null, id: null }
            };
        },
    
        methods: {        
            validateSelection(selection) {
                this.selected = selection;
                console.log(selection.name + " has been selected");
            },
        
            getDropdownValues(keyword) {
                console.log("You could refresh options by querying the API with " + keyword);
            }
        },
        mounted: async function() {
            console.log("trying api")
            try {
                this.userlist = await RimsdashAPI.getUserList()
            } catch (error) {
                console.log("api failed")                        
                this.userlist = null;
            }
            console.log("post api, userlist[2].label:  "  + this.userlist[2].label)
            console.log("post api, userlist[2]:  "  + JSON.stringify(this.userlist[2]))
        }

    } 
</script>