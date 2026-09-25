from flask import Flask, request
from datetime import datetime
import os
import pandas as pd

app = Flask(__name__)

SHOP_NAME = "MAXALSYAN"
MOMO_NUMBER = "050-5468-770"

PRODUCTS = {
    "1": {"name": "Air Max", "price": 350},
    "2": {"name": "Jersey - Ronaldo", "price": 150},
    "3": {"name": "Jersey - Messi", "price": 150},
    "4": {"name": "Slides", "price": 120},
}

EXCEL_FILE = "orders.xlsx"

def get_menu_text():
    menu = f"Welcome to {SHOP_NAME}!\n\n"
    for k, v in PRODUCTS.items():
        menu += f"{k}. {v['name']} - GHS {v['price']}\n"
    menu += f"\nReply number to order\nReply 'momo' to pay to {MOMO_NUMBER}"
    return menu

def save_order(customer, order_text):
    data = {"Date": [datetime.now().strftime("%Y-%m-%d %H:%M")], "Customer": [customer], "Order": [order_text], "Status": ["New"]}
    df_new = pd.DataFrame(data)
    if os.path.exists(EXCEL_FILE):
        df_old = pd.read_excel(EXCEL_FILE)
        df_final = pd.concat([df_old, df_new], ignore_index=True)
    else:
        df_final = df_new
    df_final.to_excel(EXCEL_FILE, index=False)

@app.route('/')
def home():
    return f"{SHOP_NAME} Bot is LIVE! Go to /whatsapp"

@app.route('/whatsapp', methods=['GET', 'POST'])
def whatsapp_bot():
    if request.method == 'GET':
        return f"{SHOP_NAME} Bot is Running! Type 'menu'", 200
    msg = request.values.get('Body', '').lower().strip()
    number = request.values.get('From', 'Web Customer')
    if "hello" in msg or "hi" in msg or "menu" in msg or msg == "":
        reply = get_menu_text()
    elif msg in PRODUCTS:
        p = PRODUCTS[msg]
        reply = f"You selected {p['name']} - GHS {p['price']}\nType 'pay' to confirm. Pay MoMo to {MOMO_NUMBER}"
        save_order(number, p['name'])
    elif "pay" in msg or "momo" in msg:
        reply = f"Pay to MoMo: {MOMO_NUMBER}\nName: {SHOP_NAME}\nSend screenshot after payment."
    else:
        reply = "Type 'menu' to see products."
    return f"<Response><Message>{reply}</Message></Response>"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)