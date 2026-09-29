import requests
def get_tygia():
    try:
        import requests
        respond = requests.get('https://open.er-api.com/v6/latest/USD')
        data = respond.json()
        rate = data['rates']['VND']
        return f"💵 **TỶ GIÁ USD/VND**\n1 USD = {rate:,.0f} VND"
    except Exception as e:
        return f"❌ Lỗi lấy tỷ giá: {e}"
