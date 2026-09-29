import requests


def get_gold_price():
    url = 'https://giavang.com.vn/wp-json/giavang/v1/all'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }

    try:
        response = requests.get(url, headers=headers).json()

        sjc_prices = response.get('sjc', {}).get('prices', [])

        if sjc_prices:
            msg = "=== BẢNG GIÁ VÀNG HÔM NAY ===\n\n"
            for item in sjc_prices:
                name = item.get('name')
                buy = item.get('buy')
                sell = item.get('sell')
                msg += f"📌 {name}\n  - Mua vào: {buy:,.0f} VNĐ\n  - Bán ra: {sell:,.0f} VNĐ\n\n"
            return msg
        else:
            return "Không tìm thấy dữ liệu giá vàng."

    except Exception as e:
        return f"Lỗi kết nối API: {e}"


def get_one_gold_price():
    try:
        url = 'https://giavang.com.vn/wp-json/giavang/v1/all'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        }
        respone = requests.get(url, headers=headers)
        data = respone.json()  # SỬA 1: Phải đổi response sang JSON
        one_price = data.get('sjc', {}).get('prices', [])
        if one_price:
            return float(one_price[0].get('sell', 0))
    except Exception:
        pass
    return 0


def read_last_price():
    try:
        with open('gold_history.txt', 'r', encoding='utf-8') as f:
            line = f.readlines()
            if line:
                last_line = line[-1].strip()
                return float(last_line)
    except FileNotFoundError:
        return 0
    except Exception:
        return 0
    return 0


def save_price(one_price):
    try:
        with open('gold_history.txt', 'a', encoding='utf-8') as f:
            f.write(f"{one_price}\n")  # SỬA 2: Đưa số về dạng chữ và thêm \n
    except Exception as e:
        print(f'Loi ghi du lieu: {e}')


def check_gold_price():
    current_gold_price = get_one_gold_price()

    if current_gold_price == 0:
        return None

    # SỬA 3: Đọc giá cũ trực tiếp từ file thay vì dùng biến global
    previous_gold_price = read_last_price()

    if previous_gold_price == 0:
        save_price(current_gold_price)
        return None

    diff = current_gold_price - previous_gold_price

    if diff != 0:
        # Có biến động -> Ghi giá mới vào file
        save_price(current_gold_price)

        if diff > 0:
            return f'--GIA VANG TANG-- \nGia moi: {current_gold_price:,.0f} VNĐ\nTang: +{diff:,.0f} VNĐ'
        else:
            return f'--GIA VANG GIAM-- \nGia moi: {current_gold_price:,.0f} VNĐ\nGiam: {diff:,.0f} VNĐ'

    return None


# Đoạn này dùng để chạy test thử trực tiếp file này
if __name__ == '__main__':
    print(get_gold_price())









# Đoạn này dùng để chạy test thử trực tiếp file này
if __name__ == '__main__':
    print(get_gold_price())