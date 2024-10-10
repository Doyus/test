import type { AppRouteModule } from '/@/router/types';
import { t } from '/@/hooks/web/useI18n';

const cms_detail: AppRouteModule = {
  path: '/cms_detail/:id',
  name: 'CmsDetail',
  component: () => import('/@/views/spiderdb/cms_data/Detail.vue'),
  meta: {
    orderNo: 10,
    icon: 'ion:grid-outline',
    title: t('routes.dashboard.dashboard'),
  },
};

export default cms_detail;