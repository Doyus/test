<template>
  <div class="header-section">
    <div class="pull-right">
      <div class="fixed-user">
        <lang-switch></lang-switch>
        <user></user>
      </div>    
    </div>
  </div>
</template>
<script>
import User from "./User";
import LangSwitch from "./LangSwitch";

export default {
  components: {
    User,
    LangSwitch,
  },
};
</script>
<style scoped>
.header-section {
  position: relative; /* 添加这一行 */
}

.fixed-user {
  position: fixed;
  top: 0px; /* 调整顶部位置 */
  right: -230px; /* 调整右侧位置 */
  z-index: 999; /* 确保在最上层 */
}
</style>
