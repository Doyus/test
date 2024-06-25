<template>
  <div class="left-side" :class="{ collapsed: isCollapsed }">
     <!-- 新增其他代码 -->
     <!-- <button class="toggle-btn" @click="toggle"><i class="fa fa-bars"></i></button> -->
     <div class="toggle-btn-container">
      <button class="toggle-btn" @click="toggle">
        <i class="fa fa-bars"></i>
      </button>
    </div>

    <div class="left-side-inner">
      <router-link to="/home" class="logo block">
        <img src="../assets/images/logo.png" alt="Gerapy" />
      </router-link>
      <el-menu
        class="menu-box"
        theme="dark"
        router
        :default-active="$route.path"
      >
        <el-menu-item class="menu-list" index="/client">
          <i class="icon fa fa-television"></i>
          <span v-text="$lang.menus.clients" class="text"></span>
        </el-menu-item>
        <el-menu-item class="menu-list" index="/project">
          <i class="icon fa fa-folder-o"></i>
          <span v-text="$lang.menus.projects" class="text"></span>
        </el-menu-item>
        <el-menu-item class="menu-list" index="/task">
          <i class="icon fa fa-hdd-o"></i>
          <span v-text="$lang.menus.tasks" class="text"></span>
        </el-menu-item>
        <el-menu-item class="menu-list" index="/tymonitor">
          <i class="icon fa fa-hdd-o"></i>
          <span v-text="$lang.menus.tymonitors" class="text"></span>
        </el-menu-item>

        <el-menu-item class="menu-list" index="/xyresult">
          <i class="icon fa fa-hdd-o"></i>
          <span v-text="$lang.menus.xyresults" class="text"></span>
        </el-menu-item>

        <el-menu-item class="menu-list" index="/pyspider">
          <i class="icon fa fa-hdd-o"></i>
          <span v-text="$lang.menus.pyspider" class="text"></span>
        </el-menu-item>
        <el-menu-item class="menu-list" index="/create_task">
          <i class="icon fa fa-hdd-o"></i>
          <span v-text="$lang.menus.create_task" class="text"></span>
        </el-menu-item>
        <el-menu-item class="menu-list" index="/task_list">
          <i class="icon fa fa-hdd-o"></i>
          <span v-text="$lang.menus.task_list" class="text"></span>
        </el-menu-item>
      </el-menu>
    </div>
  </div>
</template>
<script>
export default {
  name: "Left",
};
</script>
<style scoped>
.left-side .logo {
  text-align: left !important;
}

.left-side .logo img {
  width: 150px;
  margin-left: 10px;
}

.left-side .el-menu {
  border-right: none;
}
</style>
<script>
export default {
  name: 'Left',
  data() {
    return {
      isCollapsed: false
    }
  },
  methods: {
    toggle() {
      this.isCollapsed = !this.isCollapsed;
      this.$root.$emit('toggleSidebar', this.isCollapsed)

    }
  }
}
</script>