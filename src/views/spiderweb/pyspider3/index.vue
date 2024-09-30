<template>
  <div>
    <!-- 添加 iframe -->
    <iframe 
      src="http://39.106.238.69/pyspider/index" 
      width="100%" 
      height="1600px" 
      frameborder="0"
    ></iframe>

    <!-- 原有内容保持不变 -->
    <BasicTable @register="registerTable">
      <!-- ... 原有的表格内容 ... -->
    </BasicTable>
    <DemoDrawer @register="registerDrawer" @success="handleSuccess" />
  </div>
</template>