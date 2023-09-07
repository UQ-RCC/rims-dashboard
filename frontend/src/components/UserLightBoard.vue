<template>
    <v-container height='800px'>
        <v-row rows="2"><v-divider :thickness="4"></v-divider></v-row>
        <v-spacer rows="2"/> 
        <LightSetUser :user_state=this.state.user />
        <v-spacer rows="2"/>   
        <v-spacer rows="2"/>             
        <v-row rows="2"><v-divider :thickness="4"></v-divider></v-row>
        <LightSetProject :proj_state=this.state.user_projects[0] />
        <v-spacer rows="2"/>    
    </v-container>                              
</template>

<script>
    import Vue from 'vue'
    import LightSetUser from './LightSetUser.vue';
    import LightSetProject from './LightSetProject.vue'

    export default {
        name: 'UserLightBoard',
        components:{
            LightSetUser: LightSetUser,
            LightSetProject: LightSetProject
        },
        props:['state'],   

        created: function() {
            Vue.$log.info("init ULB")
            Vue.$log.info("ULB state  " + this.state.user + "/" + this.state.user_projects)               
        }        
        
    }

</script>

<style>
</style>
