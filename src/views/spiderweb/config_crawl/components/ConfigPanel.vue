<!-- components/ConfigPanel.vue -->
<template>
    <div class="config-panel">
      <form @submit.prevent="handleSubmit">
        <BasicConfig
          :config="basicConfig"
          @update:config="updateBasicConfig"
        />
        <ListConfig
          :config="listConfig"
          @update:config="updateListConfig"
        />
        <DetailConfig
          :config="detailConfig"
          @update:config="updateDetailConfig"
        />
        <div class="footer">
          <button type="submit" class="btn-primary" @click="$emit('run-config-test', 'Save')">保存配置</button>
          <button type="button" class="btn-secondary" @click="$emit('run-config-test', 'Test')">测试爬虫</button>
          <button type="button" class="btn-tertiary" @click="$emit('load-config')">加载配置</button>
        </div>
      </form>
    </div>
  </template>
  
  <script>
  import { defineComponent } from 'vue';
  import BasicConfig from './BasicConfig.vue';
  import ListConfig from './ListConfig.vue';
  import DetailConfig from './DetailConfig.vue';
  
  export default defineComponent({
    name: 'ConfigPanel',
    components: {
      BasicConfig,
      ListConfig,
      DetailConfig
    },
    props: {
      basicConfig: Object,
      listConfig: Object,
      detailConfig: Object
    },
    emits: ['update:basic-config', 'update:list-config', 'update:detail-config', 'run-config-test', 'load-config'],
    setup(props, { emit }) {
      const updateBasicConfig = (newConfig) => {
        emit('update:basic-config', newConfig);
      };
  
      const updateListConfig = (newConfig) => {
        emit('update:list-config', newConfig);
      };
  
      const updateDetailConfig = (newConfig) => {
        emit('update:detail-config', newConfig);
      };
  
      const handleSubmit = () => {
        // 处理表单提交
      };
  
      return {
        updateBasicConfig,
        updateListConfig,
        updateDetailConfig,
        handleSubmit
      };
    }
  });
  </script>
  
  <style scoped>
  </style>