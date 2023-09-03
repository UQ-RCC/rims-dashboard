<template>
    <div id="lightset-user">  
        {{ localstate }}
    </div>        
</template>

<script>
    import Vue from 'vue'
    
    export default {
        name: 'LightSetUser',        
        props:['localstate'],

        created: function() {
            Vue.$log.info("LSU init")
            Vue.$log.info("LSU state  " + this.localstate)               
        }           
    }

</script>

<style>
</style>