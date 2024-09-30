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

const { t } = useI18n();

// 添加这些映射，解决值的对应关系
export const configStatusMap = {
  0: t('common.websiteInfo.configStatusPending'),
  1: t('common.websiteInfo.configStatusConfigured'),
};

export const crawlStatusMap = {
  0: t('common.websiteInfo.crawlStatusPending'),
  1: t('common.websiteInfo.crawlStatusNormal'),
  '-1': t('common.websiteInfo.crawlStatusError'),
  '-2': t('common.websiteInfo.crawlStatusSiteError'),
};

export const importanceLevelMap = {
  0: t('common.websiteInfo.importanceLevelSpecial'),
  1: t('common.websiteInfo.importanceLevelA'),
  2: t('common.websiteInfo.importanceLevelB'),
  3: t('common.websiteInfo.importanceLevelC'),
};

export const websiteTypeMap = {
  1: '政府和军事',
  2: '央国企',
  3: '学校',
  4: '医院',
  5: '招标代理机构',
  6: '民营企业',
  7: '公共资源交易中心',
  8: '知名招投标公司或平台',
  9: '其它'
};

export const industryMap = {
  1:"交通运输",
  2:"网络通讯计算机",
  3:"市政房地产建筑",
  4:"水利桥梁",
  5:"机械电子电器",
  6:"环保",
  8:"医疗卫生",
  9:"科技文教旅游",
  10:"冶金矿产原材料",
  11:"出版印刷",
  12:"轻工纺织食品",
  13:"农林牧渔",
  14:"商业服务",
  15:"其它",
  16:"园林绿化",
  17:"能源",
  18:"化工",
  0:"未知"
}


export const columns: BasicColumn[] = [

    
  {
    title: t('common.cms_data.aus_id'),
    dataIndex: 'aus_id',
    width: 180,
    customRender: ({ text, record }) => {
      return {
        children: h(
            'a',
            {
              href: `/cms_detail/${record.aus_id}`,
              target: '_blank',
              rel: 'noopener noreferrer'
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
    title: t('common.task_name.title'),
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
