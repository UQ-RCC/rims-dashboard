<template>
    <div id="lightset-project">  
        {{ localstate }}
    </div>        
</template>

<script>
    import Vue from 'vue'
    
    export default {
        name: 'LightSetProject',
        props:['localstate'],

        created: function() {
            Vue.$log.info("LSP init")
            Vue.$log.info("LSP state  " + this.localstate)               
        }       
        
    }

</script>

<style>
</style>