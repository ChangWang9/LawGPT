# Law GPT - 智能法律咨询系统

这是一个基于Vue 3和Flask的智能法律咨询系统，提供实时对话和案件分析功能。

## 技术栈

### 前端

- Vue 3
- Vuetify 3
- Vue Router
- WebSocket
- Axios

### 后端

- Flask
- WebSocket Server
- Flask-CORS

## 项目结构

```
law_gpt/
├── src/                # Vue前端源代码
├── public/            # 静态资源
├── server.js          # WebSocket服务器
├── app.py            # Flask后端服务
├── agentscope/       # 智能代理相关代码
└── data/             # 数据存储目录
```

## 安装说明

1. 克隆项目

```bash
git clone [项目地址]
cd law_gpt
```

2. 安装前端依赖

```bash
npm install
# 或
yarn install
```

3. 安装后端依赖

```bash
pip install flask flask-cors
```

## 运行项目

1. 启动WebSocket服务器

```bash
node server.js
```

2. 启动Flask后端服务

```bash
python app.py
```

3. 启动Vue开发服务器

```bash
npm run serve
# 或
yarn serve
```

## 功能特点

- 实时对话：通过WebSocket实现与AI的实时对话
- 案件分析：支持上传案件相关图片和描述
- 数据持久化：自动保存对话历史和案件数据
- 响应式设计：适配多种设备尺寸

## API接口

### 后端API

- POST `/api/saveCaseData`: 保存案件数据
- POST `/api/uploadImages`: 上传案件相关图片

### WebSocket

- 端口：3000
- 功能：实时传输对话内容

## 开发说明

- 前端开发端口：默认8080
- 后端API端口：5000
- WebSocket端口：3000

## 注意事项

1. 确保所有依赖包都已正确安装
2. 运行前请确保所需端口未被占用
3. 建议使用Node.js 14+和Python 3.7+版本

## 许可证

ISC License
