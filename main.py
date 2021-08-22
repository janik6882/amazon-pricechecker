# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import json
pth = "/home/pi/Amazon_bot/input.json"
input_data = json.load(open(pth, "r"))
LAST_PRICE = input_data["last"]
URL = input_data["url"]
ZIEL = input_data["price"]


class Wrapper():
    def __init__(self, token):
        self.base = "https://api.telegram.org/bot{}".format(token)
        working = self.get_me()["ok"]
        if not working:
            raise ValueError("token invalid, please check token")

    def get_me(self):
        """
        Comment: Function for testing your auth token
        Input: Name of Instance
        Output: True if token is valid, false if not
        Special: Nothing Special
        """
        url = self.base + "/getMe"
        r = requests.get(url)
        res = json.loads(r.content)
        return res

    def send_message(self, text, chatId):
        """
        Comment: Sends a message to a specified Chat by the Chat_id
        Input: Name of Instance, text to send and the chat_id
        Output: Server Response
        Special: The user must first send a message to the bot before the bot
                can send messages to the user.
        """
        # TODO: Revisit and add additional params
        # TODO: Add optional Params from Doku
        url = self.base + "/sendMessage"
        params = {
                   "text": text,
                   "chat_id": chatId,
                   }
        r = requests.get(url, params=params)
        return json.loads(r.content)

def get_price(url):
    r = requests.get(url, headers={"User-Agent":"Defined"})
    html = r.content
    parsed = BeautifulSoup(html, 'html.parser')
    price = parsed.find("span", {"class": "a-size-medium a-color-price priceBlockBuyingPriceString"}, text=True)
    res = float(price.text[:-1].replace(",", "."))
    return res

def check_price(url, goal):
    price = get_price(url)
    if price<goal:
        return [True, price]
    else:
        return [False, price]

def main():
    pth = "/home/pi/Amazon_bot/creds.json"
    creds = json.load(open(pth, "r"))
    bot = Wrapper(creds["telegram_bot"])
    notify_true = creds["notify_true"]
    notify_false = creds["notify_false"]
    try:
        price = check_price(URL, ZIEL)
    except Exception as e:
        bot.send_message("Fehler, bitte prüfen", notify_false)
        bot.send_message(e, notify_false)
        print(str(e))
        exit()
    if price[0] is True:
        mes = f"Wunschpreis erreicht, Preis beträgt nun {price[1]}€"
        bot.send_message(mes, notify_true)
        bot.send_message(mes, notify_false)
    elif price[1] != LAST_PRICE:
        remaining = price[1] - ZIEL
        mes = f"Der Preis hat sich verändert (von {LAST_PRICE}€ zu {price[1]}€), {remaining}€ fehlen noch"
        bot.send_message(mes, notify_true)
        bot.send_message(mes, notify_false)
    else:
        mes = f"Der Preis hat sich nicht verändert und beträgt noch immer {price[1]}€"
        bot.send_message(mes, notify_false)

    input_data["last"] = price[1]
    print(price)
    json.dump(input_data, open("input.json", "w"))

main()
