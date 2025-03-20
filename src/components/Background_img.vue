<!-- src/components/Background.vue -->
<template>
    <div class="background"></div>
  </template>
  
  <script>
  export default {
    name: 'Background_img'
  };
  </script>
  
  <style scoped>
  .background {
    position: fixed; /* 背景固定位置 */
    top: 20%;
    left:40%;
    right: 50%;
    width: 20%; /* 覆盖整个视口宽度 */
    height: 30%; /* 覆盖整个视口高度 */
    /* 低些 */

    background-image: url('@/assets/IIRLAB高清文件-02.jpg'); /* 替换为你的图片路径 */
    background-position: center center;
    background-repeat: no-repeat;
    background-size: contain;
     /* filter: blur(5px);  /
    /* z-index: -1; 确保背景在内容之下 */
  }
  </style>
  