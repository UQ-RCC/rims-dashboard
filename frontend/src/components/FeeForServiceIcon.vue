<template>
    <v-icon :size="size">
      {{ value === 'Autonomous work' ? 'mdi-account' : 'mdi-file-send' }}
    </v-icon>
  </template>
  
  <script>
  export default {
    props: {
      value: {
        type: String,
        required: true
      },
      size: {
        type: [String, Number],
        default: 'x-large',
      }      
    }
  }
  </script>