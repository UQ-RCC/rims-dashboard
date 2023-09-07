<template>
    <div id="lightset-user">  
        <v-row rows="2">           
            <v-col cols="1"><h4 style="text-align:left">User</h4></v-col>    
            <v-spacer cols="1"/>             
            <v-col cols="1"
                v-for="item in this.user_state"
                :key="item.key"
            >
                <LightCell :cell_label=item.label :cell_value=item.state />
            </v-col>  
            <v-spacer cols="1"/>        
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
        name: 'LightSetUser',        
        components:{
            LightCell: LightCell
        },

        props:['user_state'],

        created: function() {
            Vue.$log.info("LSU init")
            Vue.$log.info("LSU state  " + this.user_state)               
        }           
    }

</script>

<style>
</style>