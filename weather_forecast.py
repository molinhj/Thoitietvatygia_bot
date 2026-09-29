import requests

def get_thoitiet(place='Hue'):
    try:
        api_key = '8e52e86b0eff70a88156a7eaff841fd3'
        url = f'https://api.openweathermap.org/data/2.5/weather?q={place}&appid={api_key}&units=metric&lang=vi'
        respone = requests.get(url)
        data = respone.json()

        if data.get('cod') == 200:
            temp = data['main']['temp']
            humid= data['main']['humidity']
            description = data['weather'][0]['description']
            return f"🌤 **THỜI TIẾT {place.upper()}**\n- Trạng thái: {description}\n- Nhiệt độ: {temp}°C\n- Độ ẩm: {humid}%"
        else:
            return "❌ Không tìm thấy thông tin thời tiết địa điểm này."

    except Exception as e:
        return f"❌ Lỗi lấy thời tiết: {e}"
import time

while True:
    time.sleep(3600)

