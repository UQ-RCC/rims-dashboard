<template>
    <div id="lightset-master">  
        {{ localstate }}
        <v-row>
            <v-col>
            </v-col>            
            <v-col>
                <LightCell cell_label="User"/>
            </v-col>
            <v-col>
                <LightCell cell_label="Project"/>
            </v-col>
            <v-col>
            </v-col>
            <v-col>
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
        name: 'LightSetMaster',        
        props:['localstate'],
        components:{
            LightCell: LightCell
        },
        
        created: function() {
            Vue.$log.info("LSM init")
            Vue.$log.info("LSM state  " + this.localstate)               
        }           
    
    }

</script>

<style>
</style>