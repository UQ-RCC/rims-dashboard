<template>
  <v-app id="app">
    <navbar />
    <v-main>
      <notifications group="sysnotif" position="top left"/>
      <notifications group="datanotif" position="bottom right"/>
      <div>
          <router-view />
      </div>
    </v-main>
    <v-footer app>
        <v-row justify="end">
            <a href="https://github.com/UQ-RCC/rims-dashboard">RIMS Dashboard</a>
        </v-row>
    </v-footer>  
  </v-app>
</template>

<script>
  import Navbar from "@/components/Navbar.vue";

  import Vue from 'vue'
  import VueLogger from 'vuejs-logger'

  Vue.use(VueLogger)

  Vue.$log.info("APP init")


  export default {
    name: "App",
    components: {
        Navbar
    },
    data() {
        return {
        }
    },
    
    methods: {
      mounted: function() {

      }
    },
  };


  Vue.$log.info("APP end init")
</script>

<style>
  * {
    text-transform: initial;
  }

  .v-list-group__header__prepend-icon {
    margin-right: 10px;
  }
</style>
  