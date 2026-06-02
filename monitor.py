import requests
import os
from datetime import datetime

print("="*50)
print(f"[{datetime.now()}] 调试信息开始")
print(f"DINGTALK_WEBHOOK 是否存在: {'是' if os.getenv('DINGTALK_WEBHOOK') else '否 ❌'}")

webhook = os.getenv("DINGTALK_WEBHOOK")
if webhook:
    print(f"Webhook 长度: {len(webhook)}")
    print(f"Webhook 开头: {webhook[:60]}...")
else:
    print("❌ 未读取到 DINGTALK_WEBHOOK，请检查 Secrets 设置")

# 测试推送
if webhook:
    data = {
        "msgtype": "text",
        "text": {
            "content": f"🧪 GitHub Actions 测试推送\n时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n如果看到这条消息，说明配置成功！"
        }
    }
    try:
        r = requests.post(webhook, json=data, timeout=10)
        print(f"推送状态码: {r.status_code}")
        print(f"返回内容: {r.text}")
        if r.status_code == 200:
            print("✅ 推送请求已发送成功")
        else:
            print("❌ 推送失败")
    except Exception as e:
        print("❌ 请求异常:", e)
else:
    print("跳过推送")

print("调试结束")
print("="*50)
