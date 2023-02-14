import requests
import json

currency = input().lower()


r = requests.get(f'http://www.floatrates.com/daily/{currency}.json')
rates: dict = r.json()
wanted_rates = {}

with open("rates.json", "w", encoding="utf-8") as file:
    try:
        wanted_rates['usd'] = rates['usd']
    except KeyError:
        pass
    try:
        wanted_rates['eur'] = rates['eur']
    except KeyError:
        pass
    file.write(json.dumps(wanted_rates))

while True:
    currency_to_convert_to = input().lower()
    if currency_to_convert_to == "":
        break
    try:
        amount_of_money = float(input())
    except Exception:
        break
    print("Checking the cache...")
    with open("rates.json", "r+", encoding="utf-8") as file:
        wanted_rates: dict = json.loads(file.read())
        file.seek(0)
        if currency_to_convert_to not in [rate for rate in wanted_rates]:
            print("Sorry, but it is not in the cache!")
            r = requests.get(f'http://www.floatrates.com/daily/{currency}.json')
            rates = r.json()
            wanted_rates[currency_to_convert_to] = rates[currency_to_convert_to]
            file.write(json.dumps(wanted_rates))
        else:
            print("Oh! It is in the cache!")
        converted_money = amount_of_money * float(wanted_rates[currency_to_convert_to]['rate'])
        converted_money = round(converted_money, 2)
        print(str(converted_money) + " " + currency_to_convert_to.upper() + ".")
