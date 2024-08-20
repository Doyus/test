/**
 * -*- coding: utf-8 -*-
 * time: 2024/5/22 23:43
 *
 *
 */
import { defHttp } from '/@/utils/http/axios';

enum DeptApi {
  prefix = '/api/system/monitor',
}

export const getSystemInfo = () => {
  return defHttp.get({ url: DeptApi.prefix });
};
