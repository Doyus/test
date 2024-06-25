<template>
    <div class="main-content ofh" :style="{ 'margin-left': isCollapsed ? '10px' : '220px' }">
    <g-header></g-header>
    <div class="wrapper">
      <div class="pageContent">
        <el-row>
          <el-col :span="24">
            <slot></slot>
          </el-col>
        </el-row>
      </div>
    </div>
    <g-footer></g-footer>
  </div>
</template>

<script>
import GHeader from "./Header";
import GFooter from "./Footer";

export default {
  name: "Wrapper",
  components: {
    GHeader,
    GFooter,
  },
  data() {
    return {
      isCollapsed: false,
    };
  },
  mounted() {
    // 监听 Left 组件的 isCollapsed 值变化
    this.$root.$on("toggleSidebar", (isCollapsed) => {
      this.isCollapsed = isCollapsed;
    });
  },
};
</script>