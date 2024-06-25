<template>
  <div class="panel">
    <panel-title :title="$lang.titles.createTytask"></panel-title>
    <div
      class="panel-body"
      v-loading="loadData"
      :element-loading-text="$lang.messages.loading"
    >
      <el-row>
        <el-col :span="8">
          <el-form ref="form" :model="form" :rules="rules" label-width="100px">
            <!-- 网站名 -->
            <el-form-item :label="$lang.columns.sourceName" prop="sourceName">
              <el-input
                v-model="form.sourceName"
                :placeholder="$lang.messages.enter + ' ' + $lang.columns.sourceName"
                size="small"
              ></el-input>
            </el-form-item>
            <!-- 负责人 -->
            <el-form-item :label="$lang.columns.who" prop="who">
              <el-input
                v-model="form.who"
                :placeholder="$lang.messages.enter + ' ' + $lang.columns.who"
                size="small"
              ></el-input>
            </el-form-item>
            <!-- 网站地址 -->
            <el-form-item :label="$lang.columns.tyhost" prop="tyhost">
              <el-input
                v-model="form.tyhost"
                :placeholder="$lang.messages.enter + ' ' + $lang.columns.tyhost"
                size="small"
              ></el-input>
            </el-form-item>
            <!-- 是否特源 -->
            <!-- multiple 删除-->
            <el-form-item :label="$lang.columns.tyif" prop="tyif">
                  <el-select
                    v-model="form.tyif"
                    :placeholder="$lang.messages.select"
                    size="small"
                  >
                    <el-option
                      v-for="item in tymonitorOptions"
                      :key="item.value"
                      :label="item.label"
                      :value="item.value"
                    >
                    </el-option>
                  </el-select>
            </el-form-item>
            <!-- 说明 -->
            <el-form-item :label="$lang.columns.tyremark" prop="tyremark">
              <el-input
                v-model="form.tyremark"
                :placeholder="$lang.messages.enter + ' ' + $lang.columns.tyremark"
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
      tymonitorOptions: [{ value: "1", label: "特源" }, { value: "2", label: "非特源" }],
      form: {
        sourceName: "",
        who: "",
        tyremark: "",
        tyhost:"",
        tyif: "",
        priority: 1,
        // tyif:[]
      },
      loadData: false,
      onSubmitLoading: false,
      rules: {
        sourceName: [
          {
            required: true,
            message:
              this.$store.getters.$lang.columns.sourceName +
              " " +
              this.$store.getters.$lang.messages.isNull,
            trigger: "blur",
          },
        ],
        tyhost: [
          {
            required: true,
            message:
              this.$store.getters.$lang.columns.tyhost +
              " " +
              this.$store.getters.$lang.messages.isNull,
            trigger: "blur",
          },
        ],
        tyif: [
          {
            required: true,
            message:
              this.$store.getters.$lang.columns.tyif +
              " " +
              this.$store.getters.$lang.messages.isNull,
            trigger: "blur",
          },
        ],
        who: [
          {
            required: true,
            message:
              this.$store.getters.$lang.columns.who +
              " " +
              this.$store.getters.$lang.messages.isNull,
            trigger: "blur",
          },
        ],
        tyremark: [
          {
            required: false,
            message:
              this.$store.getters.$lang.columns.tyremark +
              " " +
              this.$store.getters.$lang.messages.isNull,
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
          .post(this.$store.state.url.tymonitor.create, this.form)
          .then(() => {
            this.$message.success(
              this.$store.getters.$lang.messages.successSave
            );
            this.onSubmitLoading = false;
            this.$message.success('任务添加成功');
            // this.$router.push({
            //   name: "tymonitorIndex",
            // });
          })
          .catch(() => {
            this.$message.error('域名重复，请重写检查');
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
