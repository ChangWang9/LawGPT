<template>

  <div class="chat-page-container">

    <div class="button-group">
    <!-- 庭前准备按钮与下拉菜单 -->
    <v-btn class="button" outlined>庭前准备</v-btn>
    <v-menu offset-y>
      <template v-slot:activator="{ on, attrs }">
        <v-btn class="button" color="primary" dark v-bind="attrs" v-on="on" outlined>法庭调查</v-btn>
      </template>
      <v-list>
        <v-list-item v-for="item in menuItems1" :key="item" @click="() => {}">
          <v-list-item-title>{{ item }}</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>

    <!-- 其他按钮可以按照类似的方式添加下拉菜单 -->

    <v-btn class="button" outlined>法庭辩论</v-btn>
    <v-btn class="button" outlined>最终判决</v-btn>
  </div>
    <div class="chat-container" ref = "chatContainer">
      <!-- 消息列表 -->
      <div class="messages">
        <div v-for="message in visibleMessages" :key="message.id" class="message-wrapper" :class="{'mine': message.mine}">
          <!-- 角色标签和头像 -->
          <div class="role-and-avatar" :class="{'mine': message.mine}">
            <img :src="message.avatar" alt="avatar" class="avatar">
          </div>
          <!-- 消息内容 -->
          <div class="message-content" :class="{'mine': message.mine}">
            <div class="sender-label">{{ message.sender }}</div>
            <div class="message" :class="{'mine': message.mine}">
              <span>{{ message.displayText }}</span>
            </div>
          </div>
        </div>
      </div>
      <!-- 消息输入 -->
      <div class="message-input">
        <v-text-field
          label="Type a message..."
          v-model="newMessage"
          @keyup.enter="sendMessage"
          outlined
        ><template v-slot:append-outer>
        <!-- 暂停按钮 -->
        <v-btn icon @click="pauseAction">
          <v-icon>mdi-pause</v-icon>
        </v-btn>
      </template>
      </v-text-field>
      </div>
    </div>
  </div>
</template>


<script>
export default {
  data() {
    return {
      menuItems1: ['选项 1', '选项 2', '选项 3'],
      messages: [],
      newMessage: '',
      currentLine: 0,
      isProcessing: false,
      ws: null
    };
  },
  computed: {
    visibleMessages() {
      return this.messages.filter(msg => msg.visible);
    }
  },
  methods: {    
    getAvatarByRole(name) {
      const avatarMap = {
        '审判长': require('@/assets/审判长.png'),
        '原告律师': require('@/assets/原告律师.png'),
        '原告': require('@/assets/原告.png'),
        '被告律师': require('@/assets/被告律师.png'),
        '被告': require('@/assets/被告.png'),
        '观点总结员': require('@/assets/观点总结员.png'),
      };
      return avatarMap[name] || require('@/assets/avatar.png');
    },

    async processNextMessage() {
      if (this.isProcessing || this.currentLine >= this.messages.length) {
        return;
      }

      this.isProcessing = true;
      const message = this.messages[this.currentLine];
      if (message) {
        message.visible = true;

        for (let i = 0; i <= message.fullText.length; i++) {
          if (message.displayText !== undefined) {
            message.displayText = message.fullText.slice(0, i);
            await new Promise(resolve => setTimeout(resolve, 50));
            this.$nextTick(() => {
              this.scrollToBottom();
            });
          }
        }

        this.currentLine++;
        this.isProcessing = false;

        if (this.currentLine < this.messages.length) {
          setTimeout(() => {
            this.processNextMessage();
          }, 1000);
        }
      }
    },

    initWebSocket() {
      try {
        this.ws = new WebSocket('ws://localhost:3000');
        
        this.ws.onmessage = (event) => {
          if (event.data) {
            const newLines = event.data.split('\n').filter(line => line.trim());
            newLines.forEach(line => {
              try {
                const msgData = JSON.parse(line);
                const newMessage = {
                  id: Date.now() + Math.random(), // 确保ID唯一
                  fullText: msgData.content || '',
                  displayText: '',
                  avatar: this.getAvatarByRole(msgData.name),
                  mine: false,
                  sender: msgData.name,
                  visible: false
                };
                this.$nextTick(() => {
                  this.messages.push(newMessage);
                  if (!this.isProcessing) {
                    this.processNextMessage();
                  }
                });
              } catch (error) {
                console.error('解析消息失败:', error, line);
              }
            });
          }
        };

        this.ws.onerror = (error) => {
          console.error('WebSocket 错误:', error);
        };

        this.ws.onclose = () => {
          console.log('WebSocket 连接已关闭');
          setTimeout(() => this.initWebSocket(), 3000);
        };
      } catch (error) {
        console.error('WebSocket 初始化失败:', error);
      }
    },

    sendMessage() {
      if (this.newMessage.trim()) {
        const newMessage = {
          id: Date.now(),
          fullText: this.newMessage,
          displayText: this.newMessage,
          avatar: require('@/assets/avatar.png'),
          mine: true,
          sender: '我',
          visible: true
        };
        this.messages.push(newMessage);
        this.newMessage = '';
        this.$nextTick(() => {
          this.scrollToBottom();
        });
      }
    },

    scrollToBottom() {
      if (this.$refs.chatContainer) {
        this.$refs.chatContainer.scrollTop = this.$refs.chatContainer.scrollHeight;
      }
    },

    pauseAction() {
      // 实现暂停功能
      console.log('暂停功能待实现');
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.initWebSocket();
    });
  },
  beforeUnmount() {
    if (this.ws) {
      this.ws.close();
    }
  }
};
</script>
<style scoped>
.chat-page-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh; /* 视窗高度 */
}

