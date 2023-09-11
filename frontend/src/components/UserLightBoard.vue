<template>
    <div>        
        <v-row rows="1"><v-divider :thickness="4"></v-divider></v-row>
        <v-row rows="1">
            <LightSetUser :user_state=this.state.user />      
        </v-row>  
        <v-row rows="1"><v-divider :thickness="4"></v-divider></v-row>  
        <v-row rows="1">      
            <LightSetProject :proj_state=this.state.user_projects[0] />            
        </v-row>
    </div>                          
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
