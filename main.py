import datetime
import os

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
    # 현재 날짜와 요일 가져오기
    now = datetime.datetime.now()
    weekdays = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]
    weekday_str = weekdays[now.weekday()]
    # 메시지 포맷에 요일 추가
    today = now.strftime("%m월 %d일")
    message = f"[{today} {weekday_str} 인증 스레드]"
    send_slack_message(message)

if __name__ == "__main__":
    main()