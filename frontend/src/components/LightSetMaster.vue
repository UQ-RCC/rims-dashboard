<template>
    <div id="lightset-master">  
        {{ localstate }}
    </div>        
</template>

<script>
    import Vue from 'vue'
    
    export default {
        name: 'LightSetMaster',        
        props:['localstate'],
    
        created: function() {
            Vue.$log.info("LSM init")
            Vue.$log.info("LSM state  " + this.localstate)               
        }           
    
    }

</script>

<style>
</style>