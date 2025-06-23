import requests

def check_binance_breakouts():
    url = "https://api.binance.com/api/v3/ticker/24hr"
    exchange_info_url = "https://api.binance.com/api/v3/exchangeInfo"
    result = []

    symbols = [
        s['symbol'] for s in requests.get(exchange_info_url).json()["symbols"]
        if s['quoteAsset'] == "USDT" and s['status'] == "TRADING"
    ]

    data = requests.get(url).json()
    for coin in data:
        if coin['symbol'] not in symbols:
            continue
        try:
            price_change = float(coin['priceChangePercent'])
            volume = float(coin['quoteVolume'])
            if 5 <= price_change <= 15 and volume > 1000000:
                if float(coin['lowPrice']) < float(coin['lastPrice']) * 0.92:
                    continue  # wick filter
                if volume > 50000000:
                    level = "🔥 ULTRA"
                elif volume > 10000000:
                    level = "🚀 HIGH"
                elif volume > 3000000:
                    level = "📈 MEDIUM"
                else:
                    level = "📊 LOW"
                result.append(f"{level} breakout: {coin['symbol']} +{price_change:.2f}% 24h | Vol: {volume:,.0f} USDT")
        except:
            continue
    return result