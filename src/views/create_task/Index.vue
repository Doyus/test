<template>
  <div class="iframe-container">
    <button @click="openInNewTab">在新标签页中打开</button>
    <iframe :src="iframeUrl" frameborder="0"></iframe>
  </div>
</template>

<script>
export default {
  data() {
    return {
    };
  },
  computed: {
    iframeUrl() {
      return this.$root.$data.globalConfig.cteateServerUrl;
    },
  },
  methods: {
    openInNewTab() {
      window.open(this.iframeUrl, '_blank');
    },
  },
};
</script>

<style scoped>
.iframe-container {
  width: 100%;
  height: 100vh; /* 设置容器高度为视口的 100% */
  overflow: hidden; /* 防止容器出现滚动条 */
}

iframe {
  width: 100%;
  height: 100%;
  border: none; /* 移除边框 */
  scrolling: no; /* 移除滚动条 */
}
</style>