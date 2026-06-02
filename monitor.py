import feedparser
import requests
import os
from datetime import datetime

# ================== 配置区 ==================
WEBHOOK = os.getenv('DINGTALK_WEBHOOK')

USERS = ["aleabitoreddit", "thankUcrypto", "Jackyi_ld", "0xcryptowizard", "superexvip"]

# 推荐使用 rss.app（更稳定），请替换成你自己的RSS链接
RSS_BASE = "https://rss.app/feeds/"   # ← 如果你有rss.app账号可以改成你的

seen = set()   # 防止重复推送
# ===========================================

def send_to_dingtalk(user, title, link, summary):
    text = f"X 新推文！\n\n账号：@{user}\n时间：{datetime.now().strftime('%m-%d %H:%M')}\n\n标题：{title}\n\n摘要：{summary[:280]}...\n\n🔗 链接：{link}"
    
    data = {
        "msgtype": "text",
        "text": {"content": text}
    }
    try:
        requests.post(WEBHOOK, json=data, timeout=10)
        print(f"✅ 已推送 @{user} 的推文")
    except:
        print(f"❌ 推送失败 @{user}")

for username in USERS:
    # 使用 RSSHub（免费公开服务）
    rss_url = f"https://rsshub.app/twitter/user/{username}"
    print(f"正在检查 @{username}")
    
    feed = feedparser.parse(rss_url)
    
    for entry in feed.entries[:2]:      # 每次最多取最新2条
        post_id = entry.get('id') or entry.link
        if post_id not in seen:
            seen.add(post_id)
            title = entry.title or "无标题"
            summary = entry.description or entry.summary or "无内容"
            link = entry.link
            send_to_dingtalk(username, title, link, summary)
