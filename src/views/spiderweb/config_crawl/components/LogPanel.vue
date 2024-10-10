<!-- components/LogPanel.vue -->
<template>
    <div class="log-panel">
      <h2>日志输出</h2>
      <div id="log" ref="logContainer">
        <pre>{{ logContent }}</pre>
      </div>
      <div class="log-controls">
        <button @click="clearLog" class="btn-tertiary">清空日志</button>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, onMounted, watch } from 'vue';
  
  export default {
    name: 'LogPanel',
    setup() {
      const logContent = ref('');
      const logContainer = ref(null);
  
      const log = (message) => {
        const timestamp = new Date().toLocaleTimeString();
        let formattedMessage;
        try {
          const jsonObject = JSON.parse(message);
          formattedMessage = JSON.stringify(jsonObject, null, 2);
        } catch (error) {
          formattedMessage = message;
        }
        logContent.value += `${timestamp}: ${formattedMessage}\n`;
      };
  
      const clearLog = () => {
        logContent.value = '';
      };
  
      onMounted(() => {
        const observer = new MutationObserver(() => {
          if (logContainer.value) {
            logContainer.value.scrollTop = logContainer.value.scrollHeight;
          }
        });
  
        if (logContainer.value) {
          observer.observe(logContainer.value, { childList: true, subtree: true });
        }
      });
  
      watch(logContent, () => {
        if (logContainer.value) {
          logContainer.value.scrollTop = logContainer.value.scrollHeight;
        }
      });
  
      return {
        logContent,
        logContainer,
        log,
        clearLog
      };
    }
  };
  </script>
  
  <style scoped>
  .log-panel {
  flex: 1;
  min-width: 200px;
  display: flex;
  flex-direction: column;
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

  </style>