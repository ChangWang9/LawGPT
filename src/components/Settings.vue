<template>
    <v-container>
      <v-row justify="center">
        <v-col cols="12" md="8">
          <v-card>
            <v-card-title class="headline">设置</v-card-title>
            <v-card-text>
              <v-list>
                <!-- 主题设置 -->
                <v-list-item>
                  <v-list-item-content>
                    <v-list-item-title>深色模式</v-list-item-title>
                    <v-list-item-subtitle>切换深色/浅色主题</v-list-item-subtitle>
                  </v-list-item-content>
                  <v-list-item-action>
                    <v-switch v-model="darkMode"></v-switch>
                  </v-list-item-action>
                </v-list-item>
  
                <!-- 温度滑块 -->
                <v-list-item>
                  <v-list-item-content>
                    <v-list-item-title>温度</v-list-item-title>
                    <v-list-item-subtitle>控制生成文本的随机性 ({{ temperature }})</v-list-item-subtitle>
                  </v-list-item-content>
                  <v-list-item-action class="slider-container">
                    <v-slider
                      v-model="temperature"
                      min="0.01"
                      max="1.0"
                      step="0.01"
                      thumb-label
                    ></v-slider>
                  </v-list-item-action>
                </v-list-item>
  
                <!-- 最大生成令牌数 -->
                <v-list-item>
                  <v-list-item-content>
                    <v-list-item-title>最大生成令牌数</v-list-item-title>
                    <v-list-item-subtitle>控制生成文本的长度 ({{ maxTokens }})</v-list-item-subtitle>
                  </v-list-item-content>
                  <v-list-item-action class="slider-container">
                    <v-slider
                      v-model="maxTokens"
                      min="1"
                      max="2048"
                      step="1"
                      thumb-label
                    ></v-slider>
                  </v-list-item-action>
                </v-list-item>
  
                <!-- 检索文档数量 -->
                <v-list-item>
                  <v-list-item-content>
                    <v-list-item-title>检索文档数量</v-list-item-title>
                    <v-list-item-subtitle>每次检索返回的文档数量 ({{ topK }})</v-list-item-subtitle>
                  </v-list-item-content>
                  <v-list-item-action class="slider-container">
                    <v-slider
                      v-model="topK"
                      min="1"
                      max="10"
                      step="1"
                      thumb-label
                    ></v-slider>
                  </v-list-item-action>
                </v-list-item>
  
                <!-- 模型选择 -->
                <v-list-item>
                  <v-list-item-content>
                    <v-list-item-title>模型选择</v-list-item-title>
                  </v-list-item-content>
                  <v-list-item-action>
                    <v-select
                      v-model="selectedModel"
                      :items="availableModels"
                      outlined
                      dense
                    ></v-select>
                  </v-list-item-action>
                </v-list-item>
              </v-list>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </template>
  
  <script>
  export default {
    name: 'SettingsPage',
    data: () => ({
      darkMode: false,
      temperature: 0.5,
      maxTokens: 256,
      topK: 5,
      selectedModel: 'qwen-14B',
      availableModels: ['qwen-14B', 'bge-zh', 'gpt-3.5-turbo']
    }),
    watch: {
      darkMode(val) {
        this.$vuetify.theme.dark = val;
      },
      temperature(val) {
        // 在这里处理温度变化
        console.log('Temperature changed:', val);
      },
      maxTokens(val) {
        // 在这里处理最大令牌数变化
        console.log('Max tokens changed:', val);
      },
      topK(val) {
        // 在这里处理检索文档数量变化
        console.log('Top K changed:', val);
      },
      selectedModel(val) {
        // 在这里处理模型选择变化
        console.log('Selected model changed:', val);
      }
    }
  }
  </script>
  
  <style scoped>
  .slider-container {
    min-width: 200px;
  }
  </style>