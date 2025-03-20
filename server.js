const fs = require('fs');
const path = require('path');
const WebSocket = require('ws');

const filePath = path.join(__dirname, 'agentscope', 'runs', 'TEST', 'logging.chat');
let lastSize = 0;

// 创建 WebSocket 服务器，使用3000端口
const wss = new WebSocket.Server({ port: 3000 });

// 读取文件新内容的函数
function readNewContent(ws, currentSize) {
  fs.readFile(filePath, 'utf8', (err, data) => {
    if (err) {
      console.error('读取文件失败:', err);
      return;
    }

    // 只获取新增的内容
    const newContent = data.slice(lastSize);
    if (newContent) {
      console.log('发送新内容:', newContent);
      ws.send(newContent);
      lastSize = data.length;
    }
  });
}

wss.on('connection', (ws) => {
  console.log('客户端已连接');

  // 首先发送现有的文件内容
  fs.readFile(filePath, 'utf8', (err, data) => {
    if (err) {
      console.error('读取文件失败:', err);
      return;
    }
    
    if (data) {
      console.log('发送初始内容');
      ws.send(data);
      lastSize = data.length;
    }

    // 使用 watchFile 替代 watch，监控文件大小变化
    fs.watchFile(filePath, { interval: 1000 }, (curr, prev) => {
      if (curr.size > lastSize) {
        console.log('检测到文件变化');
        readNewContent(ws, lastSize);
      }
    });
  });

  // 当连接关闭时，停止监听文件
  ws.on('close', () => {
    console.log('客户端断开连接');
    fs.unwatchFile(filePath);
    //清空data
    lastSize = 0;
    fs.writeFileSync(filePath, '');
  });
});

console.log('WebSocket 服务器已在端口3000上运行');