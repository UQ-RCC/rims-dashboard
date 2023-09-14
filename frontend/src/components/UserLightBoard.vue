<template>
    <div> 
        <div>                  
            <v-row rows="1"><v-divider :thickness="4"></v-divider></v-row>
            <v-row rows="1"><h4 style="text-align:left">User</h4></v-row>                     
            <v-row rows="1">
                <LightSetUser :user_state=this.state.user_state />      
            </v-row>  
        </div>          
        <div>  
            <v-row rows="1"><v-divider :thickness="4"></v-divider></v-row>  
            <v-row rows="1"><h4 style="text-align:left">Projects</h4></v-row>   
            <v-row rows="1" 
                v-for="item in this.state.user_projects"
                :key="item.metadata.PojectRef"     
            >
                    <LightSetProject :proj_state=item />            
            </v-row>
        </div>                          
    </div>     
</template>

<script>
    import LightSetUser from './LightSetUser.vue';
    import LightSetProject from './LightSetProject.vue'

    export default {
        name: 'UserLightBoard',
        components:{
            LightSetUser: LightSetUser,
            LightSetProject: LightSetProject
        },
        props:['state'],   
   
        
    }

</script>

<style>
.fill-height {
  overflow-y: auto;
}


</style>
