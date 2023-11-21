<template>
  <v-app id="app">

  </v-app>
</template>

<script>
//import Navbar from "@/components/Navbar.vue";
//<navbar /> FROMHTML-----> MOVE TO below <v-app id="app">

import Vue from 'vue'
import VueLogger from 'vuejs-logger'

Vue.use(VueLogger)

Vue.$log.info("App init")


export default {
  name: "App",
  components: {
//      Navbar
  },
  data() {
      return {
      }
  },
  methods: {
    setup: function() {
      Vue.$log.info("App beforecreate");
    },

    mounted: function() {
      Vue.$log.info("App mounted");
    }
  },
};


Vue.$log.info("App end init")
</script>

<style>

</style>

<!--
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




* {
  text-transform: initial;
}

.v-list-group__header__prepend-icon {
  margin-right: 10px;
}
-->
  