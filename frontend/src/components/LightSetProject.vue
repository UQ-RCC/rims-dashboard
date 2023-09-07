<template>
    <div id="lightset-project">  
        <v-row rows="2"> 
            <v-col cols="1"><h4 style="text-align:left">Project</h4></v-col>  
            <v-spacer cols="1"/>                    
            <v-col cols="1"
                v-for="item in this.proj_state"
                :key="item.key"
            >
                <LightCell :cell_label=item.label :cell_value=item.state />
            </v-col>        
            <v-spacer cols="1"/> 
            <v-spacer cols="1"/>                             
            <v-spacer cols="1"/>                                   
        </v-row>        
    </div>        
</template>

<script>
    import Vue from 'vue'
    import LightCell from './LightCell.vue'
    
    export default {
        name: 'LightSetProject',
        props:['proj_state'],
        components:{
            LightCell: LightCell
        },

        created: function() {
            Vue.$log.info("LSP init")
            Vue.$log.info("LSP state  " + this.proj_state)               
        }       
        
    }

</script>

<style>
</style>