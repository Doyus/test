module.exports = {
  outputDir: "../SpiderSage/core/templates",
  assetsDir: "static",
  devServer: {
    disableHostCheck: true,
    host: "0.0.0.0",
    hot: true,
    port: '8001',
    proxy: {
      "/api/*": {
        // target: "http://localhost:8000",
        target: "http://127.0.0.1:6001",
        changeOrigin: true,
        secure: false,
      },
      "/static/src/*": {
        // target: "http://localhost:8000",
        target: "http://127.0.0.1:6001",
        changeOrigin: true,
        secure: false,
      },
      "/spider_run/*": {
        // target: "http://localhost:8000",
        target: "http://127.0.0.1:5556",
        changeOrigin: true,
        secure: false,
      },
    },

  },
  css: {
    sourceMap: true,
  },
};
