import requests
import os
import time
import hmac
import hashlib
import base64
from urllib.parse import quote_plus
from datetime import datetime

DINGTALK_WEBHOOK = os.getenv("DINGTALK_WEBHOOK")
DINGTALK_SECRET = os.getenv("DINGTALK_SECRET")

print(f"[{datetime.now()}] 调试开始")
print(f"Webhook 存在: {'是' if DINGTALK_WEBHOOK else '否'}")
print(f"Secret 存在: {'是' if DINGTALK_SECRET else '否'}")
print(f"Secret 内容: {DINGTALK_SECRET}")

def send_dingtalk():
    if not DINGTALK_WEBHOOK:
        print("❌ 没有 Webhook")
        return
    
    timestamp = str(round(time.time() * 1000))
    sign = ""
    
    if DINGTALK_SECRET:
        string_to_sign = f'{timestamp}\n{DINGTALK_SECRET}'
        hmac_code = hmac.new(DINGTALK_SECRET.encode('utf-8'), string_to_sign.encode('utf-8'), hashlib.sha256).digest()
        sign = quote_plus(base64.b64encode(hmac_code))
        url = f"{DINGTALK_WEBHOOK}&timestamp={timestamp}&sign={sign}"
        print("使用加签模式")
    else:
        url = DINGTALK_WEBHOOK
        print("普通模式")
    
    data = {
        "msgtype": "text",
        "text": {"content": f"🧪 测试推送 {datetime.now().strftime('%H:%M:%S')}\nGitHub Actions 配置测试\n如果看到这条，说明成功！"}
    }
    
    r = requests.post(url, json=data, timeout=10)
    print(f"状态码: {r.status_code}")
    print(f"返回: {r.text[:200]}")

send_dingtalk()
print("测试结束")
