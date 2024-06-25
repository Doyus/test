<template>
  <div class="panel">
    <div class="search-wrap">
      <div class="left">
        <!-- <el-button @click="handleChangeType('1')">关键词寻源</el-button> -->
        <!-- <el-button @click="handleChangeType('2')">普通寻源</el-button> -->
      </div>
    </div>

    <el-dialog :visible.sync="editVisible" title="编辑">
      <el-form :model="editForm">
        <el-form-item label="是否标记为已经处理">
          <el-select v-model="editForm.handleFlag">
            <el-option :value="1">是</el-option>
            <el-option :value="0">否</el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="处理说明">
          <el-input v-model="editForm.handleDesc" :style="{ width: '500px' }"></el-input>
        </el-form-item>
        
      </el-form>
      <div slot="footer">
        <el-button @click="editVisible = false">取 消</el-button>
        <el-button type="primary" @click="submitEdit">确 定</el-button>
      </div>
    </el-dialog>


    <panel-title title="筛选条件">

      <el-input v-model="selectedCpOrg" placeholder="请输入来源名称" :style="{ width: '200px' }" size="small"
        class="space-between"></el-input>

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
      <el-date-picker v-model="startDate" type="date" placeholder="选择开始日期" value-format="yyyy-MM-dd" size="small"
        class="space-between">
      </el-date-picker>

      <!-- 结束时间选择 -->
      <el-date-picker v-model="endDate" type="date" placeholder="选择结束日期" value-format="yyyy-MM-dd" size="small"
        class="space-between">
      </el-date-picker>

      <el-button class="space-between" @click="onGetXyresultData()" size="small">搜索</el-button>

      <!-- <el-button  class="space-between" @click="onGetXyresultData()" type="primary" size="small">导出当前数据</el-button> -->
      <el-button icon="el-icon-download" size="small" @click="exportExcel">导出</el-button>
      <el-button @click="goBack" size="small">
        <i class="fa fa-reply"></i>
        {{ $lang.buttons.return }}
      </el-button>

    </panel-title>
    <div class="panel-body">
      <el-table :empty-text="$lang.messages.noData" :data="xyresults" v-loading="loading"
        :element-loading-text="$lang.messages.loading" border>
        <el-table-column align="center" prop="pk" label="id" width="60">
        </el-table-column>

        <el-table-column align="center" prop="fields.keyword_owner" label="关键词添加人" width="120">
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
          <template slot-scope="scope">
            {{ scope.row.fields.pub_time.replace("T", " ").replace("Z", "") }}
          </template>
        </el-table-column>

        <el-table-column align="center" prop="fields.update_time" label="更新日期" width="200">
          <template slot-scope="scope">
            {{ scope.row.fields.update_time.replace("T", " ").replace("Z", "") }}
          </template>
        </el-table-column>

        <el-table-column align="center" :label="$lang.columns.operations">
          <template slot-scope="props">
            <el-button size="mini" @click="editData(props.row)">
              <i class="fa fa-edit"></i>
              {{ "编辑" }}
            </el-button>
          </template>
        </el-table-column>

        <!-- 
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
                  <template slot-scope="scope">
                    <span v-if="scope.row.fields.is_new_org === 1">是</span>
                    <span v-else>否</span>
                  </template>
                </el-table-column>

                <el-table-column align="center" prop="fields.is_publish" label="是否发布" width="200">
                  <template slot-scope="scope">
                    <span v-if="scope.row.fields.is_publish === 1">是</span>
                    <span v-else>否</span>
                  </template>
                </el-table-column> 
                 -->
      </el-table>
      <el-pagination v-model="pagination.currentPage" :total="pagination.total"
        :current-page.sync="pagination.currentPage" @page-change="onGetXyresultData" :page-size="pagination.pageSize">
      </el-pagination>
    </div>
  </div>
</template>

<script>
import PanelTitle from "../../components/PanelTitle";
// import XLSX from 'xlsx'
import FileSaver from 'file-saver'
import * as XLSX from 'xlsx';
import { transformDataForExcel } from '@/utils/excel';

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
      onlySourceFlag: false,
      selectedCpOrg: '',
      valueWho: '',
      valueKeyword: '',
      xynavdataKeys: [],
      xynavdataValues: [],
      startDate: '',
      endDate: '',
      editVisible: false,
      editForm: {},
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
    editData(row) {
      this.editForm = {
        edType: 3,
        firstUrl: row.fields.first_url,
        handleFlag: "",
        handleDesc: "",
      };
      this.editVisible = true; // 将此行添加到 editData 函数中
    },
    submitEdit() {
      let params = this.editForm
      // 提交修改的代码
      this.editVisible = false;
      // alert("收集到的参数：" + JSON.stringify(this.editForm));
      // this.loading = false;
      this.loading = true;
      this.$http.get(this.$store.state.url.xyresult.xyedit, { params })
        .then(({ data: result }) => {
          // eslint-disable-next-line  
          this.xyresults = result.data;
          // eslint-disable-next-line
          this.loading = false;
          this.pagination.total = result.total;
        })
        .catch(() => {
          this.loading = false;
          this.$message.error("提交失败，请检查提交参数是否正确，或者此网站中文名称已经收录，联系管理员确认");
        });
    },
    exportExcel() {
      let params = {
        page: this.pagination.currentPage,
        xytype: this.xytype,
        pageSize: this.pagination.pageSize,
        searchQuery: this.searchQuery,
        valueKeyword: this.valueKeyword,
        valueWho: this.valueWho,
        onlySourceFlag: this.onlySourceFlag,
        selectedCpOrg: this.selectedCpOrg,
        startDate: this.startDate,
        endDate: this.endDate,
        exportFlag: true,
      };
      this.$http
        .get(this.$store.state.url.xyresult.xydetail, { params, timeout: 50000 })
        .then(({ data: result }) => {
          this.xyresults = result.data;
          const dataForExcel = transformDataForExcel(result);
          // eslint-disable-next-line  
          // console.log("dataForExcel", dataForExcel)
          const columns = [
            '标题', // 标题
            '发布日期', // 发布时间
            '区域', // 地区或来源地
            '来源', // 数据来源
            '详情链接', // 首次出现的详情页面URL
            '比对来源', // 比对数据的来源名称
            '是否在CMS中存在', // 是否存在于内容管理系统：is_cp
            '对比后标题', // 对比检索后得到的文章标题
            '对比后组织机构', // 对比检索后得到的来源组织名称
            '对比后组织URL', // 对比检索后得到的来源URL
            '关键词', // 关键词
            '是否为新源头', // 是否为新的信息源头：is_new_org
            '负责人', // 负责人信息
            '是否已发布' // 是否已发布的状态：is_publish
          ];
          dataForExcel.unshift(columns);
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
        onlySourceFlag: this.onlySourceFlag,
        selectedCpOrg: this.selectedCpOrg,
        startDate: this.startDate,
        endDate: this.endDate,
      };
      // eslint-disable-next-line  
      console.log("params", params);
      // this.loading = false;
      this.loading = true;
      this.$http
        .get(this.$store.state.url.xyresult.xydetail, { params, timeout: 100000 })
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