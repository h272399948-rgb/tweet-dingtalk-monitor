import feedparser
import requests
import os
import time
from datetime import datetime

# 你的钉钉 Webhook
WEBHOOK = os.getenv('DINGTALK_WEBHOOK') or "https://oapi.dingtalk.com/robot/send?access_token=b09f09ed791dfcdbd85523763ff091886966cc0fc50312781170ac63313ef78f"

USERS = ["aleabitoreddit", "thankUcrypto", "Jackyi_ld", "0xcryptowizard", "superexvip"]

# 记录已发送的推文ID，避免重复
seen = set()

def send_to_dingtalk(user, title, link, content):
    text = f"X 新推文！\n账号：@{user}\n标题：{title}\n内容：{content[:300]}...\n链接：{link}\n时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}"
    
    data = {
        "msgtype": "text",
        "text": {"content": text}
    }
    requests.post(WEBHOOK, json=data)

for username in USERS:
    # 使用 rss.app 或 rsshub（你可以换成自己生成的链接）
    rss_url = f"https://rss.app/feeds/你的rss.app链接在这里"  # ← 这里替换成实际RSS链接
    # 或者用 rsshub: f"https://rsshub.app/twitter/user/{username}"
    
    feed = feedparser.parse(rss_url)
    
    for entry in feed.entries[:3]:   # 每次检查最新3条
        post_id = entry.id or entry.link
        if post_id not in seen:
            seen.add(post_id)
            send_to_dingtalk(username, entry.title, entry.link, entry.description)
            time.sleep(1)  # 避免发送太快
