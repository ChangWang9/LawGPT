<template>
    <v-container fluid class="pa-0 fill-height">
    <!-- 示例对话框卡片 -->
    <v-row justify="center" class="example-cards">
      <v-col cols="12" md="3" v-for="(example, index) in examples" :key="index">
        <v-card class="mx-auto" max-width="500" max-height = "100" outlined shadow = "always">
          <v-card-title>{{ example.title }}</v-card-title>
          
          <v-card-text class="d-flex justify-space-between align-center">
            <span>{{ example.description }}</span>
            <v-btn icon small @click="upload(example)">
              <v-icon size="20">mdi-upload</v-icon>
            </v-btn>
          </v-card-text>
            
        </v-card>
      </v-col>
    </v-row>
      <!-- 这里放置你的其他内容 -->
      <v-dialog v-model="dialog" max-width="800px">
        <v-card>
          <v-card-title>
            <span class="headline">上传{{ currentExample.title }}</span>
          </v-card-title>

          <v-card-text>
            <!-- 文本证据表单 -->
            <v-container v-if="currentExample.title === '文本证据 📖'">
              <v-row>
                <v-col cols="12">
                  <v-text-field v-model="caseData.案件类型" label="案件类型" outlined></v-text-field>
                </v-col>
                <v-col cols="12">
                  <v-textarea v-model="caseData.基本案情" label="基本案情" outlined auto-grow></v-textarea>
                </v-col>
                
                <!-- 原告信息 -->
                <v-col cols="12">
                  <v-expansion-panels>
                    <v-expansion-panel>
                      <v-expansion-panel-header>原告信息</v-expansion-panel-header>
                      <v-expansion-panel-content>
                        <v-row>
                          <v-col cols="12">
                            <v-combobox
                              v-model="caseData.原告.事实证据"
                              label="事实证据"
                              multiple
                              chips
                              outlined
                            ></v-combobox>
                          </v-col>
                          <v-col cols="12">
                            <v-combobox
                              v-model="caseData.原告.个人情况"
                              label="个人情况"
                              multiple
                              chips
                              outlined
                            ></v-combobox>
                          </v-col>
                          <v-col cols="12">
                            <v-combobox
                              v-model="caseData.原告.诉讼请求"
                              label="诉讼请求"
                              multiple
                              chips
                              outlined
                            ></v-combobox>
                          </v-col>
                        </v-row>
                      </v-expansion-panel-content>
                    </v-expansion-panel>
                  </v-expansion-panels>
                </v-col>

                <!-- 被告信息 -->
                <v-col cols="12">
                  <v-expansion-panels>
                    <v-expansion-panel>
                      <v-expansion-panel-header>被告信息</v-expansion-panel-header>
                      <v-expansion-panel-content>
                        <v-combobox
                          v-model="caseData.被告.个人情况"
                          label="个人情况"
                          multiple
                          chips
                          outlined
                        ></v-combobox>
                      </v-expansion-panel-content>
                    </v-expansion-panel>
                  </v-expansion-panels>
                </v-col>
              </v-row>
            </v-container>

            <!-- 图片证据表单 -->
            <!-- 图片证据表单 -->
            <v-container v-else>
              <v-row>
                <v-col cols="12">
                  <v-file-input
                    v-model="imageFiles"
                    label="选择图片"
                    multiple
                    accept="image/*"
                    prepend-icon="mdi-camera"
                    outlined
                  ></v-file-input>
                </v-col>
                
                <v-col cols="12" class="d-flex flex-wrap">
                  <v-card
                    v-for="(preview, index) in imagePreviews"
                    :key="index"
                    class="ma-2 preview-card"
                    width="200"
                  >
                    <v-img
                      :src="preview.url"
                      height="200"
                      contain
                    ></v-img>
                    <v-card-text class="text-center">
                      {{ imageFiles[index].name }}
                    </v-card-text>
                    <v-btn
                      icon
                      small
                      color="red"
                      class="remove-image"
                      @click="removeImage(index)"
                    >
                      <v-icon>mdi-close</v-icon>
                    </v-btn>
                  </v-card>
                </v-col>

                <v-col cols="12">
                  <v-textarea
                    v-model="imageDescription"
                    label="图片描述"
                    outlined
                    auto-grow
                    rows="3"
                    placeholder="请描述这些图片..."
                  ></v-textarea>
                </v-col>
              </v-row>
            </v-container>

          </v-card-text>

          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="blue darken-1" text @click="dialog = false">取消</v-btn>
            <v-btn color="blue darken-1" text @click="submitUpload">确认</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>

      <!-- 底部对话框 -->
      <v-row justify="center" class="fixed-bottom mb-6">
        <v-col cols="12" sm="8" md="7">
          <v-card tile class="d-flex">
            <v-card-text class="py-1 px-2">
              <v-row>
                <v-col cols="12">
                  <v-text-field
                    label="Type your message..."
                    append-icon="mdi-send"
                    filled
                    dense
                    
                    @click:append="$router.push('/chat')"
                  ></v-text-field>
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </template>
  
  
<script>
import axios from 'axios';
export default {
  data() {
    return {
      examples: [
        { title: '文本证据 📖', description: '本案件的文字性证据' },
        { title: '图片证据 📷', description: '本案件的图片证据' },
      ],
      dialog: false,
      currentExample: {},
      caseData: {
        案件类型: '',
        基本案情: '',
        原告: {
          事实证据: [],
          个人情况: [],
          诉讼请求: []
        },
        被告: {
          个人情况: []
        }
      },
      imageFiles: [],
      imagePreviews: [],
      imageDescription: ''
    }
  },
  watch: {
    imageFiles(newFiles) {
      this.imagePreviews = [];

      if (!newFiles || newFiles.length === 0) return;

      newFiles.forEach(file => {
        const reader = new FileReader();
        reader.onload = (e) => {
          this.imagePreviews.push({
            url: e.target.result,
            name: file.name
          });
        };
        reader.readAsDataURL(file);
      });
    }
  },
  methods: {
    upload(example) {
      this.currentExample = example;
      this.dialog = true;
    },

    removeImage(index) {
      this.imagePreviews.splice(index, 1);
      this.imageFiles.splice(index, 1); // 直接修改 imageFiles 数组
    },

    submitUpload() {
      if (this.currentExample.title === '图片证据 📷') {
        // 创建 FormData 对象用于文件上传
        const formData = new FormData();
        this.imageFiles.forEach((file) => {
          formData.append('images', file);
        });
        formData.append('description', this.imageDescription);

        // 使用 axios 发送 POST 请求，将数据发送到后端
        axios.post('http://localhost:5000/api/uploadImages', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        .then(() => { // 移除了 response 参数
          console.log('图片数据已成功发送到服务器');
          // 根据需要，可以在这里添加提示用户的逻辑
        })
        .catch(error => {
          console.error('发送图片数据时出错:', error);
          // 根据需要，处理错误情况
        });

        // 重置表单
        this.imageFiles = [];
        this.imagePreviews = [];
        this.imageDescription = '';
      } else {
        // 构建JSON对象
        const jsonData = {
          案件类型: this.caseData.案件类型,
          基本案情: this.caseData.基本案情,
          原告: {
            事实证据: this.caseData.原告.事实证据,
            个人情况: this.caseData.原告.个人情况,
            诉讼请求: this.caseData.原告.诉讼请求
          },
          被告: {
            个人情况: this.caseData.被告.个人情况
          }
        };

        // 使用 axios 发送 POST 请求，将数据发送到后端
        axios.post('http://localhost:5000/api/saveCaseData', jsonData)
          .then(() => { // 移除了 response 参数
            console.log('案件数据已成功发送到服务器');
            // 根据需要，可以在这里添加提示用户的逻辑
          })
          .catch(error => {
            console.error('发送案件数据时出错:', error);
            // 根据需要，处理错误情况
          });

        // 重置表单
        this.caseData = {
          案件类型: '',
          基本案情: '',
          原告: {
            事实证据: [],
            个人情况: [],
            诉讼请求: []
          },
          被告: {
            个人情况: []
          }
        };
      }
      this.dialog = false;
    }
  }
}

</script>

<style scoped>
.example-cards .v-card {
  /* 添加3D效果 */
  transform: perspective(1000px) rotateY(10deg);
  /* 设置圆角 */
  border-radius: 20px;
  /* 为了更好地展示3D效果，给卡片添加阴影 */
  box-shadow: 5px 5px 15px rgba(0,0,0,0.3);
}
.example-cards {
  margin-top: 400px; /* 或者根据你的设计需求调整 */
}

.preview-card {
  position: relative;
}

.remove-image {
  position: absolute;
  top: 4px;
  right: 4px;
  background: rgba(255, 255, 255, 0.8);
}

.preview-card .v-card__text {
  padding: 8px;
  font-size: 12px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
  .fixed-bottom {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
  }
  
  @media (min-width: 200px) {
    .fixed-bottom {
      left: 50%;
      transform: translateX(-50%);
    }
  }
  </style>
  