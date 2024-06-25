<template>
  <div class="panel">
    <div class="search-wrap">
      <div class="left">
      </div>
    </div>
         <!-- 弹出修改框 -->
          <el-dialog :visible.sync="editVisible" title="编辑">
            <el-form :model="editForm">
              <el-form-item label="寻源结果">
                <el-input v-model="editForm.cpOrg" :style="{ width: '500px' }"></el-input>
              </el-form-item>
              <el-form-item label="网址录入">
                <el-input v-model="editForm.cpLink" :style="{ width: '500px' }"></el-input>
              </el-form-item>
              <el-form-item label="是否新源">
                <el-select v-model="editForm.isNewOrg">
                  <el-option :value="1">是</el-option>
                  <el-option :value="0">否</el-option>
                </el-select>
              </el-form-item>
            </el-form>
            <div slot="footer">
              <el-button @click="editVisible = false">取 消</el-button>
              <el-button type="primary" @click="submitEdit">确 定</el-button>
            </div>
        </el-dialog>

    <panel-title title="关键词寻源">

      <el-input v-model="searchQuery" placeholder="请输入来源名称" :style="{ width: '200px' }" size="small"
        class="space-between"></el-input>

      <el-switch class="space-between" v-model="onlySourceFlag" active-text="非新源" @change="onGetXyresultData">
      </el-switch>

      <el-button @click="onRefresh" size="mini">
        <i class="fa fa-refresh"></i>
        {{ '刷新/查询' }}
      </el-button>
      <router-link :to="{ name: 'xyresultCreate' }" tag="span">
        <el-button type="success" size="mini">
          <i class="fa fa-plus"></i>
          添加关键词
        </el-button>
      </router-link>

    </panel-title>
    <div class="panel-body">
      <el-table :empty-text="$lang.messages.noData" :data="xyresults" v-loading="loading" 
        :element-loading-text="$lang.messages.loading" border>
        <el-table-column align="center" prop="pk" label="id" width="60">
        </el-table-column>

        <el-table-column align="center" prop="fields.cp_org" label="寻源结果" width="300">
          <template slot-scope="scope">
            <span v-if="!scope.row.fields.cp_org || scope.row.fields.cp_org.length === 0">
              寻源失败
            </span>
            <template v-else>
              {{ scope.row.fields.cp_org }}
            </template>
          </template>
        </el-table-column>

        <!-- 是否新源列 -->
        <el-table-column align="center" prop="fields.is_new_org" label="是否新源" width="200">
          <template slot-scope="scope">
            <span v-if="scope.row.fields.is_new_org === 1">是</span>
            <span v-else>否</span>
          </template>
        </el-table-column>

        <el-table-column align="center" prop="fields.count" label="统计数" width="200">
        </el-table-column>

        <el-table-column align="center" :label="$lang.columns.operations">
          <template slot-scope="props">
            <router-link :to="{ name: 'xyDetail', params: { cp_org: props.row.fields.cp_org } }" tag="span">
              <el-button type="success" size="mini">
                <i class="fa fa-sitemap"></i>
                {{ "查看详情" }}
              </el-button>
            </router-link>
            <el-button size="mini" @click="editData(props.row)">
              <i class="fa fa-edit"></i>
              {{ "编辑" }}
            </el-button>
          </template>

        </el-table-column>

      </el-table>
      <el-pagination v-model="pagination.currentPage" :total="pagination.total"
        :current-page.sync="pagination.currentPage" @page-change="onGetXyresultData" :page-size="pagination.pageSize">
      </el-pagination>
    </div>

  </div>
</template>



<script>
import PanelTitle from "../../components/PanelTitle";

export default {
  created() {
    // this.onGetXynavData();
    this.onGetXyresultData();
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
      valueWho: '',
      valueKeyword: '',
      xynavdataKeys: [],
      xynavdataValues: [],
      pagination: {
        currentPage: 1,
        pageSize: 20,
        total: 0
      },
      editVisible: false,
      editForm: {}
    };
  },
  components: {
    PanelTitle,
  },

  methods: {
    editData(row) {
        this.editForm = {
          edType: 1,
          cpOrg: row.fields.cp_org,
          isNewOrg: row.fields.is_new_org,
          cpLink:'例如：https://xxx.com/chat/',
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
        onlySourceFlag: this.onlySourceFlag
      };
      // eslint-disable-next-line  
      console.log("params", params);
      // this.loading = false;
      this.loading = true;
      this.$http.get(this.$store.state.url.xyresult.xyresult, { params })
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