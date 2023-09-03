<template>
    <div id="user-lightboard">  
        {{ state }}
        <div>
            <LightSetMaster :localstate=this.state.core />    
            <LightSetUser :localstate=this.state.user />           
            <LightSetProject :localstate=this.state.projects[0] />
        </div>
    </div>        
</template>

<script>
    import Vue from 'vue'
    import LightSetMaster from './LightSetMaster.vue'
    import LightSetUser from './LightSetUser.vue';
    import LightSetProject from './LightSetProject.vue'

    export default {
        name: 'UserLightBoard',
        components:{
            LightSetMaster: LightSetMaster,
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
