<template>
    <div>
      <PageWrapper :title="t('common.detailPage')">
        <Description
          :schema="schema"
          :data="detailData"
        />
      </PageWrapper>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, ref, onMounted } from 'vue';
  import { useRoute } from 'vue-router';
  import { useI18n } from '/@/hooks/web/useI18n';
  import { Description, DescItem } from '/@/components/Description';
  import { PageWrapper } from '/@/components/Page';
  import { getItemById } from './api';
  
  export default defineComponent({
    name: 'CmsDataDetail',
    components: { Description, PageWrapper },
    setup() {
      const { t } = useI18n();
      const route = useRoute();
      const detailData = ref({});
  
      const schema: DescItem[] = [
        {
          field: 'aus_id',
          label: t('common.cms_data.aus_id'),
        },
        {
          field: 'main_host',
          label: t('common.cms_data.main_host'),
        },
        {
          field: 'title',
          label: t('common.cms_data.title'),
        },
        // ... 添加其他字段
      ];
  
      onMounted(async () => {
        const id = route.params.id as string;
        const result = await getItemById(id);
        detailData.value = result;
      });
  
      return {
        t,
        schema,
        detailData,
      };
    },
  });
  </script>