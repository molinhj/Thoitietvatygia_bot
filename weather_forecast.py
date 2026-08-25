def thoi_tiet():
    import requests
    while True:
        api_key = '8e52e86b0eff70a88156a7eaff841fd3'
        place = input('Nhap tinh/thanh pho may muon xem  thoi tiet: ')
        url = f'https://api.openweathermap.org/data/2.5/weather?q={place}&appid={api_key}&units=metric&lang=vi'
        respone = requests.get(url)
        data = respone.json()

        if data.get('cod') == 200:
            temp = data['main']['temp']
            humid= data['main']['humidity']
            description = data['weather'][0]['description']

            print(f'\n ---THOI TIET O {place.upper()}---')
            print(f'Nhiet do: {temp}')
            print(f'Do am: {humid}')
            print(f'Trang thai: {description}')
        else:
            print('Dia diem may nhap deo ton tai\nNhap lai de')

        while True:
            user_continue = input('May xem tiep nua khong?(Co/Khong): ').lower().strip()
            if user_continue == 'co':
                break
            elif user_continue == 'khong':
                print('bye thang em')
                exit()
            else:
                print('May cuong a, nhap lai de')
