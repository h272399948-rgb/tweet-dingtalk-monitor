import requests
import os
import time
import hmac
import hashlib
import base64
from datetime import datetime
from urllib.parse import quote_plus

DINGTALK_WEBHOOK = os.getenv("DINGTALK_WEBHOOK")
DINGTALK_SECRET = os.getenv("DINGTALK_SECRET", "")   # 加签密钥（可选）

print(f"[{datetime.now()}] 🚀 监控脚本启动")

def send_to_dingtalk(text):
    if not DINGTALK_WEBHOOK:
        print("❌ 未设置 DINGTALK_WEBHOOK")
        return False
    
    timestamp = str(round(time.time() * 1000))
    sign = ""
    
    # 如果开启了加签，计算签名
    if DINGTALK_SECRET:
        secret = DINGTALK_SECRET
        string_to_sign = f'{timestamp}\n{secret}'
        hmac_code = hmac.new(secret.encode('utf-8'), string_to_sign.encode('utf-8'), digestmod=hashlib.sha256).digest()
        sign = quote_plus(base64.b64encode(hmac_code))
        url = f"{DINGTALK_WEBHOOK}&timestamp={timestamp}&sign={sign}"
    else:
        url = DINGTALK_WEBHOOK
    
    data = {
        "msgtype": "markdown",
        "markdown": {
            "title": "X 新推文提醒",
            "text": text
        }
    }
    
    try:
        r = requests.post(url, json=data, timeout=10)
        print(f"推送状态码: {r.status_code}")
        print(f"返回: {r.text}")
        if r.status_code == 200:
            print("✅ 推送成功！")
            return True
    except Exception as e:
        print("❌ 推送异常:", e)
    return False

# 测试消息
test_msg = f"**GitHub Actions 测试**\n\n加签模式测试推送\n时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n配置成功！"

send_to_dingtalk(test_msg)
print("测试完成")
