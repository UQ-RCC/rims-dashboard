<template>
    <div id="lightcell">  
        {{ localval }}
    </div>        
</template>

<script>
    import Vue from 'vue'
    
    export default {
        name: 'LightCell',
        props:['localval'],

        created: function() {
            Vue.$log.info("LC val  " + this.localval)               
        }       
        
    }

</script>

<style>
</style>