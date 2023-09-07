<template>
    <div id="lightcell">  
        <v-row rows="2"><p class="text-overline" style="text-align:right">{{this.cell_label}}</p></v-row>
        <v-row rows="2">
            <StatusIndicatorLocal :status="this.cell_value" pulse="true"/>
        </v-row>
    </div>        
</template>

<script>
    import Vue from 'vue'
    import StatusIndicatorLocal from './StatusIndicatorLocal.vue'    

    export default {
        name: 'LightCell',
        props:['cell_label', 'cell_value'],
        components:{
            StatusIndicatorLocal: StatusIndicatorLocal
        },

        created: function() {
            Vue.$log.info("LC val  " + this.cell_value)               
        }       
        
    }
    //simple map from cell_value to colour
    
</script>

<style scoped >
.text-indicator-small
{
    font-size: '24px';
    text-align: center;
    color: blue;
}
</style>


<!--
<v-btn
color="secondary"
elevation="2"
icon
></v-btn>
-->