def ty_gia():
    import requests
    respond = requests.get('https://open.er-api.com/v6/latest/USD')
    data = respond.json()
    rate = data['rates']['VND']
    print (f'Hien tai 1 USD bang: {rate} VND')
    usd = float(input('May muon doi bao nhieu USD? : '))
    vnd = usd * rate
    print(f'{usd} USD = {vnd} VND')
