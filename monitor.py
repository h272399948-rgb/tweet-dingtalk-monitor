import feedparser
import requests
import os
from datetime import datetime

WEBHOOK = os.getenv('DINGTALK_WEBHOOK')

USERS = ["aleabitoreddit", "thankUcrypto", "Jackyi_ld", "0xcryptowizard", "superexvip"]

seen = set()

def send_to_dingtalk(user, title, link, summary):
    text = f"X 新推文！\n\n账号：@{user}\n时间：{datetime.now().strftime('%m-%d %H:%M')}\n\n{title}\n\n{summary[:250]}...\n\n🔗 {link}"
    data = {"msgtype": "text", "text": {"content": text}}
    try:
        requests.post(WEBHOOK, json=data, timeout=10)
        print(f"✅ 推送 @{user}")
    except:
        print(f"❌ 推送失败 @{user}")

print("=== X 推文监控启动（多源备用） ===")

for username in USERS:
    print(f"检查 @{username}")
    found = False
    
    # 尝试多个 RSS 来源
    sources = [
        f"https://rsshub.app/twitter/user/{username}",
        f"https://rss.app/feeds/rss?user={username}",   # 备用
    ]
    
    for rss_url in sources:
        try:
            feed = feedparser.parse(rss_url)
            if feed.entries:
                for entry in feed.entries[:2]:
                    post_id = entry.get('id') or entry.link
                    if post_id not in seen:
                        seen.add(post_id)
                        title = entry.title or "无标题"
                        summary = entry.get('description') or entry.get('summary') or ""
                        link = entry.link
                        send_to_dingtalk(username, title, link, summary)
                        found = True
                if found:
                    break
        except:
            continue
    
    if not found:
        print(f"@{username} 当前暂无新内容")

print("本轮监控完成")
