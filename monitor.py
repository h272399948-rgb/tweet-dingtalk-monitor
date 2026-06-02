import requests
import os
from datetime import datetime

WEBHOOK = os.getenv('DINGTALK_WEBHOOK')

print("=== 开始测试 ===")
print("Webhook 长度:", len(WEBHOOK) if WEBHOOK else "空！")

if not WEBHOOK:
    print("❌ Webhook 未加载，请检查 Secrets")
else:
    text = f"X 钉钉测试消息 {datetime.now().strftime('%H:%M:%S')}\nGitHub Actions 正在测试推送功能"

    data = {
        "msgtype": "text",
        "text": {"content": text}
    }

    try:
        r = requests.post(WEBHOOK, json=data, timeout=15)
        print("状态码:", r.status_code)
        print("返回内容:", r.text)
        if r.status_code == 200:
            print("✅ 推送请求已发送，请检查钉钉")
        else:
            print("❌ 钉钉返回错误")
    except Exception as e:
        print("❌ 请求异常:", str(e))

print("=== 测试结束 ===")
