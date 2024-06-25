<template>
  <div class="panel">
    <div class="search-wrap">
        <div class="left">
          <el-button @click="handleChangeType('1')">特源</el-button>
          <el-button @click="handleChangeType('2')">非特源</el-button>
        </div>
        <div class="right">
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
    

    <panel-title :title="$lang.objects.tymonitors">
      <el-button @click="onRefresh" size="mini">
        <i class="fa fa-refresh"></i>
        {{ $lang.buttons.refresh }}
      </el-button>
      <router-link :to="{ name: 'tymonitorCreate' }" tag="span">
        <el-button type="success" size="mini">
          <i class="fa fa-plus"></i>
          {{ $lang.buttons.create }}
        </el-button>
      </router-link>
    </panel-title>
    <div class="panel-body">
        <el-table
          :empty-text="$lang.messages.noData"
          :data="tymonitors"
          v-loading="loading"
          :element-loading-text="$lang.messages.loading"
          border
        >
          <el-table-column
            align="center"
            :label="$lang.columns.status"
            width="100"
          >
                <template slot-scope="props">
                  <el-button
                    :type="statusClass[monitorStatus[props.row.pk]]"
                    size="mini"
                  >
                    {{ statusText[monitorStatus[props.row.pk]] }}
                  </el-button>
                </template>
          </el-table-column>
          <el-table-column
            align="center"
            prop="pk"
            :label="$lang.columns.id"
            width="60"
          >
          </el-table-column>
          <!-- <el-table-column
            align="center"
            prop="fields.sourceName"
            :label="$lang.columns.sourceName"
          >
          </el-table-column> -->

          <el-table-column align="center" prop="fields.sourceName" :label="$lang.columns.sourceName" width="260">
            <template slot-scope="scope">
              <a :href="generateUrl(scope.row.fields.tylink)" target="_blank">
                {{ scope.row.fields.sourceName }}
              </a>
            </template>
          </el-table-column>


          <el-table-column
            align="center"
            prop="fields.qr"
            :label="$lang.columns.qr"
            width="200"
          >
          </el-table-column>
          <el-table-column
            align="center"
            prop="fields.zr"
            :label="$lang.columns.zr"
            width="200"
          >
          </el-table-column>
          <el-table-column
            align="center"
            prop="fields.jr"
            :label="$lang.columns.jr"
            width="200"
          >
          </el-table-column>

          <el-table-column
            align="center"
            prop="fields.who"
            :label="$lang.columns.who"
            width="200"
          >
          </el-table-column>

          <el-table-column
            align="center"
            prop="fields.refreshDate"
            :label="$lang.columns.refreshDate"
            width="200"
          >
          </el-table-column>

          <el-table-column align="center" :label="$lang.columns.operations">
            <template slot-scope="props">
              <el-button
                type="danger"
                size="mini"
                @click="onSingleDelete(props.row.pk)"
              >
                <i class="fa fa-remove"></i>
                {{ $lang.buttons.delete }}
              </el-button>
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
import PanelTitle from "../../components/PanelTitle";

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
        // "-1": this.$store.getters.$lang.buttons.error,
        "-1": "异常",
      },
      pagination: {
          currentPage: 1,
          pageSize: 20,
          total: 0
      }
    };
  },
  components: {
    PanelTitle,
  },
  created() {
    this.onGetMonitorData();
  },
  methods: {
    generateUrl(url) {
      // 检查URL是否以 'http://' 或 'https://' 开头
      if (!/^https?:\/\//.test(url)) {
        // 如果没有，则添加 'https://' 前缀
        url = 'https://' + url;
      }
      return url;
    },
    handleChangeType(type) {
        this.tyif = type;
        this.onGetMonitorData();
    },
    onRefresh() {
      this.onGetMonitorData();
    },
    onGetmonitorStatus() {
      this.tymonitors.forEach((monitor) => {
        this.onGetMonitorStatus(monitor);
      });
    },
    onGetMonitorStatus(monitor) {
      let id = monitor.pk;
      // eslint-disable-next-line  
      console.log("monitor", monitor)
      const { qr, jr, zr } = monitor.fields;
      const result = qr == '0' & jr == '0' & zr == '0' ? "-1" : "1";
      // eslint-disable-next-line  
      console.log("monitor22", result, qr, jr, zr)
      this.$set(this.monitorStatus, id, result);
      
    },
    onGetMonitorData() {
      let params = {
        page: this.pagination.currentPage,
        tyif: this.tyif,
        pageSize: this.pagination.pageSize,
        searchQuery:this.searchQuery
      };
      // eslint-disable-next-line  
      this.loading = true;
      this.$http
        .get(this.$store.state.url.tymonitor.index,{params})
        .then(({ data: tymonitors }) => {
          // eslint-disable-next-line  
          this.tymonitors = tymonitors.data;
          this.loading = false;
          this.onGetmonitorStatus();
          this.pagination.total = tymonitors.total;

        })
        .catch(() => {
          this.loading = false;
        });
    },

    onDeleteMonitor(id) {
      this.$http
        .post(
          this.formatString(this.$store.state.url.tymonitor.remove, {
            id: id,
          })
        )
        .then(() => {
          this.$message.success(
            this.$store.getters.$lang.messages.successDelete
          );
          this.loading = false;
          this.onGetMonitorData();
        })
        .catch(() => {
          this.$message.error(this.$store.getters.$lang.messages.errorDelete);
          this.loading = false;
        });
    },
    onSingleDelete(id) {
      this.$confirm(
        this.$store.getters.$lang.messages.confirm,
        this.$store.getters.$lang.buttons.confirm,
        {
          confirmButtonText: this.$store.getters.$lang.buttons.yes,
          cancelButtonText: this.$store.getters.$lang.buttons.no,
          type: "warning",
        }
      ).then(() => {
        this.onDeleteMonitor(id);
      });
    },
  },
  
};
</script>
