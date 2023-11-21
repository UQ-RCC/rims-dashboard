<template>
    <div>        
        Welcome to the dashboard.

    </div>
</template>

<script>
    import Vue from 'vue'
    import VueLogger from 'vuejs-logger'    

    Vue.use(VueLogger)

    Vue.$log.info("Home init")

    export default {
        name: 'Home',
        data() {
            return {
            }
        },
        methods: {
            mounted: function() {
                Vue.$log.info("App mounted");
            }
        },

    }

    Vue.$log.info("Home end init")
</script>