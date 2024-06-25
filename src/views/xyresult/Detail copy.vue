<template>
  <div class="panel">
    <div class="search-wrap">
      <div class="left">
        <!-- <el-button @click="handleChangeType('1')">关键词寻源</el-button> -->
        <!-- <el-button @click="handleChangeType('2')">普通寻源</el-button> -->
      </div>
    </div>


    <panel-title title="筛选条件">

      <el-input v-model="selectedCpOrg" placeholder="请输入来源名称" :style="{width: '200px'}" size="small" class="space-between"></el-input>
     
      <el-select v-model="valueWho" clearable placeholder="请选择负责人" size="small" class="space-between">
        <el-option v-for="item in xynavdataKeys" :key="item.keys" :label="item.keys" :value="item.keys">
        </el-option>
      </el-select>

      <el-select v-model="valueKeyword" clearable placeholder="请选择关键词" size="small" class="space-between">
        <el-option v-for="keyword in xynavdataValues" :key="keyword" :label="keyword" :value="keyword">
        </el-option>
      </el-select>

      <!-- <el-switch
        class="space-between"
        v-model="onlySourceFlag"
        active-text="只看有源">
      </el-switch> -->

        <!-- 开始时间选择 -->
      <el-date-picker
        v-model="startDate"
        type="date"
        placeholder="选择开始日期"
        value-format="yyyy-MM-dd"
        size="small"
        class="space-between"
        >
      </el-date-picker>

      <!-- 结束时间选择 -->
      <el-date-picker
        v-model="endDate"
        type="date"
        placeholder="选择结束日期"
        value-format="yyyy-MM-dd"
        size="small"
        class="space-between"
        >
      </el-date-picker>

      <el-button  class="space-between" @click="onGetXyresultData()" type="primary" size="small">搜索</el-button>

      <!-- <el-button  class="space-between" @click="onGetXyresultData()" type="primary" size="small">导出当前数据</el-button> -->
      <el-button type="primary" icon="el-icon-download" size="small" @click="exportExcel" v-model="exportFlag">导出</el-button>

    </panel-title>
    <div class="panel-body">
            <div v-if="xytype === '1'">
                <el-table 
                :empty-text="$lang.messages.noData" 
                :data="xyresults" v-loading="loading"
                :element-loading-text="$lang.messages.loading" 
                border>
                  <el-table-column align="center" prop="pk" label="id" width="60">
                  </el-table-column>

                  <el-table-column align="center" prop="fields.people" label="关键词添加人" width="120">
                  </el-table-column>

                  <el-table-column align="center" prop="fields.key_word" label="关键词" width="150">
                  </el-table-column>
                  
                  <el-table-column align="center" prop="fields.title" label="标题" width="260">
                    <template slot-scope="scope">
                      <a :href="scope.row.fields.first_url" target="_blank">
                        {{ scope.row.fields.title }}
                      </a>
                    </template>
                  </el-table-column>

                  <el-table-column align="center" prop="fields.source" label="对比网站" width="150">
                  </el-table-column>

                  <el-table-column align="center" prop="fields.pub_time" label="发布日期" width="200">
                  </el-table-column>

                  <el-table-column align="center" prop="fields.cp_org" label="寻源结果" width="200">
                    <template slot-scope="scope">
                      <span v-if="!scope.row.fields.cp_org || scope.row.fields.cp_org.length === 0">
                        寻源失败
                      </span>
                      <template v-else>
                        {{ scope.row.fields.cp_org }}
                      </template>
                    </template>
                  </el-table-column>

                  <el-table-column align="center" prop="fields.is_new_org" label="是否新源" width="200">
                  </el-table-column>

                  <el-table-column align="center" prop="fields.is_publish" label="是否发布" width="200">
                  </el-table-column>
                </el-table>
                <el-pagination v-model="pagination.currentPage" :total="pagination.total"
                  :current-page.sync="pagination.currentPage" @page-change="onGetXyresultData" :page-size="pagination.pageSize">
                </el-pagination>
          </div>
          <div v-else-if="xytype === '2'">
            <el-table :empty-text="$lang.messages.noData" :data="xyresults" v-loading="loading"
                  :element-loading-text="$lang.messages.loading" border>
                  <el-table-column align="center" prop="pk" label="id" width="60">
                  </el-table-column>
<!--                   
                  <el-table-column align="center" prop="fields.people" label="关键词添加人" width="120" v-if="false">
                  </el-table-column>

                  <el-table-column align="center" prop="fields.key_word" label="关键词" width="150" v-if="false">
                  </el-table-column>
                   -->
                  <el-table-column align="center" prop="fields.title" label="标题" width="260">
                    <template slot-scope="scope">
                      <a :href="scope.row.fields.first_url" target="_blank">
                      </a>
                    </template>
                  </el-table-column>

                  <el-table-column align="center" prop="fields.source" label="对比网站" width="150">
                  </el-table-column>

                  <el-table-column align="center" prop="fields.pub_time" label="发布日期" width="200">
                  </el-table-column>

                  <el-table-column align="center" prop="fields.cp_org" label="寻源结果" width="200">
                    <template slot-scope="scope">
                      <span v-if="!scope.row.fields.cp_org || scope.row.fields.cp_org.length === 0">
                        寻源失败
                      </span>
                      <template v-else>
                        {{ scope.row.fields.cp_org }}
                      </template>
                    </template>
                  </el-table-column>

                  <el-table-column align="center" prop="fields.is_new_org" label="是否新源" width="200">
                  </el-table-column>

                  <el-table-column align="center" prop="fields.is_publish" label="是否发布" width="200">
                  </el-table-column>
                </el-table>
                <el-pagination v-model="pagination.currentPage" :total="pagination.total"
                  :current-page.sync="pagination.currentPage" @page-change="onGetXyresultData" :page-size="pagination.pageSize">
                </el-pagination>
          </div>
    </div>
  </div>
