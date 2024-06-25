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
<!--          <el-table-column-->
<!--              align="center"-->
<!--              prop="id"-->
<!--              :label="id"-->
<!--          >-->
<!--          </el-table-column>-->

          <el-table-column
              align="center"
              prop="website_name"
              :label="$lang.cteate_task.website_name"
          >
          </el-table-column>
          <el-table-column
              align="center"
              prop="class_name"
              :label="$lang.cteate_task.class_name"
          >
          </el-table-column>
          <el-table-column
              align="center"
              prop="crawl_start_time"
              :label="$lang.cteate_task.crawl_start_time"
          >
          </el-table-column>
          <el-table-column
              align="center"
              prop="crawl_end_time"
              :label="$lang.cteate_task.crawl_end_time"
          >
          </el-table-column>
          <el-table-column
              align="center"
              prop="status"
              :label="$lang.cteate_task.status"
          >
          </el-table-column>
          <el-table-column
              align="center"
              prop="crawl_next_time"
              :label="$lang.cteate_task.crawl_next_time"
          >
          </el-table-column>
          <el-table-column
              align="center"
              prop="crawl_consuming_time"
              :label="$lang.cteate_task.crawl_consuming_time"
          >
          </el-table-column>
          <el-table-column align="center" :label="$lang.columns.view">
            <template slot-scope="scope">
              <el-button
                  type="info"
                  size="mini"
                  @click="onGetDetailData(scope.row)"
              >
                <i class="fa fa-edit"></i>
                编辑
              </el-button>

              <router-link
                  :to="{ name: 'CreateTaskEdit', params: { id: scope.row.id } }"
                  tag="span"
              >
                <el-button type="info" size="mini">
                  <i class="fa fa-edit"></i>
                  {{ $lang.buttons.schedule }}
                </el-button>
              </router-link>

              <router-link
                  :to="{ name: 'CreateTaskResult', params: { id: scope.row.id } }"
                  tag="span"
              >
                <el-button type="info" size="mini">
                  <i class="fa fa-edit"></i>
                  {{ $lang.buttons.result }}
                </el-button>
              </router-link>

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
     // let params = {
     //   page: this.pagination.currentPage,
     //   tyif: this.tyif,
     //   pageSize: this.pagination.pageSize,
     //   searchQuery:this.searchQuery
     // };
     this.loading = true;
     this.$http
         .get(this.$store.state.url.cteate_task.task_List)
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