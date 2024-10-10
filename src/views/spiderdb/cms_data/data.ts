/**
 * -*- coding: utf-8 -*-
 * time: 2024/8/26 23:54
 *
 *
 */
import { BasicColumn } from '/@/components/Table';
import { FormSchema } from '/@/components/Table';
import { useI18n } from '/@/hooks/web/useI18n';
import { h } from 'vue';
import { useRouter } from 'vue-router';
import { useGo } from '/@/hooks/web/usePage';
import { RouterLink } from 'vue-router';


const { t } = useI18n();

export const columns: BasicColumn[] = [

    
  // {
  //   title: t('common.cms_data.aus_id'),
  //   dataIndex: 'aus_id',
  //   width: 200,
  //   customRender: ({ text, record }) => {
  //     return {
  //       children: h(
  //           'a',
  //           {
  //             href: record.comments,
  //             target: '_blank',
  //             rel: 'noopener noreferrer'
  //           },
  //           text
  //       )
  //     };
  //   }
  // },
  {
    title: t('common.cms_data.aus_id'),
    dataIndex: 'aus_id',
    width: 200,
    customRender: ({ text, record }) => {
      const go = useGo();
      return {
        children: h(
          'button',
          {
            onClick: () => go({ path: `/detail/${record.aus_id}` }), // 根据需要修改路径
            // onClick: () => go({ name: 'Detail', params: { id: record.aus_id } }), // 根据需要修改路径
            style: { background: 'none', border: 'none', color: 'blue', cursor: 'pointer' }
          },
          text
        )
      };
    }
  },

  {
    title: t('common.cms_data.main_host'),
    dataIndex: 'main_host',
    width: 180,
  }, 
  // {
  //   title: t('common.cms_data.title'),
  //   dataIndex: 'title',
  //   width: 180,
  // },
  {
    title: t('common.cms_data.title'),
    dataIndex: 'title',
    width: 200,
    customRender: ({ text, record }) => {
      return {
        children: h(
            'a',
            {
              href: record.comments,
              target: '_blank',
              rel: 'noopener noreferrer'
            },
            text
        )
      };
    }
  },
  {
    title: t('common.cms_data.comments'),
    dataIndex: 'comments',
    width: 180,
  }, 
  {
    title: t('common.cms_data.classd_name'),
    dataIndex: 'classd_name',
    width: 180,
  },
  {
    title: t('common.cms_data.publish_date'),
    dataIndex: 'publish_date',
    width: 180,
  },
  {
    title: t('common.cms_data.table_name'),
    dataIndex: 'table_name',
    width: 180,
  },
  {
    title: t('common.cms_data.table_name2'),
    dataIndex: 'table_name2',
    width: 180,
  },
  {
    title: t('common.cms_data.area'),
    dataIndex: 'area',
    width: 180,
  },
  {
    title: t('common.cms_data.category'),
    dataIndex: 'category',
    width: 180,
  },
  {
    title: t('common.cms_data.files'),
    dataIndex: 'files',
    width: 180,
  },
  {
    title: t('common.cms_data.created_at'),
    dataIndex: 'created_at',
    width: 180,
  },
  {
    title: t('common.cms_data.program_source'),
    dataIndex: 'program_source',
    width: 180,
  },
  {
    title: t('common.cms_data.responsible_person'),
    dataIndex: 'responsible_person',
    width: 180,
  },
  {
    title: t('common.cms_data.client_name'),
    dataIndex: 'client_name',
    width: 180,
  },
  {
    title: t('common.cms_data.client_ip'),
    dataIndex: 'client_ip',
    width: 180,
  },
  {
    title: t('common.cms_data.cms_id'),
    dataIndex: 'cms_id',
    width: 180,
  },
  {
    title: t('common.cms_data.source'),
    dataIndex: 'source',
    width: 180,
  }
  
];

// 搜索表单字段
export const searchFormSchema: FormSchema[] = [
  {
    field: 'classd_name',
    label: t('common.cms_data.classd_name'),
    component: 'Input',
    colProps: { span: 4 },
  },
  {
    field: 'title',
    label: t('common.cms_data.title'),
    component: 'Input',
    colProps: { span: 4 },
  },
  {
    field: 'comments',
    label: t('common.cms_data.comments'),
    component: 'Input',
    colProps: { span: 4 },
  },
  {
    field: 'publish_date',
    label: t('common.cms_data.publish_date'),
    component: 'Input',
    colProps: { span: 4 },
  },
  // {
  //   field: 'responsible_person',
  //   label: t('common.cms_data.responsible_person'),
  //   component: 'Input',
  //   colProps: { span: 4 },
  // } 
];

// 添加表单字段
export const formSchema: FormSchema[] = [
  
  // {
  //   field: 'website_type',
  //   label: t('common.websiteInfo.websiteType'),
  //   component: 'Input',
  // },

 
];