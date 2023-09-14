<template>
    <v-row>     
        <v-col cols="2">
            <div class="vertical-center">
                <h5 style="text-align:center">{{user_result.metadata.name}}</h5>
            </div>
        </v-col>    
        <v-col cols="1"
            v-for="([key, value]) in Object.entries(user_result.state)"
            :key = key
        >
            <LightCell :cell_value=value :cell_label=user_result.state_labels.key  />
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