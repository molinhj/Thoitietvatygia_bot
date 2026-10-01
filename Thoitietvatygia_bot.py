import requests
import schedule
import time
import os
from flask import Flask
from threading import Thread

# TẠO WEB SERVER NHẸ
app = Flask(__name__)


@app.route('/')
def home():
    return 'Bot dang chay ngon lanh', 200


def run():
    # Render sẽ tự cấp cổng PORT vào môi trường, nếu không có sẽ dùng 8080
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# Chạy web server ẩn trên một luồng riêng để trả lời Render
Thread(target=run).start()

from dotenv import load_dotenv

# Import các hàm từ file riêng của bạn
import moneyexchanging
import weather_forecast
from gold_price import get_gold_price
from gold_price import check_gold_price

load_dotenv()

tele_token = os.getenv('tele_token')
my_chat_id = os.getenv('my_chat_id')




# HÀM GỬI TIN NHẮN ĐẾN TELEGRAM
def send_telegram_message(chat_id, text):
    url = f'https://api.telegram.org/bot{tele_token}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'Markdown'
    }
    try:
        response = requests.post(url, json=payload)
        print("Mã phản hồi:", response.status_code)
    except Exception as e:
        print("Lỗi gửi tin nhắn:", e)


# LỆNH GỬI BÁO CÁO TỰ ĐỘNG
def send_report():
    print('Dang tong hop thong tin...')
    tygia_msg = moneyexchanging.get_tygia()
    thoitiet_msg = weather_forecast.get_thoitiet()
    gold_msg = get_gold_price()

    message_content = f"* BÁO CÁO MỖI NGÀY *\n\n{tygia_msg}\n\n{thoitiet_msg}\n\n{gold_msg}"
    send_telegram_message(my_chat_id, message_content)
    print("Da gui bao cao thanh cong ve telegram!")


# HÀM KIỂM TRA VÀ XỬ LÝ TIN NHẮN ĐẾN
def check_tele_message():
    last_update_id = 0
    print("Đang lắng nghe tin nhắn Telegram...")
    while True:
        try:
            url = f'https://api.telegram.org/bot{tele_token}/getUpdates?offset={last_update_id + 1}&timeout=30'
            response = requests.get(url).json()


            for result in response.get('result', []):
                last_update_id = result['update_id']
                message = result.get('message', {})
                text = message.get('text', '')
                chat_id = message.get('chat', {}).get('id')

                if not chat_id:
                    continue

                # KIỂM TRA VÀ XỬ LÝ LỆNH
                if text == '/start':
                    send_telegram_message(chat_id, 'Xin chào! Gõ /tygia, /thoitiet hoặc /giavang để xem thông tin.')
                elif text == '/tygia':
                    msg = moneyexchanging.get_tygia()
                    send_telegram_message(chat_id, msg)
                elif text.startswith('/thoitiet'):
                    part = text.split(maxsplit=1)
                    if len(part) > 1:
                        place = part[1]
                    else:
                        place = 'Hue'
                    msg = weather_forecast.get_thoitiet(place)
                    send_telegram_message(chat_id, msg)
                elif text == '/giavang':
                    msg = get_gold_price()
                    send_telegram_message(chat_id, msg)

        except Exception as e:
            print('Lỗi nhận tin nhắn:', e)
        time.sleep(1)
def auto_check_price():
    msg =  check_gold_price()
    if msg:
        chat_id = my_chat_id
        send_telegram_message(chat_id,msg)



# CHƯƠNG TRÌNH CHÍNH
if __name__ == '__main__':
    # Chạy Web Server ngầm
    threading.Thread(target=run, daemon=True).start()

    # Chạy hàm lắng nghe tin nhắn ngầm
    threading.Thread(target=check_tele_message, daemon=True).start()

    # Lên lịch gửi báo cáo lúc 07:00 sáng
    schedule.every().day.at('07:00').do(send_report)
    print('Bot da khoi dong va dang cho den 07:00 sang mai')

    # Khai báo lịch chạy trước
    schedule.every(15).minutes.do(auto_check_price)

    # Vòng lặp duy trì chạy liên tục ở cuối cùng
    while True:
        schedule.run_pending()
        time.sleep(60)

