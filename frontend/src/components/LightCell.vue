<template>
    <div id="lightcell">  
        <p class="text-caption" style="text-align:center">{{this.cell_label}}</p>
        <div id="indicator_div">
            <StatusIndicatorLocal :status="this.cell_value" :pulse="true"/>
        </div>
    </div>        
</template>



<script>
    import StatusIndicatorLocal from './StatusIndicatorLocal.vue'    

    export default {
        name: 'LightCell',
        props:['cell_label', 'cell_value'],
        components:{
            StatusIndicatorLocal: StatusIndicatorLocal
        },   
        
    }
    //simple map from cell_value to colour
    
</script>

<style scoped >

#lightcell
{
    text-align: center
}

#indicator_div
{
    text-align: center;
    padding-bottom: 25%;    /*% of width*/
}

</style>


<!--
<v-row rows="2"><p class="text-overline" style="text-align:right">{{this.cell_label}}</p></v-row>
<v-row rows="2">
   <StatusIndicatorLocal :status="this.cell_value" pulse="true"/>
</v-row>




<v-btn
color="secondary"
elevation="2"
icon
></v-btn>
-->