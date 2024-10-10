<!-- components/ListConfig.vue -->
<template>
    <div class="form-section" id="list_config">
      <h2>列表页配置</h2>
      <div class="form-group">
        <label for="list_url">请求地址</label>
        <input type="text" id="list_url" v-model="localConfig.list_url" required>
      </div>
      <div class="form-group">
        <label for="list_method">请求方式</label>
        <select id="list_method" v-model="localConfig.list_method">
          <option value="GET">GET</option>
          <option value="POST">POST</option>
          <option value="JSON">JSON</option>
        </select>
      </div>
      <div class="form-group">
        <label for="list_params">请求参数设置</label>
        <textarea id="list_params" v-model="localConfig.list_params"></textarea>
      </div>
      <div class="form-group">
        <label for="list_encoding">响应编码</label>
        <input type="text" id="list_encoding" v-model="localConfig.list_encoding">
      </div>
      <div class="form-group">
        <label for="list_headers">请求头设置</label>
        <textarea id="list_headers" v-model="localConfig.list_headers"></textarea>
      </div>
      <div class="form-group">
        <label for="list_cookies">Cookie设置</label>
        <textarea id="list_cookies" v-model="localConfig.list_cookies"></textarea>
      </div>
      <div class="form-group">
        <label for="list_retry">失败尝试次数</label>
        <input type="number" id="list_retry" v-model="localConfig.list_retry">
      </div>
      <div class="form-group">
        <label for="list_timeout">最大等待时间(秒)</label>
        <input type="number" id="list_timeout" v-model="localConfig.list_timeout">
      </div>
      <div id="fieldContainerList">
        <div v-for="(field, index) in localConfig.fields" :key="index" class="field-group">
          <h3>{{ getFieldLabel(field.field_name) }}</h3>
          <div class="form-group">
            <label :for="`field_type_List_${index}`">字段类型:</label>
            <select :id="`field_type_List_${index}`" v-model="field.field_type">
              <option value="XPath">XPath</option>
              <option value="Regex">正则表达式</option>
            </select>
          </div>
          <div class="form-group">
            <label :for="`expression_List_${index}`">提取表达式:</label>
            <input type="text" :id="`expression_List_${index}`" v-model="field.expression">
          </div>
          <div class="form-group">
            <label :for="`prefix_List_${index}`">前置值:</label>
            <input type="text" :id="`prefix_List_${index}`" v-model="field.prefix">
          </div>
          <div class="form-group">
            <label :for="`suffix_List_${index}`">后置值:</label>
            <input type="text" :id="`suffix_List_${index}`" v-model="field.suffix">
          </div>
          <div class="replace-rule-container">
            <div v-for="(rule, ruleIndex) in field.replace_rules" :key="ruleIndex" class="replace-rule">
              <input type="text" v-model="rule.old_value" placeholder="旧值">
              <input type="text" v-model="rule.new_value" placeholder="新值">
              <button type="button" @click="removeReplaceRule(index, ruleIndex)">删除规则</button>
            </div>
          </div>
          <div class="field-group-buttons">
            <button type="button" @click="addReplaceRule(index)">添加替换规则</button>
            <button type="button" @click="removeField(index)">删除字段</button>
          </div>
        </div>
      </div>
      <div class="button_bottom" style="text-align: right;">
        <button type="button" @click="showFieldSelection">添加字段</button>
        <button type="button" @click="runConfigTest" class="btn-secondary">运行</button>
      </div>
      <!-- 字段选择弹出框 -->
      <div v-if="showFieldModal" class="modal">
        <div class="modal-content">
          <h3>选择字段类型</h3>
          <select v-model="selectedFieldType">
            <option v-for="(label, value) in fieldLabelMap" :key="value" :value="value">{{ label }}</option>
          </select>
          <button @click="addField">确认添加</button>
          <button @click="showFieldModal = false">取消</button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, reactive, watch } from 'vue';
  
  export default {
    name: 'DetailConfig',
    props: {
      config: Object,
    },
    emits: ['update:config', 'run-config-test'],
    setup(props, { emit }) {
      const localConfig = reactive({ ...props.config });
      const showFieldModal = ref(false);
      const selectedFieldType = ref('');
  
      const fieldLabelMap = {
        "list_rule": "列表页规则",
        "title": "标题",
        "publish_date": "发布日期",
        "link": "链接",
        "content": "内容",
        "region": "地区",
        "industry": "行业",
        "id": "ID"
      };
  
      const getFieldLabel = (fieldName) => {
        return fieldLabelMap[fieldName] || fieldName;
      };
  
      const showFieldSelection = () => {
        showFieldModal.value = true;
      };
  
      const addField = () => {
        if (selectedFieldType.value) {
          localConfig.fields.push({
            field_name: selectedFieldType.value,
            field_type: 'XPath',
            expression: '',
            prefix: '',
            suffix: '',
            replace_rules: []
          });
          showFieldModal.value = false;
          selectedFieldType.value = '';
        }
      };
  
      const removeField = (index) => {
        localConfig.fields.splice(index, 1);
      };
  
      const addReplaceRule = (fieldIndex) => {
        localConfig.fields[fieldIndex].replace_rules.push({ old_value: '', new_value: '' });
      };
  
      const removeReplaceRule = (fieldIndex, ruleIndex) => {
        localConfig.fields[fieldIndex].replace_rules.splice(ruleIndex, 1);
      };
  
      const runConfigTest = () => {
        emit('run-config-test', 'List');
      };
  
      watch(localConfig, (newValue) => {
        emit('update:config', newValue);
      }, { deep: true });
  
      return {
        localConfig,
        showFieldModal,
        selectedFieldType,
        fieldLabelMap,
        getFieldLabel,
        showFieldSelection,
        addField,
        removeField,
        addReplaceRule,
        removeReplaceRule,
        runConfigTest
      };
    }
  };
  </script>
  
  <style scoped>
  </style>