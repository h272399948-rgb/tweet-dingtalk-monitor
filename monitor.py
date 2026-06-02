import requests
import time
import os
from datetime import datetime

# ================== 配置区 ==================
DINGTALK_WEBHOOK = os.getenv("DINGTALK_WEBHOOK")  

# 要监控的 X（Twitter）用户名，多个用逗号分隔
X_USERS = ["elonmusk", "xAI", "OpenAI"]  

last_tweet_ids = {}

def send_to_dingtalk(text):
    if not DINGTALK_WEBHOOK:
        print("钉钉 Webhook 未设置")
        return
    data = {
        "msgtype": "markdown",
        "markdown": {
            "title": "X 新推文提醒",
            "text": text
        }
    }
    try:
        requests.post(DINGTALK_WEBHOOK, json=data, timeout=10)
        print(f"[{datetime.now()}] 已推送到钉钉")
    except Exception as e:
        print("推送失败:", e)

print(f"[{datetime.now()}] 推文监控已启动，正在监控: {X_USERS}")

# 简单监控循环
while True:
    for user in X_USERS:
        try:
            # 使用公开可用的方式获取最新推文（实际可替换更好 API）
            url = f"https://syndication.twitter.com/srv/timeline-profile/screen_name/{user}"
            # 这里简化处理，实际部署推荐用第三方 API
            print(f"检查用户 {user} ...")
            # 占位，后面可完善
        except:
            pass
    time.sleep(300)  # 每 5 分钟检查一次
