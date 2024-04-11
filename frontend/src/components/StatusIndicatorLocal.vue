<!--component derived from:
https://github.com/coderdiaz/vue-status-indicator/tree/master
Copyright (c) 2018 Javier Diaz Chamorro
-->

<template>
    <span class="status-indicator" :[modifiedStatus]="true" :pulse="pulse" :border="border">
      <span class="status-label">{{ label }}</span>
    </span>      
</template>


<script>

export default 
{
  name: 'StatusIndicator',

  props: 
  {
    status: 
    {
      type: String,
      default: '',
      validator(value) 
      {
        if (value === '') return true;
        return ['none', 'incomplete', 'off', 'ready', 'extended', 'warn', ].indexOf(value) !== -1;
      },
    },
    pulse: 
    {
      type: Boolean,
      default: false,
    },
    label: 
    {
      type: String,
      default: '',
    },
    border: 
    {
      type: Boolean,
      default: false,
    },
  },
  
  computed:
  {
    modifiedStatus() 
    {
      if (this.status.includes('_')) 
      {
        return this.status.split('_')[1];  
      } 
      else 
      {
        return this.status
      }
    },
  },
}

</script>

<style src="../assets/status-indicator.css"></style>


<!--
MIT License

Copyright (c) 2018 Javier Diaz Chamorro
Adapted (c) 2023 Lachlan Casey at the University of Queensland

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
-->