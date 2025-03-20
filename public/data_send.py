import json
import time
from pathlib import Path

def send_messages():
    # 读取原始数据
    messages = []
    with open('public/data.txt', 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                messages.append(json.loads(line))
    
    # 读取现有的logging.chat内容
    existing_messages = []
    chat_file = Path('public/logging.chat')
    if chat_file.exists():
        with open(chat_file, 'r', encoding='utf-8') as f:
            existing_messages = [line.strip() for line in f if line.strip()]
    
    # 只追加新消息
    for msg in messages:
        with open('public/logging.chat', 'a', encoding='utf-8') as f:
            f.write(json.dumps(msg, ensure_ascii=False) + '\n')
        print(f"已发送消息: {msg['name']} - {msg['content'][:30]}...")
        time.sleep(4)  # 每条消息间隔4秒

if __name__ == '__main__':
    try:
        send_messages()
    except KeyboardInterrupt:
        print("\n程序已停止")
    except Exception as e:
        print(f"发生错误: {e}")