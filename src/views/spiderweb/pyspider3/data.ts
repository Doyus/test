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

  // {
  //   title: t('common.websiteInfo.siteName'),
  //   dataIndex: 'site_name',
  //   width: 200,
  // },
  {
    title: t('common.websiteInfo.siteName'),
    dataIndex: 'site_name',
    width: 200,
    customRender: ({ text, record }) => {
      return {
        children: h(
          'a',
          {
            href: record.site_url,
            target: '_blank',
            rel: 'noopener noreferrer'
          },
          text
        )
      };
    }
  },
  
  {
    title: t('common.websiteInfo.mainHost'),
    dataIndex: 'main_host',
    width: 180,
  },
  // {
  //   title: t('common.websiteInfo.demandSide'),
  //   dataIndex: 'demand_side',
  //   width: 150,
  // },
  {
    title: t('common.websiteInfo.websiteType'),
    dataIndex: 'website_type',
    width: 100,
    customRender: ({ text }) => websiteTypeMap[text] || text,
  },

  {
    title: t('common.websiteInfo.siteLocation'),
    dataIndex: 'site_location',
    width: 120,
    customRender: ({ record }) => {
      const province = record.site_province || '';
      const city = record.site_city || '';
      const county = record.site_county || '';
      return `${province} ${city} ${county}`.trim();
    },
  },

  {
    title: t('common.websiteInfo.industry'),
    dataIndex: 'industry',
    width: 100,
    customRender: ({ text }) => industryMap[text] || text,
  },
  // {
  //   title: t('common.websiteInfo.siteUrl'),
  //   dataIndex: 'site_url',
  //   width: 200,
  // },

  
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
    title: t('common.websiteInfo.crawlPerson'),
    dataIndex: 'crawl_person',
    width: 100,
  },
  {
    title: t('common.websiteInfo.importanceLevel'),
    dataIndex: 'importance_level',
    width: 90,
    customRender: ({ text }) => importanceLevelMap[text] || text,
  },
  {
    title: t('common.websiteInfo.jrStorage'),
    dataIndex: 'jr_storage',
    width: 60,
  },
  {
    title: t('common.websiteInfo.zrStorage'),
    dataIndex: 'zr_storage',
    width: 60,
  },
  {
    title: t('common.websiteInfo.qrStorage'),
    dataIndex: 'qr_storage',
    width: 60,
  },
  {
    title: t('common.websiteInfo.monStorage'),
    dataIndex: 'mon_storage',
    width: 70,
  },
  {
    title: t('common.createDateText'),
    dataIndex: 'created_at',
    width: 150,
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
    ifShow: ({ values }) => values.isUpdate, // 添加时候不现实此字段,由程序根据site_url生成
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
  // {
  //   field: 'website_type',
  //   label: t('common.websiteInfo.websiteType'),
  //   component: 'Input',
  // },
  {
    field: 'website_type',
    label: t('common.websiteInfo.websiteType'),
    component: 'Select',
    componentProps: {
      options: [
        { label: '政府和军事', value: '1' },
        { label: '央国企', value: '2' },
        { label: '学校', value: '3' },
        { label: '医院', value: '4' },
        { label: '招标代理机构', value: '5' },
        { label: '民营企业', value: '6' },
        { label: '公共资源交易中心', value: '7' },
        { label: '知名招投标公司或平台', value: '8' },
        { label: '其它', value: '9' }

      ],
    },
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
    component: 'Select',
    componentProps: {
      options: [
        {label:'交通运输',value:'1'},
        {label:'网络通讯计算机',value:'2'},
        {label:'市政房地产建筑',value:'3'},
        {label:'水利桥梁',value:'4'},
        {label:'机械电子电器',value:'5'},
        {label:'环保',value:'6'},
        {label:'医疗卫生',value:'8'},
        {label:'科技文教旅游',value:'9'},
        {label:'冶金矿产原材料',value:'10'},
        {label:'出版印刷',value:'11'},
        {label:'轻工纺织食品',value:'12'},
        {label:'农林牧渔',value:'13'},
        {label:'商业服务',value:'14'},
        {label:'其它',value:'15'},
        {label:'园林绿化',value:'16'},
        {label:'能源',value:'17'},
        {label:'化工',value:'18'},
        {label:'未知',value:'0'}
      ],
    },
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
  // {
  //   field: 'config_person',
  //   label: t('common.websiteInfo.configPerson'),
  //   component: 'Input',
  // },
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
