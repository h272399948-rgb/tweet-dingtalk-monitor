import requests
import os
from datetime import datetime

DINGTALK_WEBHOOK = os.getenv("DINGTALK_WEBHOOK")

print(f"[{datetime.now()}] 测试开始")

if DINGTALK_WEBHOOK:
    data = {
        "msgtype": "markdown",
        "markdown": {
            "title": "X监控",
            "text": f"**X监控** 测试推送成功！\n\n时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n钉钉关键词过滤已通过 ✅"
        }
    }
    r = requests.post(DINGTALK_WEBHOOK, json=data)
    print(f"状态码: {r.status_code}")
    print(f"返回: {r.text}")
else:
    print("❌ 未找到 Webhook")
