<template>
  <div class="panel">
    <div class="search-wrap">
      <div class="left">
        <el-input
            class="search-input"
            v-model="searchQuery"
            placeholder="搜索"
            clearable
        />
        <el-button @click="onGetMonitorData()">搜索</el-button>
        <div class="spacer"></div>
      </div>
    </div>
    <br>
    <div class="panel-body">
      <el-table
          :empty-text="$lang.cteate_task.noData"
          :data="tymonitors"
          v-loading="loading"
          :element-loading-text="$lang.cteate_task.loading"
      >
        <el-table-column
            align="center"
            prop="id"
            :label="$lang.cteate_task.id"
        >
        </el-table-column>

        <el-table-column
            align="center"
            prop="title"
            :label="$lang.columns.title"
        >
        </el-table-column>
        <el-table-column
            align="center"
            prop="pub_date"
            :label="$lang.columns.pub_time"
        >
        </el-table-column>

        <el-table-column align="center" :label="$lang.columns.view">
          <template slot-scope="scope">
            <router-link
                :to="{ name: 'CreateTaskDetail', params: { id: scope.row.id } }"
                tag="span"
            >
              <el-button type="info" size="mini">
                <i class="fa fa-edit"></i>
                {{ $lang.buttons.result }}
              </el-button>
            </router-link>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination
          v-model="pagination.currentPage"
          :total="pagination.total"
          :current-page.sync="pagination.currentPage"
          @page-change="onGetMonitorData"
          :page-size="pagination.pageSize">
      </el-pagination>
    </div>


  </div>
</template>
<style>
.search-wrap {
  display: flex;
  justify-content: space-between;

}

.left {
  display: flex;
  align-items: center;
}

.right {
  display: flex;
  align-items: center;

}
.spacer {
  width: 10%;
  display: flex;
  align-items: center;
}
</style>
<script>

export default {
  watch: {
    'pagination.currentPage':{
      handler() {
        // eslint-disable-next-line
        this.onGetMonitorData();
      },
      deep: true
    }
  },
 name: "tymonitors",
 props: {},
 data() {
   return {
     searchQuery:null, //搜索关键词
     tyif: '1',//1 代表特源,2 代表非特源
     tymonitors: null,
     loading: true,
     routeId: this.$route.params.id,
     // to store batch selected id of monitor
     monitorStatus: {},
     statusClass: {
       "1": "success",
       "0": "warning",
       "-1": "danger",
     },
     statusText: {
       "1": this.$store.getters.$lang.buttons.normal,
       "0": this.$store.getters.$lang.buttons.connecting,
       "-1": this.$store.getters.$lang.buttons.error,
     },
     pagination: {
       currentPage: 10,
       pageSize: 20,
       total: 1000
     }
   };
 },
 created() {
   this.onGetMonitorData();
 },
 methods: {
   handleChangeType(type) {
     this.tyif = type;
     this.onGetMonitorData();
   },
   onRefresh() {
     this.onGetMonitorData();
   },
   onGetmonitorStatus() {
     this.tymonitors.forEach((monitor) => {
       this.onGetMonitorStatus(monitor.pk);
     });
   },

   onGetMonitorData() {
     this.loadData = true;
     this.$http
         .get(
             this.formatString(this.$store.state.url.cteate_task.result, {
               page: this.pagination.currentPage,
               id: this.routeId,
               pageSize: this.pagination.pageSize,
               searchQuery:this.searchQuery
             })
         )
         .then(({ data: tymonitors }) => {
           this.tymonitors = tymonitors;
           this.loading = false;
           this.onGetmonitorStatus();
           this.pagination.total =100;
         })
         .catch(() => {
           this.loadData = false;
         });
   },
   onGetDetailData(id) {
     // this.loading = false;
     let params =id['id'];
     console.log(id)
     // eslint-disable-next-line no-debugger
     debugger;
     window.open(this.$root.$data.globalConfig.openServerUrl+params, '_blank');
     this.loading = false;
   },

 },

};
</script>