<template>
  <div>
    <div id="tip" class="alert alert-success alert-dismissible fade show" style="position: fixed; width:100%;display: none;">
      <button type="button" class="close" data-dismiss="alert">&times;</button>
      <span id="tip_message">提示：保存成功！</span>
    </div>
    <div id="tipInfo" class="alert alert-info alert-dismissible fade show" style="position: fixed; width:100%;display: none;">
      <button type="button" class="close" data-dismiss="alert">&times;</button>
      <span id="info_message">提示：您加载的任务版本不是最新版，可能出现兼容性问题。</span>
    </div>
    <div id="tipError" class="alert alert-danger alert-dismissible fade show" style="position: fixed; width:100%;display: none;">
      <button type="button" class="close" data-dismiss="alert">&times;</button>
      <span id="error_message">提示：保存名不符合MySQL表名规范，请重试！</span>
    </div>
    <div style="display:flex">
      <div style="width: 200px;float:left;overflow: auto">
        <div class="toolbox" style="text-align:center;margin: 20px;border-radius:10px;border:navy solid;background-color:rgb(242,243,245);z-index: 9999;">
          <div style="padding: 10px;border-radius:10px;font-size: 20px;">工具箱</div>
          <button type="button" id="save" data-toggle="modal" data-target="#myModal" @mousedown="showModal" class="btn btn-primary">保存任务</button>
          <button type="button" data=1 draggable="true" class="btn btn-outline-primary options">打开网页</button>
          <button type="button" data=8 draggable="true" class="btn btn-outline-primary options" style="font-weight: bold">循环</button>
          <button type="button" data=2 draggable="true" class="btn btn-outline-primary options">点击元素</button>
          <button type="button" data=3 draggable="true" class="btn btn-outline-primary options">提取数据</button>
          <button type="button" data=15 draggable="true" class="btn btn-outline-primary options" style="font-weight: bold">保存数据</button>
          <button type="button" data=14 draggable="true" class="btn btn-outline-primary options" style="font-weight: bold">返回</button>
          <div>*----以下为测试功能----*</div>
          <button type="button" data=5 draggable="true" class="btn btn-outline-primary options" style="font-weight: bold">自定义操作</button>
          <button type="button" data=4 draggable="true" class="btn btn-outline-primary options">输入文字</button>
          <button type="button" data=6 draggable="true" class="btn btn-outline-primary options">验证码</button>
          <div style="text-align: left;margin: 10px;font-size:15px!important">提示：拖动上方按钮到流程图箭头处以添加操作</div>
        </div>
      </div>
      <div style="margin-top:20px;height:750px;border: solid;overflow: auto;width:28%;float:right" id="flowchart_graph">
        <div id="0" class="clk" data="0"></div>
        <div style="border-radius: 100%;width: 40px;height: 40px;border:solid black;margin: 5px auto;background-color:lightcyan">
          <p style="font-size: 22px!important;text-align: center;margin-left: 1px;">■</p>
        </div>
      </div>
      <div style="margin-top:20px;border: solid navy;height:750px;overflow: auto;margin-left:10px;margin-right:10px;width:30%;float:right;min-width:300px">
        <div class="Modify" id="app">
          <div class="modal fade" id="myModal_XPath" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
            <div class="modal-dialog">
              <div class="modal-content">
                <div class="modal-header">
                  <h4 class="modal-title">等价XPath</h4>
                  <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
                </div>
                <div class="modal-body">
                  <label>以下提供除默认生成的XPath外其余等价的XPath，都能定位到同一个元素（但不完全准确，可能可以定位到除该元素外的其他元素，因此只是提供在这里作为参考）。</label>
                  <label>每行一个XPath（可使用预装的XPath Helper扩展调试）：</label>
                  <textarea spellcheck=false id="otherXPaths" @keydown="inputDelete" class="form-control" rows="4">{{XPaths}}</textarea>
                  <!-- <div><img src="../img/XPather_helper.png" style="width:50%;height:50%; margin: 10px auto"></div> -->
                </div>
              </div>
            </div>
          </div>
          <div>
            <label>提示：在流程图中<b>双击</b>操作可<b>试运行</b></label>
            <label>选项名称：</label>
            <input spellcheck=false @keydown="inputDelete" class="form-control" v-model='list.nl[index.nowNodeIndex]["title"]'></input>
          </div>
          <div class="elements" v-if="nodeType==1">
            <label>URL：</label>
            <input spellcheck=false @keydown="inputDelete" class="form-control" v-model.number="nowNode['parameters']['url']" type="text" required></input>
            <label>页面加载最长等待时间（秒）：</label>
            <input spellcheck=false @keydown="inputDelete" class="form-control" v-model.number="nowNode['parameters']['maxWaitTime']" type="number" required></input>
            <label>是否添加全局代理，涉及封禁Ip使用</label>
            <select v-model='nowNode["parameters"]["proxy"]' class="form-control">
              <option :value=0>否</option>
              <option :value=1>是</option>
            </select>
            <p style="margin-top: 10px">
              <a class="btn btn-primary" data-toggle="collapse" href="#collapseOpenPage" role="button" aria-expanded="false" aria-controls="collapseExample">点此展开/折叠自定义操作</a>
            </p>
            <div :class="{collapse: true, 'show': nowNode['parameters']['cookies'].length!=0}" id="collapseOpenPage">
              <div>
                <label>设置用户目录：维持cookie使用</label>
                <input spellcheck=false @keydown="inputDelete" class="form-control" v-model.number="nowNode['parameters']['user']" type="text" required></input>
                <label>设置指定端口：</label>
                <input spellcheck=false @keydown="inputDelete" class="form-control" v-model.number="nowNode['parameters']['port']" type="number" required></input>
              </div>
            </div>
          </div>
          <!-- 其他类型的操作选项省略，类似于上面的结构 -->
        </div>
      </div>
      <div style="margin-top:20px;border: solid navy;height:750px;overflow: auto;margin-left:10px;margin-right:10px;width:40%;float:right;min-width:300px">
        <textarea id="logDisplay" readonly>双击运行没有日志产生，请查看终端日志，或者请先保存当前配置，然后刷新当前页面</textarea>
        <div id="logDisplayHtml">只展示一条记录，并展示渲染效果</div>
      </div>
    </div>
    <div class="modal fade" id="myModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
      <div class="modal-dialog modal-xl">
        <div class="modal-content">
          <div class="modal-header">
            <h4 class="modal-title" id="myModalLabel">保存任务（可按Ctrl+S调出此窗口）</h4>
            <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
          </div>
          <div class="modal-body" style="height:60vh;overflow: auto">
            <input spellcheck=false @keydown="inputDelete" id="serviceId" type="hidden" name="serviceId" value="-1"></input>
            <label>采集负责人：</label>
            <input spellcheck=false @keydown="inputDelete" type="text" value="填写采集负责人" id="principal" class="form-control"></input>
            <label>首页地址：</label>
            <input spellcheck=false @keydown="inputDelete" type="text" value="填写网站首页地址" id="url" class="form-control"></input>
            <label>网站名称：</label>
            <input spellcheck=false @keydown="inputDelete" required name="serviceName" value="采集网站名称" id="serviceName" class="form-control"></input>
            <label>栏目名称：</label>
            <input spellcheck=false @keydown="inputDelete" required name="className" value="填写采集栏目名称" id="className" class="form-control"></input>
            <label>任务描述：</label>
            <input spellcheck=false @keydown="inputDelete" id="serviceDescription" name="serviceDescription" class="form-control" value="填写任务描述"></input>
            <label for="crawlType">采集类型：</label>
            <select id="crawlType" name="crawlType" class="form-control" @change="inputDelete">
              <option value="1">浏览器爬虫</option>
              <option value="2">协议爬虫</option>
            </select>
            <label>选择去重字段(shit+鼠标单击):</label>
            <select multiple class="form-control" name="selectedFields">
              <option value="title">标题</option>
              <option value="content">内容</option>
              <option value='comments'>详情地址</option>
              <option value='publish_date'>发布时间</option>
            </select>
            <label>其他自定义配置：</label>
            <textarea id="customConfig" class="form-control" placeholder="请输入JSON格式数据" rows="5" cols="30"></textarea>
            <button @click="validateJson">验证JSON格式</button>
          </div>
          <div class="modal-footer">
            <button type="button" id="saveButton" style="width: 100px" class="btn btn-primary">保存任务</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "DesignFlow",
  data() {
    return {
      // 初始化数据
    };
  },
  methods: {
    showModal() {
      $('#myModal').modal('show');
    },
    validateJson() {
      const inputField = document.getElementById('customConfig');
      let inputValue = inputField.value.trim();
      try {
        const jsonObj = JSON.parse(inputValue);
        const formattedJson = JSON.stringify(jsonObj, null, 2);
        inputField.value = formattedJson;
        alert("JSON格式正确");
      } catch (error) {
        alert("JSON格式错误: " + error.message);
      }
    },
    inputDelete(event) {
      // 处理输入删除事件
    }
  },
  mounted() {
    document.getElementById('customConfig').value = JSON.stringify({
      "noTrace": {
        "name": "是否开启无痕模式",
        "value": "false"
      },
      "crawlTimeLimit": {
        "name": "抓取时间时段限制",
        "value": "00:00:00-23:59:59"
      },
      "crawlInterval": {
        "name": "抓取时间频率(秒)",
        "value": "1000"
      },
    }, null, 4);
  }
};
</script>

<style scoped>
/* 添加必要的样式 */
textarea {
  width: 100%;
  height: 400px;
  resize: vertical;
  font-family: monospace;
  overflow-y: scroll;
  white-space: pre-wrap;
}
</style>