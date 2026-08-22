import requests
import schedule
import time
import os
from flask import Flask
import threading
from dotenv import load_dotenv
import moneyexchanging
import weather_forecast

load_dotenv()

tele_token = os.getenv('tele_token')
my_chat_id = os.getenv('my_chat_id')

#TAO WEB SEVER NHO
app = Flask(__name__)
@app.route('/')
def home():
    print('Bot dang chay ngon lanh'),200
def run():
    app.run(host='0.0.0.0', port=8080)

# LENH LAY DU LIEU TY GIA + THOI TIET
def exchangingrate():
    try:
        url = 'https://open.er-api.com/v6/latest/USD'
        respone = requests.get(url).json()
        rate = respone['rates']['VND']
        return f' TY GIA USD/VND - 1USD = {rate} VND'
    except Exception:
        return ' LOI KHONG LAY DUOC TY GIA '

def weatherforecast(city='Hue'):
    try:
        weather_api_key = '8e52e86b0eff70a88156a7eaff841fd3'
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric&lang=vi"
        respone = requests.get(url).json()
        if respone.get('cod') == 200:
            temp = respone['main']['temperature']
            humid = respone['main']['humidity']
            description = respone['weather'][0]['description']
        else:
            print('Dia diem may nhap deo ton tai. Nhap lai de')
    except Exception:
        return ' LOI KET NOI THOI TIET '
# HAM GUI TIN NHAN DEN MAY CHU
def send_telegram_message(chat_id,text):
    url = f'https://api.telegram.org/bot{tele_token}/sendMessage'
    payload = {
        'chat_id' : chat_id,
        'text': text,
        'parse_mode': 'Markdown'
    }
    response = requests.post(url,json=payload)
    print("Mã phản hồi:", response.status_code)
    print("Chi tiết:", response.json())
#LENH GUI BAO CAO
def send_report():
    print ('Dang tong hop thong tin...')
    message_content = f'* BAO CAO MOI NGAY *\n{exchangingrate()}\n{weatherforecast()}'
    my_chat_id = 8788964360
    send_telegram_message(my_chat_id, message_content)
    print("Da gui bao cao thanh cong ve telegram!")
# CHUONG TRINH CHINH
if __name__ == '__main__':
    def check_tele_message():
        last_update_id = 0
        while True:
            try:
                #GOI API TELEGRAM LAY TIN NHAN MOI
                url = f'https://api.telegram.org/bot{tele_token}/getUpdates?offset={last_update_id + 1}&timeout=30'
                respone = requests.get(url).json()
                for result in respone.get('result',[]):
                    last_update_id = result['update_id']
                    text = result.get('message',{}).get('text','')
                    chat_id = result.get('message',{}).get('chat',{}).get('id')
                #KIEM TRA TIN NHAN
                if text == '/tygia':
                    msg = moneyexchanging.get_tygia()
                    send_telegram_message(msg, chat_id)
                elif text == '/thoitiet':
                    msg = weather_forecast.get_thoitiet()
                    send_telegram_message(msg, chat_id)
            except Exception as e:
                print ('loi',e)
            threading.Thread(target=check_tele_message, daemon=True).start()
    threading.Thread(target=run, daemon=True).start()
    schedule.every().day.at('07:00').do(send_report)
    print('Bot da khoi dong va dang cho den 07:00 sang mai')
    while True:
        schedule.run_pending()
        time.sleep(60)

