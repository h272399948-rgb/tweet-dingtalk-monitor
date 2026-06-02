import requests
import os
from datetime import datetime

WEBHOOK = os.getenv('DINGTALK_WEBHOOK')

USERS = ["aleabitoreddit", "thankUcrypto", "Jackyi_ld", "0xcryptowizard", "superexvip"]

def send_to_dingtalk(text):
    data = {"msgtype": "text", "text": {"content": text}}
    try:
        requests.post(WEBHOOK, json=data, timeout=10)
        print("✅ 推送成功")
    except Exception as e:
        print("❌ 推送失败", e)

print("=== X 监控启动 - 每轮报告 ===")

for username in USERS:
    text = f"X 监控报告\n@{username} 已检查\n时间：{datetime.now().strftime('%m-%d %H:%M:%S')}\n\n（当前RSS服务暂未抓到新推文，正在持续监控中...）"
    send_to_dingtalk(text)

print("本轮检查完成")