</template>

<script>
import PanelTitle from "../../components/PanelTitle";
// import XLSX from 'xlsx'
// import FileSaver from 'file-saver'
// import * as XLSX from 'xlsx';
// import { transformDataForExcel } from '@/utils/excel';

export default {

  created() {
    this.selectedCpOrg = this.$route.params.cp_org;
    // eslint-disable-next-line  
    console.log('cp_org:', this.selectedCpOrg);
    this.onGetXynavData();
    // this.onGetXyresultData();
  },

  watch: {
    'pagination.currentPage': {
      handler() {
        // eslint-disable-next-line  
        this.onGetXyresultData();
      },
      deep: true
    },
    valueWho(newVal) {
      this.xynavdataValues = this.xynavdataKeys.find(item => item.keys === newVal).values 
    }
  },
  name: "xyresults",
  props: {},
  data() {
    return {
      searchQuery: null, //搜索关键词
      xytype: '1',//1 代表关键词,2 代表普通
      xyresults: null,
      loading: false,
      onlySourceFlag:false,
      selectedCpOrg:'',
      valueWho: '', 
      valueKeyword: '',
      xynavdataKeys: [],
      xynavdataValues:[],
      startDate: '',
      endDate: '',
      exportFlag:false,
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

  methods: {
    
    exportExcel() {
      let params = {
        page: this.pagination.currentPage,
        xytype: this.xytype,
        pageSize: this.pagination.pageSize,
        searchQuery: this.searchQuery,
        valueKeyword: this.valueKeyword,
        valueWho: this.valueWho,
        onlySourceFlag:this.onlySourceFlag,
        selectedCpOrg:this.selectedCpOrg,
        startDate: this.startDate,
        endDate: this.endDate,
        exportFlag:this.exportFlag
      };
      this.$http
        .get(this.$store.state.url.xyresult.xydetail, { params, timeout: 50000 })
        .then(({ data: result }) => {
          this.xyresults = result.data;
          const dataForExcel = transformDataForExcel(result);
          const workbook = XLSX.utils.book_new();
          const worksheet = XLSX.utils.aoa_to_sheet(dataForExcel);
          XLSX.utils.book_append_sheet(workbook, worksheet, 'Sheet1');
          const wbout = XLSX.write(workbook, { type: 'array', bookType: 'xlsx' });
          const blob = new Blob([wbout], { type: 'application/octet-stream' });
          FileSaver.saveAs(blob, 'data.xlsx');
          this.exportFlag = false;
        })
        .catch(() => {
          this.exportFlag = false;
        });
    },

    handleChangeType(type) {
      this.onGetXynavData();
      this.xytype = type;
      this.onGetXyresultData();
    },
    onRefresh() {
      this.onGetXyresultData();
    },
    onGetXynavData() {
      this.loading = true;
      this.$http
        .get(this.$store.state.url.xyresult.xynavdata)
        .then(({ data: result }) => {
          // eslint-disable-next-line  
          this.xynavdataKeys = result.data;
          // eslint-disable-next-line
          this.loading = false;
          this.pagination.total = result.total;
        })
        .catch(() => {
          this.loading = false;
        });
    },
    onGetXyresultData() {
      // eslint-disable-next-line  
      let params = {
        page: this.pagination.currentPage,
        xytype: this.xytype,
        pageSize: this.pagination.pageSize,
        searchQuery: this.searchQuery,
        valueKeyword: this.valueKeyword,
        valueWho: this.valueWho,
        onlySourceFlag:this.onlySourceFlag,
        selectedCpOrg:this.selectedCpOrg,
        startDate: this.startDate,
        endDate: this.endDate,
        exportFlag:this.exportFlag
      };
      // eslint-disable-next-line  
      console.log("params", params);
      // this.loading = false;
      this.loading = true;
      this.$http
        .get(this.$store.state.url.xyresult.xydetail,{params,timeout: 50000})
        .then(({ data: result }) => {
          // eslint-disable-next-line  
          this.xyresults = result.data;
          // eslint-disable-next-line
          this.loading = false;
          this.pagination.total = result.total;
        })
        .catch(() => {
          this.loading = false;
        });
    },

  },

};
</script>
<style>
.search-wrap {
  display: flex;
  justify-content: space-between;

}
.space-between {
  margin-right: 15px; 
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