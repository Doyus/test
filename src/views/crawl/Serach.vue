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
            :empty-text="$lang.messages.noData"
            :data="tymonitors"
            v-loading="loading"
            :element-loading-text="$lang.messages.loading"
        >
          <el-table-column
              align="center"
              prop="sourceName"
              :label="$lang.columns.crawlName"
          >
          </el-table-column>
          <el-table-column
              align="center"
              prop="updateTime"
              :label="$lang.columns.updateTime"
          >
          </el-table-column>
          <el-table-column
              align="center"
              prop="area"
              :label="$lang.columns.area"
          >
          </el-table-column>
          <el-table-column align="center" :label="$lang.columns.view">
            <template slot-scope="scope">
              <el-button
                  type="danger"
                  size="mini"
                  @click="onGetDetailData(scope.row)"
              >
                <i class=""></i>
                查看
              </el-button>
            </template>
          </el-table-column>
          <el-pagination
              v-model="pagination.currentPage"
              :total="pagination.total"
              :current-page.sync="pagination.currentPage"
              @page-change="onGetMonitorData"
              :page-size="pagination.pageSize">
          </el-pagination>
        </el-table>
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
 name: "tymonitors",
 props: {},
 data() {
   return {
     searchQuery:null, //搜索关键词
     tyif: '1',//1 代表特源,2 代表非特源
     tymonitors: null,
     loading: true,
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
       currentPage: 1,
       pageSize: 20,
       total: 0
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
     let params = {
       page: this.pagination.currentPage,
       tyif: this.tyif,
       pageSize: this.pagination.pageSize,
       searchQuery:this.searchQuery
     };
     this.loading = true;
     this.$http
         .post(this.$store.state.url.crawl.index,{params})
         .then(({ data: tymonitors }) => {
           this.tymonitors = tymonitors.data;
           this.loading = false;
           this.onGetmonitorStatus();
           this.pagination.total = tymonitors.total;

         })
         .catch(() => {
           this.loading = false;
         });
   },
   onGetDetailData(id) {
     let params =id['md5'];
     let routeData= this.$router.resolve({ path: "crawl/detail",query:{'params':params}});
     window.open(routeData.href, '_blank');
     this.loading = false;
   },
 },

};
</script>