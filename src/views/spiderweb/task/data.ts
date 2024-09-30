/**
 * -*- coding: utf-8 -*-
 * time: 2024/5/26 23:54
 *
 *
 */
import { BasicColumn } from '/@/components/Table';
import { FormSchema } from '/@/components/Table';
import { useI18n } from '/@/hooks/web/useI18n';
import { h } from 'vue';

// import { getAreaTextByCode } from '/@/components/Form/src/utils/Area';
const { t } = useI18n();
export const crawlStatusMap = {
  0: t('common.task_name.crawlStatusStop'),
  1: t('common.task_name.crawlStatusRunning'),
  2: t('common.task_name.crawlStatusEnd'),
  '-1': t('common.task_name.crawlStatusSiteStart'),
  3: t('common.task_name.crawlStatusSiteEdit')
};
export const columns: BasicColumn[] = [
  {
    title: t('common.task_name.principal'),
    dataIndex: 'principal',
    width: 100,

  },
  {
    title: t('common.task_name.website_name'),
    dataIndex: 'website_name',
    width: 200,
    customRender: ({ text, record }) => {
      return {
        children: h(
            'a',
            {
              href: 'https://39.105.227.135:10000/static/create_task.html?id='+record.id,
              target: '_blank',
              rel: 'noopener noreferrer'
            },
            text
        )
      };
    }
  },
  {
    title: t('common.task_name.remark'),
    dataIndex: 'remark',
    width: 100,

  },
  {
    title: t('common.task_name.class_name'),
    dataIndex: 'class_name',
    width: 100,
  },
  {
    title: t('common.task_name.crawl_start_time'),
    dataIndex: 'crawl_start_time',
    width: 100,

  },
  {
    title: t('common.task_name.crawl_end_time'),
    dataIndex: 'crawl_end_time',
    width: 100,

  },
  {
    title: t('common.task_name.next_crawl_time'),
    dataIndex: 'next_crawl_time',
    width: 100,
  },
  {
    title: t('common.task_name.status'),
    dataIndex: 'status',
    width: 100,
    customRender: ({ text }) => crawlStatusMap[text] || text,
  },
  {
    title: t('common.task_name.crawl_consuming_time'),
    dataIndex: 'crawl_consuming_time',
    width: 100,
    customRender: ({ text, record }) => {
      console.log('ifShow values:', record.crawl_end_time); // 添加日志
      return Math.floor((new Date(record.crawl_end_time).getTime()-new Date(record.crawl_start_time).getTime())/1000);
    },

  },
];
// crawlStatusRunning: '正在运行',
//   crawlStatusStop: '停止运行',
//   crawlStatusEnd: '运行结束',
//   crawlStatusSiteStart: '准备运行',
  // crawlStatusSiteEdit: '配置中',

export const searchFormSchema: FormSchema[] = [
  {
    field: 'website_name',
    label: t('common.task_name.website_name'),
    component: 'Input',
    colProps: { span: 4 },
  },
  {
    field: 'status',
    label: t('common.task_name.status'),
    component: 'Select',
    componentProps: {
      options: [
        { label: t('common.task_name.crawlStatusStop'), value: 0 },
        { label: t('common.task_name.crawlStatusRunning'), value: 1 },
        { label: t('common.task_name.crawlStatusEnd'), value: 2 },
        { label: t('common.task_name.crawlStatusSiteStart'), value: -1 },
        { label: t('common.task_name.crawlStatusSiteEdit'), value: 3 },
      ],
    },
    colProps: { span: 4 },
  },
];



export const formSchema: FormSchema[] = [
    {
      field: 'isUpdate',
      label: '是否更新',
      component: 'Switch',
      show: false, // 如果不需要在表单中显示
    },
  {
    field: 'id',
    label: 'id',
    component: 'Input',
    show: false,
  },
  {
    field: 'website_name',
    label: t('common.task_name.website_name'),
    required: true,
    component: 'Input',
  },
  {
    field: 'class_name',
    label: t('common.task_name.class_name'),
    required: true,
    component: 'Input',
  },
  {
    field: 'remark',
    label: t('common.task_name.remark'),
    required: true,
    component: 'Input',
  },
  {
    field: 'principal',
    label: t('common.task_name.principal'),
    required: true,
    component: 'Input',
  },
  {
    field: 'main_host',
    label: t('common.task_name.main_host'),
    required: true,
    component: 'Input',
  },
  {
    field: 'crawl_interval',
    label: t('common.task_name.crawl_interval'),
    required: true,
    component: 'Input',
      ifShow: ({ values }) => {
          console.log('ifShow values:', values); // 添加日志
          return values.isUpdates;
      },
  },
  {
    field: 'run_dp',
    label: t('common.task_name.run_dp'),
    required: true,
    component: 'Select',
    componentProps: {
      options: [
        { label: '本地采集', value: 1 },
        { label: '云端采集', value: 2},

      ],
    },
      ifShow: ({ values }) => {
        return values.isUpdate;
      },
  },
  {
    field: 'is_proxy',
    label: t('common.task_name.proxyPool'),
    required: true,
    component: 'Select',
    componentProps: {
      options: [
        { label: '使用代理', value: 1 },
        { label: '不使用代理', value: 2},
      ],
    },
    ifShow: ({ values }) => {
          console.log('ifShow values:', values); // 添加日志
          return values.isUpdate;
      },
  },
  {
    field: 'selectedFields',
    label: t('common.task_name.selectedFields'),
    required: true,
    component: 'Select',
    componentProps: {
      mode: 'multiple', // 启用多选模式
      options: [
        // ["title", "publish_date", "comments"]
        { label: '标题', value: 'title' },
        { label: '发布时间', value: 'publish_date' },
        { label: '详情地址', value: 'comments' },
      ]
    },
    ifShow: ({ values }) => {
          console.log('ifShow values:', values); // 添加日志
          return values.isUpdate;
      },
  },

];
