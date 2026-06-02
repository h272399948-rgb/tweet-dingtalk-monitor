import requests
import time
import os
from datetime import datetime

# ================== 配置 ==================
DINGTALK_WEBHOOK = os.getenv("DINGTALK_WEBHOOK")

# 这里修改你要监控的账号（可多个）
X_USERS = ["aleabitoreddit", "thankUcrypto", "Jackyi_ld",  "0xcryptowizard","superexvip"]

last_tweet_ids = {}

def send_to_dingtalk(text):
    if not DINGTALK_WEBHOOK:
        print("❌ 钉钉 Webhook 未设置")
        return
    data = {
        "msgtype": "markdown",
        "markdown": {
            "title": "🔔 X 新推文提醒",
            "text": text
        }
    }
    try:
        requests.post(DINGTALK_WEBHOOK, json=data, timeout=10)
        print(f"✅ 已推送到钉钉")
    except Exception as e:
        print("❌ 钉钉推送失败:", e)

def get_latest_tweet(username):
    """使用免费第三方接口获取最新推文"""
    try:
        # 方法1：使用公开可用的接口（推荐）
        url = f"https://api.v2.rss.app/rss/100/twitter/{username}"
        r = requests.get(url, timeout=15)
        if r.status_code == 200:
            # 这里简化处理，实际可进一步解析
            print(f"✅ 检查 @{username} 成功")
            # 暂时用模拟数据测试（后面再优化）
            return {
                "id": int(time.time()),
                "text": f"这是 @{username} 的测试推文（实际部署后会显示真实内容）",
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
    except:
        pass
    return None

print(f"[{datetime.now()}] 🚀 推文监控启动 | 监控账号: {X_USERS}")

# 测试运行一次
for user in X_USERS:
    tweet = get_latest_tweet(user)
    if tweet:
        msg = f"**@{user}** 发布了新内容\n\n"
        msg += f"{tweet['text']}\n\n"
        msg += f"🕒 {tweet['created_at']}\n"
        msg += f"🔗 https://x.com/{user}"
        
        send_to_dingtalk(msg)

print("本次运行结束")
