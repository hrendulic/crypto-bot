import asyncio
from telegram_bot import send_telegram_message
from breakout import check_for_breakouts

async def main():
    while True:
        try:
            signals = await check_for_breakouts()
            for signal in signals:
                await send_telegram_message(signal)
        except Exception as e:
            print(f"Error: {e}")
        await asyncio.sleep(60)  # run every minute

if __name__ == "__main__":
    asyncio.run(main())
