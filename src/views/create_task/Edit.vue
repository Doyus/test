<template>
  <div class="panel">
    <panel-title :title="$lang.titles.editClient"></panel-title>
    <div
        class="panel-body"
        v-loading="loadData"
        :element-loading-text="$lang.messages.loading"
    >
      <el-row>
        <el-col :span="8">
          <el-form ref="form" :model="form" :rules="rules" label-width="100px">
            <el-form-item :label="$lang.columns.proxyPool" prop="is_proxy">
              <el-switch
                  v-model="form.is_proxy"
                  :active-value="1"
                  :inactive-value="0"
                  active-color="#13ce66"
                  inactive-color="#ff4949"
              ></el-switch>
            </el-form-item>

            <el-form-item :label="$lang.columns.crawl_interval" prop="crawl_interval">
              <el-input
                  v-model="form.crawl_interval"
                  :placeholder="$lang.messages.enter + $lang.columns.crawl_interval"
                  size="small"
              ></el-input>
            </el-form-item>

            <el-form-item :label="$lang.columns.website_name" prop="website_name">
              <el-input
                  v-model="form.website_name"
                  :placeholder="$lang.messages.enter + $lang.columns.website_name"
                  size="small"
              ></el-input>
            </el-form-item>

            <el-form-item :label="$lang.columns.class_name" prop="class_name">
              <el-input
                  v-model="form.class_name"
                  :placeholder="$lang.messages.enter + $lang.columns.class_name"
                  size="small"
              ></el-input>
            </el-form-item>

            <el-form-item :label="$lang.columns.crawl_dp" prop="crawl_dp">
              <el-select
                  v-model="form.crawl_dp"
                  :placeholder="$lang.messages.enter + $lang.columns.crawl_dp"
                  size="small"
              >
                <el-option
                    v-for="interval in crawlIntervals"
                    :key="interval.value"
                    :label="interval.label"
                    :value="interval.value"
                ></el-option>
              </el-select>
              <el-button
                  type="primary"
                  size="small"
                  @click="runForm"
              >
                <i class="fa fa-check"></i>
                本地测试运行
              </el-button>
            </el-form-item>


            <el-form-item>
              <el-button
                  type="primary"
                  size="small"
                  @click="onSubmitForm"
                  :loading="onSubmitLoading"
              >
                <i class="fa fa-check"></i>
                {{ $lang.buttons.update }}
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
export default {
  data() {
    return {
      form: {
        name: "",
        ip: "",
        port: "",
        description: "",
        auth: false,
        username: "",
        password: "",
        crawl_dp: '',
      },
      crawlIntervals: [
        { value: '1', label: '本地采集' },
        { value: '2', label: '云端采集' },
      ],
      routeId: this.$route.params.id,
      loadData: false,
      onSubmitLoading: false,
      rules: {
        name: [
          {
            required: true,
            message:
                this.$store.getters.$lang.columns.name +
                " " +
                this.$store.getters.$lang.messages.isNull,
            trigger: "blur",
          },
        ],
      },
    };
  },
  created() {
    this.routeId !== null && this.onGetFormData();
  },
  methods: {
    onGetFormData() {
      this.loadData = true;
      this.$http
          .get(
              this.formatString(this.$store.state.url.cteate_task.show, {
                id: this.routeId,
              })
          )
          .then(({ data: data }) => {
            this.form = data;
            this.form.auth = !!data.auth;
            this.loadData = false;
          })
          .catch(() => {
            this.loadData = false;
          });
    },
    onSubmitForm() {
      this.$refs.form.validate((valid) => {
        if (!valid) {
          return false;
        }
        this.onSubmitLoading = true;
        this.$http
            .post(
                this.formatString(this.$store.state.url.cteate_task.update, {
                  id: this.form.id,
                }),
                this.form
            )
            .then(() => {
              this.$message.success(
                  this.$store.getters.$lang.messages.successSave
              );
              this.onSubmitLoading = false;
            })
            .catch(() => {
              this.onSubmitLoading = false;
            });
      });
    },
    runForm() {
      this.$refs.form.validate((valid) => {
        if (!valid) {
          return false;
        }
        this.onSubmitLoading = true;
        this.$http
            .post(
                this.formatString('http://127.0.0.1:5556/spider_run/run_task', {
                  id: this.form.id,
                }),
                this.form
            )
            .then(() => {
              this.$message.success(
                  this.$store.getters.$lang.messages.successSave
              );
              this.onSubmitLoading = false;
            })
            .catch(() => {
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
