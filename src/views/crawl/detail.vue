<template>
    <div class="panel-body" v-html="detail.title">
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
      title:'demooo',
      detail:'demooo',
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
      let params =this.$route.query
      this.loading = true;
      // debugger;
      this.$http
          .post(this.$store.state.url.crawl.detail,{params})
          .then(({ data: tymonitors }) => {
            this.tymonitors = tymonitors.data;
            this.detail = tymonitors.data;
            this.loading = false;
          })
          .catch(() => {
            this.loading = false;
          });
    },
  },

};
</script>