<template>
  <div>
    <BasicTable @register="registerTable">
        <template #tableTitle>
            <Space style="height: 40px">
                <a-button
                        type="primary"
                        preIcon="ant-design:plus-outlined"
                        @click="handleCreate"
                >
                    {{ t('common.task_name.create_task') }}
                </a-button>
            </Space>
        </template>
      <template #bodyCell="{ column, record }">
        <template v-if="column.key === 'action'">
          <TableAction
            :actions="[
              {
                type: 'button',
                icon: 'clarity:note-edit-line',
                color: 'primary',
                onClick: handleEdit.bind(null, record),
              },
            ]"
          />
        </template>
      </template>
    </BasicTable>
    <DemoDrawer @register="registerDrawer" @success="handleSuccess" />
  </div>
</template>
<script lang="ts">
  import { defineComponent } from 'vue';

  import { BasicTable, useTable, TableAction } from '/@/components/Table';
  import { usePermission } from '/@/hooks/web/usePermission';
  import { useDrawer } from '/@/components/Drawer';
  import DemoDrawer from './Drawer.vue';
  import { Space } from 'ant-design-vue';
  import { BasicUpload } from '/@/components/Upload';
  import { deleteItem, getList, exportData, importData } from './api';
  import { columns, searchFormSchema } from './data';
  import { message } from 'ant-design-vue';
  import { useMessage } from '/@/hooks/web/useMessage';
  import { downloadByData } from '/@/utils/file/download';
  import { useI18n } from '/@/hooks/web/useI18n';
  export default defineComponent({
    name: 'spiderweb',
    components: { BasicTable, DemoDrawer, TableAction, BasicUpload, Space },
    setup() {
      const { t } = useI18n();
      const [registerDrawer, { openDrawer }] = useDrawer();
      const { createConfirm } = useMessage();
      const { hasPermission } = usePermission();
      const [registerTable, { reload, getSelectRows }] = useTable({
        api: getList,
        columns,
        formConfig: {
          labelWidth: 80,
          schemas: searchFormSchema,
        },
        useSearchForm: true,
        showTableSetting: true,
        tableSetting: { fullScreen: true },
        bordered: true,
        showIndexColumn: false,
        rowSelection: {
          type: 'checkbox',
        },
        actionColumn: {
          width: 150,
          title: t('common.operationText'),
          dataIndex: 'action',
          fixed: undefined,
        },
      });
      const statusOptions = defineComponent({
        0: '未开始',
        1: '进行中',
        2: '已完成',
        // ... 其他状态
      });

      const customRender = (text) => statusOptions.value[text];

      function handleCreate() {
        openDrawer(true, {
          isUpdate: false,
        });
      }

      function handleEdit(record: Recordable) {
        openDrawer(true, {
          record,
          isUpdate: true,
        });
      }

      async function handleDelete(id: number) {
        await deleteItem(id);
        message.success(t('common.successText'));
        await reload();
      }

      function handleBulkDelete() {
        if (getSelectRows().length == 0) {
          message.warning(t('common.batchDelHintText'));
        } else {
          createConfirm({
            iconType: 'warning',
            title: t('common.hintText'),
            content: t('common.delHintText'),
            async onOk() {
              for (const item of getSelectRows()) {
                await deleteItem(item.id);
              }
              message.success(t('common.successText'));
              await reload();
            },
          });
        }
      }

      async function handleChange(list: string[]) {
        console.log(list[0]);
        await importData({ path: list[0] });
        message.success(`导入成功`);
        await reload();
      }

      async function handleExportData() {
        const response = await exportData();
        await downloadByData(response.data, '项目数据.xlsx');
      }

      function handleSuccess() {
        message.success(t('common.successText'));
        reload();
      }

      return {
        registerTable,
        registerDrawer,
        handleCreate,
        handleEdit,
        handleDelete,
        handleSuccess,
        hasPermission,
        handleBulkDelete,
        getSelectRows,
        handleExportData,
        handleChange,
        statusOptions,
        customRender,
        t,
      };
    },
  });
</script>
