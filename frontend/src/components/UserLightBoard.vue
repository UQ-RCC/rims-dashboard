<template>
    <div> 
        <div>                  
            <v-row rows="1"><v-divider :thickness="4"></v-divider></v-row>
            <v-row rows="1"><h4 style="text-align:left">User</h4></v-row>                     
            <v-row rows="1">
                <LightSetUser :user_result=this.board_state.user_result />      
            </v-row>  
        </div>          
        <div>  
            <v-row rows="1"><v-divider :thickness="4"></v-divider></v-row>  
            <v-row rows="1"><h4 style="text-align:left">Projects</h4></v-row>   

        </div>                          
    </div>     
</template>

<!---
<v-row rows="1" 
v-for="item in this.board_state.projects_results"
:key="item.metadata.PojectRef"     
>
    <LightSetProject :proj_state=item />            
</v-row>
-->

<script>
    import LightSetUser from './LightSetUser.vue';
    //import LightSetProject from './LightSetProject.vue'

    export default {
        name: 'UserLightBoard',
        components:{
            LightSetUser: LightSetUser,
        //    LightSetProject: LightSetProject
        },
        props:['board_state'],   
   
        
    }

</script>

<style>
.fill-height {
  overflow-y: auto;
}


</style>
