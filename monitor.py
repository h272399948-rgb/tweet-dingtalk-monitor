import feedparser
import requests
import os
from datetime import datetime

WEBHOOK = os.getenv('DINGTALK_WEBHOOK')

USERS = [
    "aleabitoreddit",
    "thankUcrypto",
    "Jackyi_ld",
    "0xcryptowizard",
    "superexvip"
]

seen = set()

def send_to_dingtalk(user, title, link, summary):
    text = f"X 新推文！\n\n账号：@{user}\n时间：{datetime.now().strftime('%m-%d %H:%M')}\n\n{title}\n\n摘要：{summary[:280]}...\n\n🔗 {link}"
    
    data = {
        "msgtype": "text",
        "text": {"content": text}
    }
    try:
        requests.post(WEBHOOK, json=data, timeout=10)
        print(f"✅ 推送成功 @{user}")
    except Exception as e:
        print(f"❌ 推送失败 @{user}")

print("=== 开始监控5个账号 ===")

for username in USERS:
    # 使用 RSSHub（目前可用）
    rss_url = f"https://rsshub.app/twitter/user/{username}"
    print(f"正在检查 @{username}")
    
    feed = feedparser.parse(rss_url)
    
    if not feed.entries:
        print(f"@{username} 暂无内容")
        continue
    
    for entry in feed.entries[:2]:   # 每次取最新2条
        post_id = entry.get('id') or entry.link
        if post_id not in seen:
            seen.add(post_id)
            title = entry.title or "无标题"
            summary = entry.get('description') or entry.get('summary') or "无内容"
            link = entry.link
            send_to_dingtalk(username, title, link, summary)
