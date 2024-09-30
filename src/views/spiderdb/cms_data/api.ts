/**
 * -*- coding: utf-8 -*-
 * time: 2024/5/22 23:43
 *
 *
 */
import { defHttp } from '/@/utils/http/axios';

enum DeptApi {
  prefix = '/api/gxspider/cms_data',
}
/**
 * 获取list
 */
export const getList = (params) => {
  return defHttp.get({ url: DeptApi.prefix, params });
};
// * 获取单个项目详情

export const getItemById = (id: string) => {
  return defHttp.get({ url: `${DeptApi.prefix}/${id}` });
};

/**
 * 保存或更新
 */
export const createOrUpdate = (params, isUpdate) => {
  if (isUpdate) {
    return defHttp.put({ url: DeptApi.prefix + '/' + params.id, params });
  } else {
    return defHttp.post({ url: DeptApi.prefix, params });
  }
};


/**
 * 删除
 */
export const deleteItem = (id) => {
  return defHttp.delete({ url: DeptApi.prefix + '/' + id });
};
