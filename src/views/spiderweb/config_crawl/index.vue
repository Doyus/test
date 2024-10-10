<template>
  <div class="container">
    <ConfigPanel 
      :basic-config="basicConfig"
      :list-config="listConfig"
      :detail-config="detailConfig"
      @update:basic-config="updateBasicConfig"
      @update:list-config="updateListConfig"
      @update:detail-config="updateDetailConfig"
      @run-config-test="runConfigTest"
      @load-config="loadConfig"
    />
    <div class="resizer" ref="resizer"></div>
    <LogPanel ref="logPanel" />
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue';
import ConfigPanel from './components/ConfigPanel.vue';
import LogPanel from './components/LogPanel.vue';
import DetailConfig from './components/DetailConfig.vue';
import listConfig from './components/listConfig.vue';
import basicConfig from './components/BasicConfig.vue';

import axios from 'axios';

export default {
  name: 'App',
  components: {
    ConfigPanel,
    LogPanel,
    DetailConfig,
    listConfig,
    basicConfig,
    
  },
  setup() {
    const basicConfig = reactive({
      website_name: '',
      website_category: '',
      info_category: '',
      info_type: '',
      proxy_type: '',
      region: '',
      industry: '',
      start_page: 1,
      end_page: 5,
      interval: 1
    });

    const listConfig = reactive({
      list_url: '',
      list_method: 'GET',
      list_params: '',
      list_encoding: 'utf-8',
      list_headers: '',
      list_cookies: '',
      list_retry: 3,
      list_timeout: 30,
      fields: []
    });

    const detailConfig = reactive({
      detail_url: '',
      detail_method: 'GET',
      detail_params: '',
      detail_encoding: 'utf-8',
      detail_headers: '',
      detail_cookies: '',
      detail_retry: 3,
      detail_timeout: 30,
      fields: []
    });

    const logPanel = ref(null);
    const resizer = ref(null);

    const updateBasicConfig = (newConfig) => {
      Object.assign(basicConfig, newConfig);
    };

    const updateListConfig = (newConfig) => {
      Object.assign(listConfig, newConfig);
    };

    const updateDetailConfig = (newConfig) => {
      Object.assign(detailConfig, newConfig);
    };

    const runConfigTest = async (configType) => {
      const config = {
        req_type: configType,
        basic_config: basicConfig,
        list_config: listConfig,
        detail_config: detailConfig
      };

      if (configType === 'List') {
        delete config.detail_config;
      }

      try {
        const response = await axios.post('/test_config', config);
        logPanel.value.log(`${configType}配置测试结果: ${JSON.stringify(response.data, null, 2)}`);
      } catch (error) {
        logPanel.value.log(`${configType}配置测试失败: ${error.message}`);
      }
    };

    const loadConfig = async () => {
      try {
        const response = await axios.get(`/load_config/${basicConfig.website_name}`);
        const parsedData = response.data;
        updateBasicConfig(parsedData.basic_config);
        updateListConfig(parsedData.list_config);
        updateDetailConfig(parsedData.detail_config);
        logPanel.value.log("配置已成功加载");
      } catch (error) {
        logPanel.value.log(`加载配置时出错: ${error.message}`);
      }
    };

    onMounted(() => {
      // 实现拖拽调整面板大小的逻辑
      let x = 0;
      let leftWidth = 0;

      const mouseDownHandler = function(e) {
        x = e.clientX;
        const leftSide = resizer.value.previousElementSibling;
        leftWidth = leftSide.getBoundingClientRect().width;

        document.addEventListener('mousemove', mouseMoveHandler);
        document.addEventListener('mouseup', mouseUpHandler);
      };

      const mouseMoveHandler = function(e) {
        const dx = e.clientX - x;
        const newLeftWidth = ((leftWidth + dx) * 100) / resizer.value.parentNode.getBoundingClientRect().width;
        resizer.value.previousElementSibling.style.flexBasis = `${newLeftWidth}%`;
      };

      const mouseUpHandler = function() {
        document.removeEventListener('mousemove', mouseMoveHandler);
        document.removeEventListener('mouseup', mouseUpHandler);
      };

      resizer.value.addEventListener('mousedown', mouseDownHandler);
    });

    return {
      basicConfig,
      listConfig,
      detailConfig,
      updateBasicConfig,
      updateListConfig,
      updateDetailConfig,
      runConfigTest,
      loadConfig,
      logPanel,
      resizer
    };
  }
};
</script>

<style>

:root {
  --primary-color: #3498db;
  --secondary-color: #2ecc71;
  --tertiary-color: #e74c3c;
  --background-color: #f0f3f6;
  --panel-background: #ffffff;
  --text-color: #2c3e50;
  --border-color: #bdc3c7;
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  line-height: 1.6;
  margin: 0;
  padding: 0;
  background-color: var(--background-color);
  color: var(--text-color);
  /* border: #27ae60 20px solid; */
}

.container {
  /* width: 100%; */
  display: flex;
  height: 100vh;
  /* border: #27ae60 20px solid; */
  max-width: 100%;

}

.config-panel,
.log-panel {
  background-color: var(--panel-background);
  padding: 20px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  overflow-y: auto;
}

.config-panel {
  flex: 0 0 60%;
  min-width: 300px;
}

.log-panel {
  flex: 1;
  min-width: 200px;
  display: flex;
  flex-direction: column;
}

.resizer {
  width: 8px;
  background-color: var(--border-color);
  cursor: col-resize;
}

h1,
h2 {
  color: var(--primary-color);
  margin-top: 0;
}

.form-section,
.field-group,
.rules-list,
.date-extraction {
  background-color: rgba(255, 255, 255, 0.8);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.form-group {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
  gap: 15px;
}

label {
  flex: 0 0 80px;
  color: var(--text-color);
  text-align: right;
  padding-right: 10px;
  font-weight: 600;
}

input[type="text"],
input[type="number"],
select,
textarea {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  font-size: 14px;
  transition: border-color 0.3s ease;
}

input[type="text"]:focus,
input[type="number"]:focus,
select:focus,
textarea:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.2);
}

/* button {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  transition: background-color 0.3s, transform 0.1s;
} */

button:hover {
  transform: translateY(-1px);
}

button:active {
  transform: translateY(1px);
}

.btn-primary {
  background-color: var(--primary-color);
  color: white;
}

.btn-primary:hover {
  background-color: #2980b9;
}

.btn-secondary {
  background-color: var(--secondary-color);
  color: white;
}

.btn-secondary:hover {
  background-color: #27ae60;
}

.btn-tertiary {
  background-color: var(--tertiary-color);
  color: white;
}

.btn-tertiary:hover {
  background-color: #c0392b;
}

#log {
  flex-grow: 1;
  background-color: #2c3e50;
  border-radius: 4px;
  padding: 10px;
  font-family: 'Courier New', Courier, monospace;
  font-size: 14px;
  color: #ecf0f1;
  overflow-y: auto;
  margin-bottom: 10px;
}

#logContent {
  white-space: pre-wrap;
}

.log-controls {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.field-group-buttons {
  display: flex;
  justify-content: flex-end;
  margin-top: 10px;
}

.field-group-buttons button {
  margin-left: 10px;
}

/* Add more styles as needed */
</style>