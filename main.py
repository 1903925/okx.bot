from flask import Flask, request, jsonify
import os
import requests
import time
import hmac
import hashlib
import base64

app = Flask(__name__)

@app.route('/')
def home():
    return 'Bot çalışıyor!'

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    print("Webhook verisi geldi:", data)

    action = data.get("action")  # "buy" veya "sell"
    symbol = data.get("symbol", "BTC-USDT")  # default
    qty = str(data.get("qty", 0.05))  # miktar

    # API Key bilgilerini oku
    api_key = os.getenv("OKX_API_KEY")
    secret_key = os.getenv("OKX_API_SECRET")
    passphrase = os.getenv("OKX_API_PASSPHRASE")

    # Zaman damgası
    timestamp = str(time.time())

    # Emir verisi
    endpoint = "/api/v5/trade/order"
    url = "https://www.okx.com" + endpoint
    body = {
        "instId": symbol,
        "tdMode": "isolated",
        "side": action,
        "ordType": "market",
        "sz": qty
    }
    body_str = json.dumps(body)

    # İmzalama
    msg = timestamp + 'POST' + endpoint + body_str
    signature = base64.b64encode(hmac.new(secret_key.encode(), msg.encode(), hashlib.sha256).digest()).decode()

    headers = {
        "Content-Type": "application/json",
        "OK-ACCESS-KEY": api_key,
        "OK-ACCESS-SIGN": signature,
        "OK-ACCESS-TIMESTAMP": timestamp,
        "OK-ACCESS-PASSPHRASE": passphrase
    }

    try:
        response = requests.post(url, headers=headers, data=body_str)
        print("OKX cevabı:", response.json())
        return jsonify({"status": "emir gönderildi"}), 200
    except Exception as e:
        print("HATA:", e)
        return jsonify({"status": "hata", "detail": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
