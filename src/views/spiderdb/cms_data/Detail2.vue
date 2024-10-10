<template>
  <PageWrapper  :content="content.category + ' | ' + content.area" contentBackground>

    <!-- <template #title>
      <div class="centered-title">{{ content.title }}</div>
    </template> -->
      <!-- <a-button type="primary">编辑23</a-button> -->
      <!-- <div class="centered-title">{{ content.title }}</div> -->
<!--     
    <template #extra>
      <div class="title-container">
        <h1 class="centered-title">{{ content.title }}</h1>
      </div>
    </template> -->

    <template #headerContent>
      <div class="title-container">
        <h1 class="centered-title">{{ content.title }}</h1>
      </div>
    </template>

    
    <Card :bordered="false">
      <div class="content-detail">
        <div class="meta">
          <a-descriptions :column="2">
            <a-descriptions-item label="发布日期">{{ formatDate(content.publish_date) }}</a-descriptions-item>
            <a-descriptions-item label="地区">{{ content.area }}</a-descriptions-item>
            <a-descriptions-item label="类别">{{ content.category }}</a-descriptions-item>
            <a-descriptions-item label="来源">{{ getSource(content.source) }}</a-descriptions-item>
          </a-descriptions>
        </div>
        <Divider />
        <div class="body" v-html="content.description"></div>
      </div>
    </Card>
    <template #footer>
      <div class="footer-info">
        <p>采购ID: {{ content.aus_id }}</p>
        <p>原始链接: <a :href="content.comments" target="_blank">查看原文</a></p>
      </div>
    </template>
  </PageWrapper>
</template>

<script lang="ts" setup>
import { ref } from 'vue';
import { PageWrapper } from '/@/components/Page';
import { Card, Descriptions, Divider } from 'ant-design-vue';

const json_data = {
  'aus_id': 2716206,
  'title': '广西融安鱼峰水泥有限公司2024-2025年计量仪表外协检定项目成交结果公告',
  'comments': 'https://gxygcg.ejy365.com/#/purchase/detail/2/ZBCG/64359',
  'publish_date': '2024-09-01',
  'area': '广西壮族自治区',
  'category': '其它',
  'source': '5',
  'description':"正文"
};

const content = ref(json_data);

const formatDate = (dateString: string) => {
  const date = new Date(dateString);
  return `${date.getFullYear()}年${date.getMonth() + 1}月${date.getDate()}日`;
};

const getSource = (sourceCode: string) => {
  const sources = {
    '5': '广西阳光采购服务平台',
    // 添加其他来源映射
  };
  return sources[sourceCode] || '未知来源';
};
</script>

<style lang="less" scoped>

// .title-container {
//   width: 100%;
//   display: flex;
//   justify-content: center;
//   align-items: center;
//   margin-bottom: 16px;
// }

// // .centered-title {
// //   font-size: 20px;
// //   font-weight: bold;
// //   text-align: center;
// //   margin: 0;
// // }
// .centered-title {
//   text-align: center;
//   width: 100%;
//   font-size: 20px;
//   font-weight: bold;
//   margin-bottom: 16px;
// }
// .content-detail {
//   .meta {
//     margin-bottom: 16px;
//     color: @text-color-secondary;
//   }
//   .body {
//     line-height: 1.8;
//     font-size: 16px;
//   }
// }
// .footer-info {
//   text-align: right;
//   color: @text-color-secondary;
//   font-size: 14px;
// }


.title-container {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 16px;
}

.centered-title {
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
}
</style>

  <!-- 'description': '<p style="text-align:center;line-height:39px"><strong><span style="font-family: 宋体;letter-spacing: 0;font-size: 19px">广西融安鱼峰水泥有限公司</span></strong><strong><span style="font-family: 宋体;letter-spacing: 0;font-size: 19px">2024-2025年计量仪表外协检定项目</span></strong><strong><span style="font-family: 宋体;letter-spacing: 0;font-size: 19px">成交结果公告</span></strong></p><p style="margin: 0 0 10px;text-indent: 32px"><span style="font-family: 宋体;color: rgb(51, 51, 51);letter-spacing: 0;font-size: 19px">&nbsp;</span></p><p style="text-indent: 32px"><span style=";font-family:宋体;font-size:19px">2024-2025年计量仪表外协检定项目（项目编号：RAYF-2024-88），</span><span style="font-family: 宋体;color: rgb(51, 51, 51);letter-spacing: 0;font-size: 19px">采购</span><span style="font-family: 宋体;color: rgb(51, 51, 51);letter-spacing: 0;font-size: 19px">工作已结束，</span><span style="font-family: 宋体;color: rgb(51, 51, 51);letter-spacing: 0;font-size: 19px">现将</span><span style="font-family: 宋体;color: rgb(51, 51, 51);letter-spacing: 0;font-size: 19px">采购</span><span style="font-family: 宋体;color: rgb(51, 51, 51);letter-spacing: 0;font-size: 19px">结果公示如下：</span></p><p style="margin-top:0;margin-right:0;margin-bottom:0;margin-left:0;text-indent:37px;padding:0 0 0 0 ;text-align:justify;text-justify:inter-ideograph"><span style="font-family: 宋体;color: rgb(51, 51, 51);letter-spacing: 0;font-size: 19px">拟成交人：广西华融达计量质量检验检测有限公司</span></p><p style="margin-top:0;margin-right:0;margin-bottom:0;margin-left:0;text-indent:37px;padding:0 0 0 0 ;text-align:justify;text-justify:inter-ideograph"><span style="font-family: 宋体;color: rgb(51, 51, 51);letter-spacing: 0;font-size: 19px"><span style="font-family:宋体">拟成交金额：人民币</span><span style="font-family:宋体">135416元</span></span></p><p style="text-indent: 32px"><span style="font-family: 宋体;color: rgb(51, 51, 51);letter-spacing: 0;font-size: 19px">&nbsp;</span></p><p style="margin-top:8px;margin-right:0;margin-bottom:8px;margin-left:0;text-indent:0"><span style="font-family: 宋体;color: rgb(51, 51, 51);letter-spacing: 0;font-size: 19px">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;广西融安鱼峰水泥有限公司</span></p><p><span style="font-family: 宋体;color: rgb(51, 51, 51);letter-spacing: 0;font-size: 19px">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 202</span><span style="font-family: 宋体;color: rgb(51, 51, 51);letter-spacing: 0;font-size: 19px">4</span><span style="font-family: 宋体;color: rgb(51, 51, 51);letter-spacing: 0;font-size: 19px">年</span><span style="font-family: 宋体;color: rgb(51, 51, 51);letter-spacing: 0;font-size: 19px">8</span><span style="font-family: 宋体;color: rgb(51, 51, 51);letter-spacing: 0;font-size: 19px">月</span><span style="font-family: 宋体;color: rgb(51, 51, 51);letter-spacing: 0;font-size: 19px">31</span><span style="font-family: 宋体;color: rgb(51, 51, 51);letter-spacing: 0;font-size: 19px">日</span></p>' -->
#