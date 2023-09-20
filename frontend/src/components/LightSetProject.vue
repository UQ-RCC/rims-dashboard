<template>
    <v-row>
        <v-col cols="2">
            <div class="vertical-center">
                <h5 style="text-align:center">{{this.proj_state.metadata.ProjectName | truncate(99)}}</h5>
            </div>
        </v-col>                    
        <v-col cols="1"
            v-for="item in this.proj_state.indicators"
            :key="item.key"
        >
            <LightCell :cell_label=item.label :cell_value=item.value />
        </v-col>        
        <v-spacer cols="1"/> 
        <v-spacer cols="1"/>                             
        <v-spacer cols="1"/>  
        <v-spacer cols="1"/>         
    </v-row>                                              
</template>

<!--
    BUG: vue-truncate above not working, not really required
-->

<script>
    import LightCell from './LightCell.vue'
    
    export default {
        name: 'LightSetProject',
        props:['proj_state'],
        components:{
            LightCell: LightCell
        },
  
        
    }

</script>

<style>
</style>