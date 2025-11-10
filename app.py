from flask import Flask, jsonify, render_template
import requests
from datetime import datetime

app = Flask(__name__)

LIGHTER_API = "https://api.lighter.xyz/v1/markets/BTC-USD-PERP/ticker"
PARADEX_API = "https://api.prod.paradex.trade/v1/markets/BTC-USD-PERP/ticker"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/prices')
def prices():
    try:
        lighter = requests.get(LIGHTER_API).json()
        paradex = requests.get(PARADEX_API).json()

        lighter_price = float(lighter.get('price', 0))
        paradex_price = float(paradex.get('markPrice', 0))
        spread = lighter_price - paradex_price
        timestamp = datetime.now().strftime("%H:%M:%S")

        return jsonify({
            "lighter": lighter_price,
            "paradex": paradex_price,
            "spread": spread,
            "time": timestamp
        })
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
