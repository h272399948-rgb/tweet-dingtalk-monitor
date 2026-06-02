import feedparser
import requests
import os
from datetime import datetime

WEBHOOK = os.getenv('DINGTALK_WEBHOOK')

USERS = ["aleabitoreddit", "thankUcrypto", "Jackyi_ld", "0xcryptowizard", "superexvip"]

def send_to_dingtalk(user, title, link, summary):
    text = f"X 测试推送！@{user} 的最新动态\n\n{title}\n\n摘要：{summary[:200]}...\n\n🔗 {link}\n时间：{datetime.now().strftime('%m-%d %H:%M')}"
    
    data = {"msgtype": "text", "text": {"content": text}}
    try:
        requests.post(WEBHOOK, json=data, timeout=10)
        print(f"✅ 已推送 @{user}")
    except Exception as e:
        print(f"❌ 推送失败: {e}")

print("=== 开始强制测试推送 ===")

for username in USERS:
    rss_url = f"https://rsshub.app/twitter/user/{username}"
    print(f"检查 @{username} ...")
    feed = feedparser.parse(rss_url)
    
    if not feed.entries:
        print(f"❌ @{username} 没有抓到内容（RSS可能失效）")
        # 即使没内容也发一条测试
        send_to_dingtalk(username, "RSS抓取测试", f"https://x.com/{username}", "当前RSS服务可能不稳定，正在测试推送功能")
        continue
    
    for entry in feed.entries[:1]:
        title = entry.title or "无标题"
        summary = entry.get('description') or entry.get('summary') or "无内容"
        link = entry.link
        send_to_dingtalk(username, title, link, summary)
