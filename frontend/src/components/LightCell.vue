<template>
    <div id="lightcell">  
        <v-row><p class="text-overline" style="text-align:right">{{this.cell_label}}</p></v-row>
        <v-row><v-btn
            color="secondary"
            elevation="2"
            icon
        ></v-btn></v-row>
    </div>        
</template>

<script>
    import Vue from 'vue'
    
    export default {
        name: 'LightCell',
        props:['localval', 'cell_label'],

        created: function() {
            Vue.$log.info("LC val  " + this.localval)               
        }       
        
    }

</script>

<style scoped >
.text-indicator-small
{
    font-size: '24px';
    text-align: center;
    color: blue;
}
</style>