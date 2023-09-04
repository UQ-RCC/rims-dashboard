<template>
    <div id="lightset-project">  
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
                <LightCell cell_label="Billing"/>
            </v-col>
            <v-col>
                <LightCell cell_label="RA"/>
            </v-col>
            <v-col>
                <LightCell cell_label="RDM"/>
            </v-col>   
            <v-col>
                <LightCell cell_label="Phase"/>                
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
        name: 'LightSetProject',
        props:['localstate'],
        components:{
            LightCell: LightCell
        },

        created: function() {
            Vue.$log.info("LSP init")
            Vue.$log.info("LSP state  " + this.localstate)               
        }       
        
    }

</script>

<style>
</style>