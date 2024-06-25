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
            <el-form-item :label="$lang.cteate_task.site_id" prop="title">
              {{form.site_id}}
            </el-form-item>
            <el-form-item  class="single-line"  :label="$lang.cteate_task.url" prop="title">
              {{form.url}}
            </el-form-item>

            <el-form-item class="single-line"  :label="$lang.cteate_task.title" prop="title">
              {{form.title}}
            </el-form-item>

            <el-form-item class="single-line"  :label="$lang.cteate_task.data" prop="title">
              {{form.data}}
            </el-form-item>

            <el-form-item class="single-line"  :label="$lang.cteate_task.pub_date" prop="title">
              {{form.pub_date}}
            </el-form-item>

            <el-form-item class="single-line"  :label="$lang.cteate_task.create_time" prop="title">
              {{form.create_time}}
            </el-form-item>

            <el-form-item :label="$lang.cteate_task.content">
              <div v-html="form.content"></div>
            </el-form-item>

          </el-form>
        </el-col>
      </el-row>
    </div>
  </div>
</template>
<style>
.single-line {
  white-space: nowrap;
}
</style>

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
              this.formatString(this.$store.state.url.cteate_task.detail, {
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
                this.formatString(this.$store.state.url.cteate_task.detail, {
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
