import { createRouter, createWebHistory } from 'vue-router';
import ChatPage from '@/components/ChatPage.vue'; // 确保路径正确
import SettingsPage from '@/components/Settings.vue'; // 确保路径正确
const routes = [
  // 其他路由
  {
    path: '/chat',
    name: 'Chat',
    component: ChatPage,
    meta: { layout: 'chat' } // 添加元信息指示使用特定布局
  },
  {
    path: '/settings',
    name: 'Settings',
    component: SettingsPage,
  }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});

export default router;
