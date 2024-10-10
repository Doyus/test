<!-- components/BasicConfig.vue -->
<template>
    <div class="form-section" id="basic_config">
      <h2>基本设置</h2>
      <div class="form-group">
        <label for="website_name">采集源网站名称</label>
        <input type="text" id="website_name" v-model="localConfig.website_name" required>
      </div>
      <div class="form-group">
        <label for="website_category">采集网站栏目</label>
        <input type="text" id="website_category" v-model="localConfig.website_category">
      </div>
      <div class="form-group">
        <label for="info_category">信息分类</label>
        <select id="info_category" v-model="localConfig.info_category" @change="updateInfoType">
          <option value="ZBXX">招标信息</option>
          <option value="XMXX">项目信息</option>
          <option value="tx_add">osc/项目信息</option>
          <option value="czw_add">osc/招标类信息</option>
        </select>
        <label for="info_type">信息类型</label>
        <select id="info_type" v-model="localConfig.info_type">
          <option v-for="type in infoTypes[localConfig.info_category]" :key="type.value" :value="type.value">
            {{ type.label }}
          </option>
        </select>
      </div>
      <div class="form-group">
        <label for="proxy_type">代理服务器选择</label>
        <select id="proxy_type" v-model="localConfig.proxy_type">
          <option value="dynamic">隧道代理-动态</option>
          <option value="30s">隧道代理-30s</option>
          <option value="private">私密代理</option>
          <option value="none">不启用</option>
        </select>
      </div>
      <div class="form-group">
        <label for="region">所属地区</label>
        <select id="region" v-model="localConfig.region">
          <option v-for="(value, key) in areaDict" :key="key" :value="value">{{ key }}</option>
        </select>
      </div>
      <div class="form-group">
        <label for="industry">行业</label>
        <select id="industry" v-model="localConfig.industry">
          <option v-for="(value, key) in cateDict" :key="key" :value="key">{{ value }}</option>
        </select>
      </div>
      <div class="form-group">
        <label for="start_page">采集起始页</label>
        <input type="number" id="start_page" v-model="localConfig.start_page">
        <label for="end_page">采集结束页</label>
        <input type="number" id="end_page" v-model="localConfig.end_page">
        <label for="interval">间隔</label>
        <input type="number" id="interval" v-model="localConfig.interval">
      </div>
      <div class="form-group">
        <label for="cron_expression">定时(每隔几分钟)</label>
        <input type="number" id="cron_expression" v-model="localConfig.cron_expression">
      </div>
    </div>
  </template>
  
  <script>
  import { ref, reactive, watch } from 'vue';
  
  export default {
    name: 'BasicConfig',
    props: {
      config: Object,
    },
    emits: ['update:config'],
    setup(props, { emit }) {
      const localConfig = reactive({ ...props.config });
  
      const infoTypes = reactive({
        "ZBXX": [
          { "value": "ZBGS", "label": "中标公示" },
          { "value": "ZBGG", "label": "招标公告" }
        ],
      });
  
      const areaDict = reactive({
        "未设置": -1,
        "北京": 1,
        "上海": 2,
      });
  
      const cateDict = reactive({
        "0": "未设置",
        "1": "交通运输",
        "2": "网络通讯计算机",
      });
  
      const updateInfoType = () => {
        if (localConfig.info_category === "ZBXX") {
          localConfig.info_type = "ZBGG";
        }
      };
  
      watch(localConfig, (newValue) => {
        emit('update:config', newValue);
      }, { deep: true });
  
      return {
        localConfig,
        infoTypes,
        areaDict,
        cateDict,
        updateInfoType,
      };
    },
  };
  </script>
  
  <style scoped>
  
  </style>