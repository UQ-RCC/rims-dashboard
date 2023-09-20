<template>
    <v-row>     
        <v-col cols="2">
            <div class="vertical-center">
                <h5 style="text-align:center">{{this.user_result.metadata.name}}</h5>
            </div>
        </v-col>    
        <v-col cols="1"
            v-for="item in this.user_result.indicators"
            :key="item.key"
        >
            <LightCell :cell_label=item.label :cell_value=item.value   />
        </v-col>  
        <v-spacer cols="1"/>        
        <v-spacer cols="1"/> 
        <v-spacer cols="1"/>                             
        <v-spacer cols="1"/>      
    </v-row>         
</template>



<!---
<v-col cols="1"
v-for="item in this.user_result.states"
:key="item.key"
>
-->


<script>
    import LightCell from './LightCell.vue'

    export default {
        name: 'LightSetUser',        
        components:{
            LightCell: LightCell
        },

        props:['user_result'],
      
    }

</script>

<style>
.vertical-center {
  margin: 0;
  position: relative;
  top: 50%;
  -ms-transform: translateY(-50%);
  transform: translateY(-50%);
}
</style>