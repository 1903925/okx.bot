from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/')
def home():
    return 'Bot çalışıyor!'

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    print("Webhook verisi geldi:", data)

    # .env'den OKX API KEY al
    api_key = os.getenv("OKX_API_KEY")
    print("OKX API KEY:", api_key)  # Test için, iş bitince silebilirsin

    return jsonify({'status': 'OK'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