.chat-container {
  display: flex;
  flex-direction: column;
  width: 1200px;
  margin: 20px auto;
  border: 1px solid #ddd;
  padding: 16px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  background-color: #fff;
  overflow-y: auto;
  height: 86%;
}

.messages {
  flex-grow: 1;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
}

.message {
  display: flex;
  align-items: flex-start;
  
  margin-bottom: 32px;
  padding: 8px;
  background-color: #f0f0f0; /* 消息背景色 */
  border-radius: 20px; /* 消息圆角 */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05); /* 消息阴影 */
  word-wrap: break-word; /* 允许单词内换行 */
  max-width: 80%; /* 最大宽度为容器的80% */
}

.message.mine {
  align-items: flex-end;
  justify-content: flex-end; 
  margin-bottom: 32px;
  padding: 8px;
  background-color: #f0f0f0; /* 消息背景色 */
  border-radius: 20px; /* 消息圆角 */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05); /* 消息阴影 */
  word-wrap: break-word; /* 允许单词内换行 */
  max-width: 80%; /* 最大宽度为容器的80% */
}

.message-wrapper {
  display: flex;
  align-items: flex-start;
  justify-content: flex-start; 
  /* justify-content: flex-end; 默认将消息放在右侧 */
  margin-bottom: 10px; /* 增加间距 */
}

.message-wrapper.mine {
  display: flex;
  align-items: flex-start;
  justify-content: flex-end; /* 将“我的”消息放在左侧 */
  margin-bottom: 10px; /* 增加间距 */
  
}

.message-content {
  display: flex;
  flex-direction:column;
  justify-content: flex-start; 
  align-items: flex-start;
  /* 确保它的宽度和消息框一致，如果需要限制宽度，可以在这里设置 */
  flex: 1;
}
.message-content.mine {
  flex-direction:column;
  justify-content: flex-end; 
  align-items: flex-end;
  /* 确保它的宽度和消息框一致，如果需要限制宽度，可以在这里设置 */
}


.role-and-avatar {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 0 6px;
}
.role-and-avatar.mine {
  align-items: flex-start;
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 0 6px;
}



.mine {
  flex-direction: row-reverse; /* “我的”消息的背景色 */
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin: 0 8px;
  border: 0px solid #fff; /* 假设你想要一个白色的边框 */
   box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);/* 可选：为头像添加阴影，使其更加立体 */
}
.mine .avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin: 0 8px;
  border: 0px solid #fff; /* 假设你想要一个白色的边框 */
   box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);/* 可选：为头像添加阴影，使其更加立体 */
}

.message-input {
  margin-top: 16px;
}

.avatar-and-role {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-right: 8px; /* 头像和消息之间的间距 */
}

.role-label {
  margin-top: 4px;
  font-size: 12px;
}

.mine .avatar-and-role {
  display: flex-end;
  flex-direction: column;
  align-items: center;
  margin-right: 8px; /* 头像和消息之间的间距 */
}

.sender-label {
  /* 加粗字体*/
  font-weight: bold;
  font-size: 0.9em; /* 调整大小 */
  color: #333; /* 谁发送的消息的字体颜色 */
  margin-bottom: 4px; /* 在消息内容上方留出一些空间 */
  /*向右移动2px*/
  align-self: flex-start; /* 对齐到消息框的起始位置 */
}

.mine .sender-label { /* 如果是“我的”消息，对齐到消息框的末端位置 */
  font-weight: bold;
  font-size: 0.9em; /* 调整大小 */
  color: #333; /* 谁发送的消息的字体颜色 */
  margin-bottom: 4px; /* 在消息内容上方留出一些空间 */
  align-self: flex-end; /* 对齐到消息框的起始位置 */
  /*对齐到消息框的末端位置*/

}
.message > span {
  word-break: break-all; /* 针对长字符串进行强制换行 */
}
.button-group {
  display: flex;
  flex-direction: column;
  padding: 350px;
  margin-right: -600px; /* 与聊天容器的间距 */
}

.button {
  margin-bottom: 70px; /* 按钮之间的间距 */
  border-radius: 2500px; /* 圆角矩形形状 */
  font-size: 2.0em;
  /*按钮放大些*/
  padding: 30px 20px; /* 按钮内边距 */
    /*字放在按钮正中间*/
  display: flex; /* 使用flexbox布局 */
  justify-content: center; /* 水平居中 */
  align-items: center; /* 垂直居中 */
  text-align: center; /* 文本居中对齐 */
  width: fit-content; /* 按钮宽度适应内容 */
}

</style>
