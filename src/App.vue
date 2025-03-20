<template>
  <v-app>
    <Top />
    <!-- 根据路由动态显示或隐藏组件 -->
    <MainTheme v-if="$route.path !== '/chat' && $route.path !== '/settings'" />
    <Background_img v-if="$route.path !== '/chat' && $route.path !== '/settings'" />
    <!-- 页面内容渲染区域 -->
    <router-view/>
  </v-app>
</template>

<script>
import Top from './components/Top.vue'
import MainTheme from './components/MainTheme.vue'
import Background_img from './components/Background_img.vue'

export default {
  name: 'App',
  components: {
    Top,
    MainTheme,
    Background_img,
  },
  data: () => ({
    drawer: false
  }),
}
</script>
