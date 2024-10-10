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
                <a-descriptions-item label="来源">来源：{{ content.classd_name }}</a-descriptions-item>
              </a-descriptions>
            </div>
            <Divider />
            <div class="body" v-html="content.description"></div>
          </div>
        </Card>
      </div>
      
      <div class="footer-info">
        <p>内容ID: {{ content.aus_id }}</p>
        <p>原始链接: <a :href="content.comments" target="_blank">查看原文</a></p>
      </div>
    </template>
  </PageWrapper>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue';
import { PageWrapper } from '/@/components/Page';
import { Card, Divider, message } from 'ant-design-vue';
import { useRoute } from 'vue-router';
import { getItemById } from './api';

const route = useRoute();
const content = ref({} as any);
const loading = ref(true);

const formatDate = (dateString: string) => {
  if (!dateString) return '';
  const date = new Date(dateString);
  return `${date.getFullYear()}年${date.getMonth() + 1}月${date.getDate()}日`;
};

const fetchData = async () => {
  try {
    loading.value = true;
    const aid = route.params.id as string;
    const res = await getItemById(aid);
    content.value = res;
  } catch (error) {
    console.error('Error fetching data:', error);
    message.error('获取数据失败，请稍后重试');
  } finally {
    loading.value = false;
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
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    padding: 0 8px;
  }
  .ant-descriptions-item-label {
    margin-bottom: 4px;
  }
}
</style>