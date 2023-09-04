<template>
    <div id="user-lightboard">  
        <div> 
            <v-row><h4 style="text-align:left">User</h4></v-row> 
            <LightSetUser :localstate=this.state.user />
            <v-row></v-row>   
            <v-row><h4 style="text-align:left">Projects</h4></v-row>       
            <LightSetProject :localstate=this.state.projects[0] />
        </div>
        <div>       
            {{this.state.user}}
            {{this.state.projects[0]}}
        </div>           
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
            Vue.$log.info("ULB state  " + this.state.core + "/" + this.state.user + "/" + this.state.projects)               
        }        
        
    }

</script>

<style>
</style>
