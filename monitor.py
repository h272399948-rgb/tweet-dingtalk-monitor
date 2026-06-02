import requests
import os
from datetime import datetime

WEBHOOK = os.getenv('DINGTALK_WEBHOOK')

USERS = ["aleabitoreddit", "thankUcrypto", "Jackyi_ld", "0xcryptowizard", "superexvip"]

def send_to_dingtalk(message):
    data = {"msgtype": "text", "text": {"content": message}}
    try:
        requests.post(WEBHOOK, json=data, timeout=10)
        print("✅ 推送成功")
    except Exception as e:
        print("❌ 推送失败:", e)

print("=== X 推文监控启动 ===")

for username in USERS:
    # 尝试 RSSHub
    rss_url = f"https://rsshub.app/twitter/user/{username}"
    print(f"检查 @{username}")
    
    try:
        # 这里我们先简化，只发一条测试性质的消息，后面再完善RSS
        send_to_dingtalk(f"X 监控测试\n@{username} 的监控已启动\n时间：{datetime.now().strftime('%m-%d %H:%M')}\n\n（RSS抓取中...）")
    except:
        pass

print("本轮检查完成")
