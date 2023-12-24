import requests
import os

from dotenv import load_dotenv

load_dotenv()

SERVICE_KEY = os.environ.get("SERVICE_KEY")

api_url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst"

# 관측 위치 : 서울특별시 강남구 개포2동
# 당일 새벽 2시에 발표된 예보를 기준으로 최저기온, 최고기온 정보를 가져옵니다.
params = {
    'serviceKey': SERVICE_KEY,
    'numOfRows': '10',
    'dataType': 'JSON',
    'base_time': '0200',
    'nx': '62',
    'ny': '125',
}

'''
category: 예보 항목
- TMN : 최저 기온 - 오전 6시 
- TMX : 최고 기온 - 오후 3시 
- SKY : 하늘 상태
- PTY : 강수 형태
'''
def fetch_data_from_kma(current_time_kst, page_no, category, fcst_time):
    try:
        date_format = "YYYYMMDD"
        base_date = current_time_kst.format(date_format)
        params['base_date'] = base_date
        params['pageNo'] = page_no

        response = requests.get(api_url, params=params)
        response.raise_for_status()
        data = response.json()

        items = data['response']['body']['items']['item']
        found = next(filter(lambda x: x['category'] == category and x['fcstTime'] == fcst_time, items), None)

        if (found):
            return found['fcstValue']
        else:
            return None

    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Something went wrong: {err}")

    return None
