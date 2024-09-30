/**
 * -*- coding: utf-8 -*-
 * time: 2024/5/22 23:43
 *
 *
 */
import { defHttp } from '/@/utils/http/axios';

enum DeptApi {
  prefix = '/api/gxtask/queryTasks',
  create = '/api/gxtask/create_task',
  update = '/api/gxtask/update_task',
}
/**
 * 获取list
 */
export const getList = (params) => {
  return defHttp.get({ url: DeptApi.prefix, params });
};

/**
 * 保存或更新
 */
export const createOrUpdate = (params, isUpdate) => {
  if (isUpdate) {
    console.log(params)
    return defHttp.put({ url: DeptApi.update + '/' + params.id, params });
  } else {
    return defHttp.post({ url: DeptApi.create, params });
  }
};

/**
 * 导入
 */
export const importData = (params) => {
  return defHttp.post({ url: DeptApi.prefix + '/all/import', params });
};

/**
 * 导出
 */
export const exportData = () => {
  return defHttp.get(
    { url: DeptApi.prefix + '/all/export', responseType: 'blob' },
    { isReturnNativeResponse: true },
  );
};

/**
 * 删除
 */
export const deleteItem = (id) => {
  return defHttp.delete({ url: DeptApi.prefix + '/' + id });
};
