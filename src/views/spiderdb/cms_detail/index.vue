<template>
  <div>
    <DemoDrawer></DemoDrawer>
  </div>
</template>
<script lang="ts">
  import { defineComponent } from 'vue';

  import { BasicTable, useTable, TableAction } from '/@/components/Table';
  import DemoDrawer from './Drawer.vue';
  export default defineComponent({
    name: 'Demo',
    components: { BasicTable, DemoDrawer, TableAction, BasicUpload, Space }});
</script>
