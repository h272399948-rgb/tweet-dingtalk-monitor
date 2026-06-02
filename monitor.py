import feedparser
import requests
import os
from datetime import datetime

WEBHOOK = os.getenv('DINGTALK_WEBHOOK')

USERS = ["aleabitoreddit", "thankUcrypto", "Jackyi_ld", "0xcryptowizard", "superexvip"]

seen = set()

def send_to_dingtalk(user, title, link, summary):
    text = f"X 新推文！\n\n账号：@{user}\n时间：{datetime.now().strftime('%m-%d %H:%M')}\n\n{title}\n\n{summary[:280]}...\n\n🔗 {link}"
    data = {"msgtype": "text", "text": {"content": text}}
    try:
        requests.post(WEBHOOK, json=data, timeout=10)
        print(f"✅ 推送 @{user}")
    except:
        print(f"❌ 推送失败 @{user}")

print("=== X 推文监控启动（每5分钟） ===")

for username in USERS:
    print(f"检查 @{username}")
    rss_url = f"https://rsshub.app/twitter/user/{username}"
    
    try:
        feed = feedparser.parse(rss_url)
        for entry in feed.entries[:3]:
            post_id = entry.get('id') or entry.link
            if post_id and post_id not in seen:
                seen.add(post_id)
                title = entry.title or "无标题"
                summary = entry.get('description') or entry.get('summary') or "无内容"
                link = entry.link
                send_to_dingtalk(username, title, link, summary)
                print(f"发现新推文 @{username}")
    except Exception as e:
        print(f"@{username} 检查出错: {e}")

print("本轮检查完成")
