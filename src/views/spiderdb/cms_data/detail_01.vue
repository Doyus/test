<template>
    <PageWrapper contentBackground>
      <template #default>
        <div class="page-content">
          <div class="custom-title-container">
            <h1 class="custom-centered-title">{{ content.title }}</h1>
          </div>
          <Card :bordered="false">
            <div class="content-detail">
              <div class="meta" style="max-width: 70%; margin: 0 auto;">
                <a-descriptions :column="4" :colon="false" style="display: flex; justify-content: space-between;">
                    <a-descriptions-item label="发布日期">发布日期：{{ formatDate(content.publish_date) }}</a-descriptions-item>
                    <a-descriptions-item label="地区">地区：{{ content.area }}</a-descriptions-item>
                    <a-descriptions-item label="类别">行业：{{ content.category }}</a-descriptions-item>
                    <a-descriptions-item label="来源">来源：{{ content.source }}</a-descriptions-item>
                  </a-descriptions>
              </div>
              <Divider />
              <div class="body" v-html="content.description"></div>
            </div>
          </Card>
        </div>
        
        <div class="footer-info">
          <p>采购ID: {{ content.aus_id }}</p>
          <p>原始链接: <a :href="content.comments" target="_blank">查看原文</a></p>
        </div>
      </template>
    </PageWrapper>
  </template>
  
  <script lang="ts" setup>
  import { ref, onMounted  } from 'vue';
  import { PageWrapper } from '/@/components/Page';
  import { Card, Descriptions, Divider } from 'ant-design-vue';
  import { useRoute } from 'vue-router';
  import { getItemById } from './api';
  
  
  
  const route = useRoute();
  
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return `${date.getFullYear()}年${date.getMonth() + 1}月${date.getDate()}日`;
  };
  // const saa = {
  // 	'aus_id': 2716206,
  // 	'title': '广西融安鱼峰水泥有限公司2024-2025年计量仪表外协检定项目成交结果公告',
  // 	'comments': 'https://gxygcg.ejy365.com/#/purchase/detail/2/ZBCG/64359',
  // 	'main_host': 'gxygcg.ejy365.com',
  // 	'ok_status': 'Y',
  // 	'classd_name': '广西阳光采购服务平台-结果公示(pyspider)',
  // 	'publish_date': "2020-01-01",
  // 	'table_name2': 'ZBGS',
  // 	'classd_id': '二手',
  // 	'table_name': 'ZBXX',
  // 	'original_id': 150847748752960,
  // 	'area': '广西壮族自治区',
  // 	'area_id': 21,
  // 	'category': '其它',
  // 	'category_id': '15',
  // 	'files': '[]',
  // 	'sync_status': 1,
  // 	'crawl_status': 1,
  // 	'program_source': 'pyspider',
  // 	'client_name': 'spider002',
  // 	'client_ip': '192.168.93.192',
  // 	'cms_id': '1091000416064291',
  // 	'responsible_person': 'SUPER',
  // 	'source': '5',
  // 	'description': '<p style="text-align:center;line-height:39px"><strong><span style="font-family: 宋体;letter-spacing: 0;font-size: 19px">广西融安鱼峰水泥有限公司</span></strong><strong><span style="font-family: 宋体;letter-spacing: 0;font-size: 19px">2024-2025年计量仪表外协检定项目</span></strong><strong><span style="font-family: 宋体;letter-spacing: 0;font-size: 19px">成交结果公告</span></strong></p><p style="margin: 0 0 10px;text-indent: 32px"><span style="font-family: 宋体;color: rgb(51, 51, 51);letter-spacing: 0;font-size: 19px">&nbsp;</span></p><p style="text-indent: 32px"><span style=";font-family:宋体;font-size:19px">2024-2025年计量仪表外协检定项目（项目编号：RAYF-2024-88），</span><span style="font-family: 宋体;color: rgb(51, 51, 51);letter-spacing: 0;font-size: 19px">采购</span><span style="font-family: 宋体;color: rgb(51, 51, 51);letter-spacing: 0;font-size: 19px">工作已结束，</span><span style="font-family: 宋体;color: rgb(51, 51, 51);letter-spacing: 0;font-size: 19px">现将</span><span style="font-family: 宋体;color: rgb(51, 51, 51);letter-spacing: 0;font-size: 19px">采购</span><span style="font-family: 宋体;color: rgb(51, 51, 51);letter-spacing: 0;font-size: 19px">结果公示如下：</span></p><p style="margin-top:0;margin-right:0;margin-bottom:0;margin-left:0;text-indent:37px;padding:0 0 0 0 ;text-align:justify;text-justify:inter-ideograph"><span style="font-family: 宋体;color: rgb(51, 51, 51);letter-spacing: 0;font-size: 19px">拟成交人：广西华融达计量质量检验检测有限公司</span></p><p style="margin-top:0;margin-right:0;margin-bottom:0;margin-left:0;text-indent:37px;padding:0 0 0 0 ;text-align:justify;text-justify:inter-ideograph"><span style="font-family: 宋体;color: rgb(51, 51, 51);letter-spacing: 0;font-size: 19px"><span style="font-family:宋体">拟成交金额：人民币</span><span style="font-family:宋体">135416元</span></span></p><p style="text-indent: 32px"><span style="font-family: 宋体;color: rgb(51, 51, 51);letter-spacing: 0;font-size: 19px">&nbsp;</span></p><p style="margin-top:8px;margin-right:0;margin-bottom:8px;margin-left:0;text-indent:0"><span style="font-family: 宋体;color: rgb(51, 51, 51);letter-spacing: 0;font-size: 19px">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;广西融安鱼峰水泥有限公司</span></p><p><span style="font-family: 宋体;color: rgb(51, 51, 51);letter-spacing: 0;font-size: 19px">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 202</span><span style="font-family: 宋体;color: rgb(51, 51, 51);letter-spacing: 0;font-size: 19px">4</span><span style="font-family: 宋体;color: rgb(51, 51, 51);letter-spacing: 0;font-size: 19px">年</span><span style="font-family: 宋体;color: rgb(51, 51, 51);letter-spacing: 0;font-size: 19px">8</span><span style="font-family: 宋体;color: rgb(51, 51, 51);letter-spacing: 0;font-size: 19px">月</span><span style="font-family: 宋体;color: rgb(51, 51, 51);letter-spacing: 0;font-size: 19px">31</span><span style="font-family: 宋体;color: rgb(51, 51, 51);letter-spacing: 0;font-size: 19px">日</span></p><br><a href="https://gxygcg.ejy365.com/#/purchase/detail/2/ZBCG/64359">点击查看原文</a>'
  // }
  // const content = ref(saa);
  const fetchData = async () => {
    try {
      const aid = route.params.id;
      const res = getItemById(aid);
      const content = ref(res);
  
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };
  
  onMounted(() => {
    fetchData();
  });
  
  </script>
  
  <style lang="less" scoped>
  .page-content {
    display: flex;
    flex-direction: column;
    min-height: 100%;
  }
  
  .custom-title-container {
    width: 100%;
    display: flex;
    justify-content: center;
    margin-bottom: 24px;
    margin-top: 24px;
  }
  
  .custom-centered-title {
    font-size: 20px;
    font-weight: bold;
    text-align: center;
    margin: 0;
  }
  
  .content-detail {
    .meta {
      margin-bottom: 16px;
      color: @text-color-secondary;
    }
    .body {
      line-height: 1.8;
      font-size: 16px;
    }
  }
  
  .footer-info {
    text-align: right;
    color: @text-color-secondary;
    font-size: 14px;
    margin-top: auto;
  }
  
  :deep(.ant-page-header-heading) {
    display: none;
  }
  
  :deep(.ant-page-header-content) {
    padding-top: 24px;
  }
  
  :deep(.ant-descriptions) {
    .ant-descriptions-row {
      display: flex;
      justify-content: space-between;
    }
    .ant-descriptions-item {
      padding-bottom: 0;
      display: flex;
      flex-direction: column;
      align-items: center;
      text-align: center;
    }
    .ant-descriptions-item-label {
      margin-bottom: 4px;
    }
  }
  :deep(.ant-descriptions) {
    .ant-descriptions-item {
      flex: 1; /* 使每个描述项平均分配空间 */
      display: flex;
      flex-direction: column;
      align-items: center;
      text-align: center;
      padding: 0 8px; /* 可调整内边距，增加间距 */
    }
  }
  
  </style>