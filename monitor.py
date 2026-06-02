import requests
import os
from datetime import datetime

DINGTALK_WEBHOOK = os.getenv("DINGTALK_WEBHOOK")

print(f"[{datetime.now()}] 🚀 测试脚本启动")

if not DINGTALK_WEBHOOK:
    print("❌ 未找到 DINGTALK_WEBHOOK")
else:
    data = {
        "msgtype": "markdown",
        "markdown": {
            "title": "✅ 测试成功！",
            "text": f"**GitHub Actions 监控脚本测试成功**\n\n当前时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n这是第一条测试消息，证明钉钉推送正常。\n\n后续会添加真实推文监控。"
        }
    }
    r = requests.post(DINGTALK_WEBHOOK, json=data)
    print("推送状态码:", r.status_code)
    if r.status_code == 200:
        print("✅ 钉钉推送成功！")
    else:
        print("❌ 推送失败", r.text)
