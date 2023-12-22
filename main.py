import os

import arrow
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

import weather

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
    date_format = "YYYY년 MM월 DD일 dddd"
    date_of_today = current_time_kst.format(date_format, locale="ko_kr")
    
    # 메시지 제목
    header = f"*[{date_of_today} 인증 스레드]*\n"

    # 날씨 정보
    weather_msg = ""
    response_json = weather.fetch_data_from_openweather_api()
    if (response_json == {}):
        weather_msg = "날씨 정보를 가져오지 못했습니다. 😢"
    else:
        weather_data = weather.parse_weather_data(response_json)
        weather_msg = f"오늘의 날씨: {weather_data['description']}\n- ⬇️최저 기온: {weather_data['min_temp']}°C\n- ⬆️최고 기온: {weather_data['max_temp']}°C\n- 💦습도: {weather_data['humidity']}%\n- 🌬️풍속: {weather_data['wind']}m/s\n- 🔎관측 지점: 서울 종로구"

    # 메시지 본문
    body = header + weather_msg

    # 슬랙 채널에 전송
    send_slack_message(body)

if __name__ == "__main__":
    main()