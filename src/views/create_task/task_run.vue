<template>
  <!-- 任务启停控制 -->
  <div class="task-control">
    <h2>任务启停</h2>
    任务名称： 测试验证码
    任务描述： 填写任务描述
    用户本地浏览器数据目录（如果需要使用本地的登录信息，插件和cookie，请设置此目录，并点击下方“执行（带用户信息模式）”按钮开始执行任务）：
    ./user_data
    点击以下按钮执行任务，任务执行过程中可以长按暂停键（默认：p键）暂停任务的执行以便人工干预，如手动输入密码，验证码等。
    执行任务的过程中也可以随时使用XPath Helper扩展来调试XPath。
    如果想进行更复杂的操作，如设置无头模式，设置定时执行等，请使用下方的命令行执行任务选项并配置好命令行参数。
    执行ID（执行文件存放在execution_instances文件夹内，提前在下方写好执行ID且文件名不为current_time时可以追加文件内容以实现增量采集）：
    如果已在此处写/生成了ID号，则点击执行或获得ID按钮后，任务ID将保持不变且原任务文件将会被新配置覆盖
    提示：点击下方“获得任务执行ID”按钮得到任务ID，点击后面的“使用命令行执行任务”按钮获得如何使用命令行运行任务的提示命令。
  </div>
</template>
<script>
// function toggleTask() {
//   const taskStatus = document.getElementById('taskStatus').value;
//   alert(`任务状态已更改为: ${taskStatus}`);
//   // 实际应用中应发送请求到后端接口处理任务状态变更
// }

// function setSchedule() {
//   const cronExpression = document.getElementById('cronExpression').value;
//   if (cronExpression) {
//     alert(`定时任务已设置，Cron表达式为: ${cronExpression}`);
//     // 实际应用中应将Cron表达式发送到后端进行定时任务的配置
//   } else {
//     alert("请先输入Cron表达式");
//   }
// }

</script>
<style>
body {
  font-family: Arial, sans-serif;
  //max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}

.task-control, .schedule-task {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-top: 10px;
}

button {
  background-color: #4CAF50;
  color: white;
  padding: 10px 20px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  margin: 10px 2px;
  cursor: pointer;
}
.task-control {
  margin-left: -100px; /* 调整这个值以改变移动的距离 */
  /* 如果需要保持内容居中，可以添加以下代码 */
  display: flex;
  align-items: center;
  justify-content: center;
}

</style>