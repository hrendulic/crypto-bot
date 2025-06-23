import aiohttp
import datetime

async def fetch_binance_data():
    url = "https://api.binance.com/api/v3/ticker/24hr"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.json()

def categorize_change(pct):
    if pct > 30:
        return "ULTRA"
    elif pct > 20:
        return "HIGH"
    elif pct > 10:
        return "MEDIUM"
    elif pct > 5:
        return "LOW"
    return None

async def check_for_breakouts():
    data = await fetch_binance_data()
    now = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    signals = []
    for coin in data:
        try:
            symbol = coin["symbol"]
            if not symbol.endswith("USDT"):
                continue
            price_change = float(coin["priceChangePercent"])
            volume = float(coin["quoteVolume"])
            category = categorize_change(price_change)
            if category and volume > 1000000:
                signals.append(
                    f"🚨 <b>{symbol}</b> breakout ({category})
"
                    f"Price change: {price_change:.2f}%
"
                    f"Volume: ${volume:,.0f}
"
                    f"<i>{now} UTC</i>"
                )
        except Exception:
            continue
    return signals
