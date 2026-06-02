import feedparser
import requests
import os
from datetime import datetime
import re

WEBHOOK = os.getenv('DINGTALK_WEBHOOK')

RSS_FEEDS = {
    "aleabitoreddit": "https://rss.app/r/feed/dCRFqvMPbt99MRjT",
    "thankUcrypto": "https://rss.app/feeds/ELLWvZlaubXflZWJ.xml",
    "Jackyi_ld": "https://rss.app/r/feed/dTjMDQsSRBVOEruA",
    "0xcryptowizard": "https://rss.app/r/feed/4KIACkEKXR1H2QjT",
    "superexvip": "https://rss.app/r/feed/9E2kPstowBAWbmDc"
}

seen = set()

def clean_text(text):
    """清理HTML标签"""
    if not text:
        return ""
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def send_to_dingtalk(user, title, link, summary):
    clean_summary = clean_text(summary)
    text = f"X 新推文！\n\n账号：@{user}\n时间：{datetime.now().strftime('%m-%d %H:%M')}\n\n{clean_summary}\n\n🔗 {link}"
    data = {"msgtype": "text", "text": {"content": text}}
    try:
        requests.post(WEBHOOK, json=data, timeout=10)
        print(f"✅ 推送 @{user}")
    except:
        print(f"❌ 推送失败 @{user}")

print("=== X 推文监控启动（严格过滤本人推文） ===")

for username, rss_url in RSS_FEEDS.items():
    print(f"检查 @{username}")
    try:
        feed = feedparser.parse(rss_url)
        for entry in feed.entries[:5]:
            link = entry.link or ""
            title = entry.title or ""
            summary = entry.get('description') or entry.get('summary') or ""
            
            post_id = entry.get('id') or link
            
            # 严格过滤：只保留该账号自己发的推文
            if not link or f"/{username}/status/" not in link.lower():
                continue
                
            if post_id and post_id not in seen:
                seen.add(post_id)
                send_to_dingtalk(username, title, link, summary)
                print(f"发现 @{username} 本人新推文")
    except Exception as e:
        print(f"@{username} 检查出错: {e}")

print("本轮检查完成")
