<template>
  <div class="panel">
    <panel-title title="关键词添加"></panel-title>
    <div
      class="panel-body"
      v-loading="loadData"
      :element-loading-text="$lang.messages.loading"
    >
      <el-row>
        <el-col :span="8">
          <el-form ref="form" :model="form" :rules="rules" label-width="100px">
            <!-- 添加人 -->
            <el-form-item label="负责人" prop="keyword_owner">
              <el-input
                v-model="form.keyword_owner"
                placeholder="请添加关键词关注人"
                size="small"
              ></el-input>
            </el-form-item>
            
            <!-- 关键词 -->
            <el-form-item label="关键词" prop="keyword">
              <el-input
                v-model="form.keyword"
                placeholder="请添加关键词"
                size="small"
              ></el-input>
            </el-form-item>
            
            <!-- 优先级 -->
            <el-form-item label="优先级" prop="priority">
              <el-input
                v-model="form.priority"
                placeholder="优先级"
                size="small"
              ></el-input>
            </el-form-item>

            <el-form-item>
              <el-button
                type="primary"
                size="small"
                @click="onSubmitForm"
                :loading="onSubmitLoading"
              >
                <i class="fa fa-check"></i>
                {{ $lang.buttons.create }}
              </el-button>
              <el-button @click="$router.back()" size="small">
                <i class="fa fa-reply"></i>
                {{ $lang.buttons.return }}
              </el-button>
            </el-form-item>
          </el-form>
        </el-col>
      </el-row>
    </div>
  </div>
</template>
<script>
import PanelTitle from "../../components/PanelTitle";
// import { ip, port } from "../../utils/regex";

export default {
  data() {
    return {
      form: {
        keyword_owner: "",
        keyword: "",
        priority: "",
      },
      loadData: false,
      onSubmitLoading: false,
      rules: {
        keyword_owner: [
          {
            required: true,
            message:'请输入关键词关注人',
            trigger: "blur",
          },
        ],
      
        keyword: [
          {
            required: true,
            message:'请输入关键词',
            trigger: "blur",
          },
        ],
        priority: [
          {
            required: true,
            message:'优先级',
            trigger: "blur",
          },
        ],
      },
    };
  },
  methods: {
    onSubmitForm() {
      this.$refs.form.validate((valid) => {
        if (!valid) return false;
        this.onSubmitLoading = true;
        this.$http
          .post(this.$store.state.url.xyresult.xycreate, this.form)
          .then(() => {
            this.$message.success(
              this.$store.getters.$lang.messages.successSave
            );
            this.onSubmitLoading = false;
            this.$router.push({
              name: "xyresultIndex",
            });
          })
          .catch(() => {
            this.$message.error('请勿重复添加关键词');
            this.onSubmitLoading = false;
          });
      });
    },
  },
  components: {
    PanelTitle,
  },
};
</script>
