import json

def tg_adatok_betoltese():
    try:
        with open('autok.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def tg_adatok_mentese(autok):
    with open('autok.json', 'w', encoding='utf-8') as f:
        json.dump(autok, f, indent=4)

def tg_add_car(autok, new_car_data):
    autok.append(new_car_data)
    tg_adatok_mentese(autok)

def tg_delete_car(autok, index):
    del autok[index]
    tg_adatok_mentese(autok)
