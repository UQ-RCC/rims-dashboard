<template>
    <div id="lightset-user">  
        <v-row>
            <v-col>
            </v-col>              
            <v-col>
                <LightCell cell_label="Ready"/>
            </v-col> 
            <v-col>
                <LightCell cell_label="Active"/>
            </v-col>                        
            <v-col>
                <LightCell cell_label="AIBN"/>
            </v-col>
            <v-col>
                <LightCell cell_label="Hawken"/>
            </v-col>
            <v-col>
                <LightCell cell_label="Chemistry"/>
            </v-col>
            <v-col>
                <LightCell cell_label="QBP"/>
            </v-col>   
            <v-col>
            </v-col>   
            <v-col>
            </v-col>   
            <v-col>            
            </v-col>                                                                               
            <v-col>
            </v-col>               
        </v-row>
    </div>        
</template>

<script>
    import Vue from 'vue'
    import LightCell from './LightCell.vue'

    export default {
        name: 'LightSetUser',        
        components:{
            LightCell: LightCell
        },

        props:['localstate'],

        created: function() {
            Vue.$log.info("LSU init")
            Vue.$log.info("LSU state  " + this.localstate)               
        }           
    }

</script>

<style>
</style>