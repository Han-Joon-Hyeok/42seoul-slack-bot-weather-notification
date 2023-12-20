import os

import arrow
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# 환경 변수에서 Slack 토큰을 로드
load_dotenv()

SLACK_TOKEN = os.environ.get("SLACK_TOKEN")
SLACK_CHANNEL = os.environ.get("SLACK_CHANNEL") # 여기에 메시지를 보낼 Slack 채널 이름을 입력하세요.

def send_slack_message(message):
    try:
        client = WebClient(token=SLACK_TOKEN)
        client.chat_postMessage(channel=SLACK_CHANNEL, text=message)
    except SlackApiError as e:
        print(f"Error sending message: {e}")

def main():
    # 현재 날짜 (KST 기준)
    current_time_kst = arrow.now('Asia/Seoul')
    date_of_today = current_time_kst.format("YYYY년 MM월 DD일")
    
    # 메시지 제목
    header = f"*[{date_of_today} 인증 스레드]*"

    # 슬랙 채널에 전송
    send_slack_message(header)

if __name__ == "__main__":
    main()