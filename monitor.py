import feedparser
import requests
import os
from datetime import datetime

WEBHOOK = os.getenv('DINGTALK_WEBHOOK')

RSS_FEEDS = {
    "aleabitoreddit": "https://rss.app/r/feed/dCRFqvMPbt99MRjT",
    "thankUcrypto": "https://rss.app/feeds/ELLWvZlaubXflZWJ.xml",
    "Jackyi_ld": "https://rss.app/r/feed/dTjMDQsSRBVOEruA",
    "0xcryptowizard": "https://rss.app/r/feed/4KIACkEKXR1H2QjT",
    "superexvip": "https://rss.app/r/feed/9E2kPstowBAWbmDc"
}

seen = set()

def send_to_dingtalk(user, title, link, summary):
    text = f"X 新推文！\n\n账号：@{user}\n时间：{datetime.now().strftime('%m-%d %H:%M')}\n\n{title}\n\n{summary[:280]}...\n\n🔗 {link}"
    data = {"msgtype": "text", "text": {"content": text}}
    try:
        requests.post(WEBHOOK, json=data, timeout=10)
        print(f"✅ 推送 @{user}")
    except:
        print(f"❌ 推送失败 @{user}")

print("=== X 推文监控启动（仅本人推文） ===")

for username, rss_url in RSS_FEEDS.items():
    print(f"检查 @{username}")
    try:
        feed = feedparser.parse(rss_url)
        for entry in feed.entries[:5]:
            title = entry.title or ""
            link = entry.link
            summary = entry.get('description') or entry.get('summary') or ""
            post_id = entry.get('id') or link
            
            # 重要过滤：只保留该账号自己发的推文（排除别人@的）
            if username.lower() not in title.lower() and username.lower() not in summary.lower():
                continue
                
            if post_id and post_id not in seen:
                seen.add(post_id)
                send_to_dingtalk(username, title, link, summary)
                print(f"发现 @{username} 本人新推文")
    except Exception as e:
        print(f"@{username} 检查出错: {e}")

print("本轮检查完成")
