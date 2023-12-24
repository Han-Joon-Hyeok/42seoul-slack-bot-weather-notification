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

STATUS_OF_SKY = {
    '1': '맑음 ☀️',
    '3': '구름많음 ☁️',
    '4': '흐림 ⛅️',
}

STATUS_OF_PRECIPITATION = {
    '0': '없음',
    '1': '비 🌧️',
    '2': '비/눈 🌨️',
    '3': '눈 ❄️',
    '4': '소나기 ☔️'
}

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
    sky = weather.fetch_data_from_kma(current_time_kst, '3', 'SKY', '0500')
    precipitation = weather.fetch_data_from_kma(current_time_kst, '4', 'PTY', '0500')
    lowest_temp_of_today = weather.fetch_data_from_kma(current_time_kst, '5', 'TMN', '0600')
    highest_temp_of_today = weather.fetch_data_from_kma(current_time_kst, '16', 'TMX', '1500')

    if (sky == None or precipitation == None or 
        lowest_temp_of_today == None or highest_temp_of_today == None):
        weather_msg = "날씨 정보를 가져오지 못했습니다. 😢"
    else:
        weather_of_today = f"{STATUS_OF_SKY[sky]} (강수: {STATUS_OF_PRECIPITATION[precipitation]})"
        weather_msg = (
            f"🌏 현재 날씨: {weather_of_today}\n"
            f"🔼 최고 기온: {highest_temp_of_today}°C\n"
            f"🔽 최저 기온: {lowest_temp_of_today}°C\n"
            f"🔎 관측 지점: 서울 강남구 개포2동"
        )

    # 메시지 본문
    body = header + weather_msg

    # 슬랙 채널에 전송
    send_slack_message(body)

if __name__ == "__main__":
    main()