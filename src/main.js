import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import ElementUI from "element-ui";
import ECharts from "vue-echarts";
import "font-awesome/scss/font-awesome.scss";
import "./assets/scss/element.scss";
import "./assets/scss/main.scss";
import store from "./store";
import { mapGetters } from "vuex";
import VueAxios from "vue-axios";
import VueClipboard from "vue-clipboard2";
import http from "./http";

Vue.use(ElementUI);
Vue.use(VueClipboard);

Vue.component("v-chart", ECharts);

Vue.config.productionTip = false;

const globalConfig = {
  backendServerUrl: 'http://172.167.0.41:5005/pyspider/index',
  // cteateServerUrl: 'http://172.167.0.41:5173/src/assets/html/create_task.html?id=-1'
  cteateServerUrl: '/api/cteateTask?id=-1',
  openServerUrl: '/api/cteateTask?id='
}

Vue.use(VueAxios, http);

Vue.mixin({
  computed: {
    // register global language configuration
    ...mapGetters(["$lang"]),
  },
  methods: {
    // register global methods
    formatString: require("string-format-obj"),
    basename: require("path").basename,
    join: require("path").join,
  },
});

new Vue({
  data: {
    globalConfig
  },  
  router,
  store,
  render: (h) => h(App),
}).$mount("#app");
