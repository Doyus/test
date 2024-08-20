/**
 * -*- coding: utf-8 -*-
 * time: 2024/5/26 23:54
 *
 *
 */
import { BasicColumn } from '/@/components/Table';
import { FormSchema } from '/@/components/Table';
import { useI18n } from '/@/hooks/web/useI18n';

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


export const columns: BasicColumn[] = [



  {
    title: t('common.websiteInfo.siteName'),
    dataIndex: 'site_name',
    width: 200,
  },
  {
    title: t('common.websiteInfo.mainHost'),
    dataIndex: 'main_host',
    width: 180,
  },
  {
    title: t('common.websiteInfo.demandSide'),
    dataIndex: 'demand_side',
    width: 150,
  },
  {
    title: t('common.websiteInfo.siteUrl'),
    dataIndex: 'site_url',
    width: 200,
  },
  {
    title: t('common.websiteInfo.websiteType'),
    dataIndex: 'website_type',
    width: 120,
  },
  {
    title: t('common.websiteInfo.crawlStatus'),
    dataIndex: 'crawl_status',
    width: 100,
    customRender: ({ text }) => crawlStatusMap[text] || text,
  },
  {
    title: t('common.websiteInfo.configStatus'),
    dataIndex: 'config_status',
    width: 100,
    customRender: ({ text }) => configStatusMap[text] || text,
  },
  {
    title: t('common.websiteInfo.importanceLevel'),
    dataIndex: 'importance_level',
    width: 100,
    customRender: ({ text }) => importanceLevelMap[text] || text,
  },
  {
    title: t('common.websiteInfo.jrStorage'),
    dataIndex: 'jr_storage',
    width: 120,
  },
  {
    title: t('common.createDateText'),
    dataIndex: 'created_at',
    width: 180,
  },
];

// 搜索表单字段
export const searchFormSchema: FormSchema[] = [
  {
    field: 'site_name',
    label: t('common.websiteInfo.siteName'),
    component: 'Input',
    colProps: { span: 4 },
  },
  {
    field: 'main_host',
    label: t('common.websiteInfo.mainHost'),
    component: 'Input',
    colProps: { span: 4 },
  },
  {
    field: 'config_person',
    label: t('common.websiteInfo.crawlPerson'),
    component: 'Input',
    colProps: { span: 4 },
  },
  {
    field: 'crawl_status',
    label: t('common.websiteInfo.crawlStatus'),
    component: 'Select',
    componentProps: {
      options: [
        { label: t('common.websiteInfo.crawlStatusPending'), value: 0 },
        { label: t('common.websiteInfo.crawlStatusNormal'), value: 1 },
        { label: t('common.websiteInfo.crawlStatusError'), value: -1 },
        { label: t('common.websiteInfo.crawlStatusSiteError'), value: -2 },
      ],
    },
    colProps: { span: 4 },
  },
];

// 添加表单字段
export const formSchema: FormSchema[] = [
  {
    field: 'id',
    label: 'id',
    component: 'Input',
    show: false,
  },
  {
    field: 'demand_side',
    label: t('common.websiteInfo.demandSide'),
    component: 'Input',
  },
  {
    field: 'main_host',
    label: t('common.websiteInfo.mainHost'),
    required: true,
    component: 'Input',
  },
  {
    field: 'site_name',
    label: t('common.websiteInfo.siteName'),
    required: true,
    component: 'Input',
  },
  {
    field: 'site_url',
    label: t('common.websiteInfo.siteUrl'),
    component: 'Input',
  },
  {
    field: 'website_type',
    label: t('common.websiteInfo.websiteType'),
    component: 'Input',
  },
  {
    field: 'site_province',
    label: t('common.websiteInfo.siteProvince'),
    component: 'Input',
  },
  {
    field: 'site_city',
    label: t('common.websiteInfo.siteCity'),
    component: 'Input',
  },
  {
    field: 'site_county',
    label: t('common.websiteInfo.siteCounty'),
    component: 'Input',
  },
  {
    field: 'industry',
    label: t('common.websiteInfo.industry'),
    component: 'Input',
  },
  {
    field: 'crawl_status',
    component: 'Select',
    label: t('common.websiteInfo.crawlStatus'),
    componentProps: {
      options: [
        { label: t('common.websiteInfo.crawlStatusPending'), value: 0 },
        { label: t('common.websiteInfo.crawlStatusNormal'), value: 1 },
        { label: t('common.websiteInfo.crawlStatusError'), value: -1 },
        { label: t('common.websiteInfo.crawlStatusSiteError'), value: -2 },
      ],
    },
  },
  {
    field: 'crawl_person',
    label: t('common.websiteInfo.crawlPerson'),
    component: 'Input',
  },
  {
    field: 'config_status',
    component: 'Select',
    label: t('common.websiteInfo.configStatus'),
    componentProps: {
      options: [
        { label: t('common.websiteInfo.configStatusPending'), value: 0 },
        { label: t('common.websiteInfo.configStatusConfigured'), value: 1 },
      ],
    },
  },
  {
    field: 'config_person',
    label: t('common.websiteInfo.configPerson'),
    component: 'Input',
  },
  {
    field: 'importance_level',
    component: 'Select',
    label: t('common.websiteInfo.importanceLevel'),
    componentProps: {
      options: [
        { label: t('common.websiteInfo.importanceLevelSpecial'), value: 0 },
        { label: t('common.websiteInfo.importanceLevelA'), value: 1 },
        { label: t('common.websiteInfo.importanceLevelB'), value: 2 },
        { label: t('common.websiteInfo.importanceLevelC'), value: 3 },
      ],
    },
  },
  {
    field: 'remark',
    label: t('common.websiteInfo.remark'),
    component: 'InputTextArea',
  },
];
