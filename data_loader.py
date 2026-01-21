from tinkoff.invest.clients import Client
from tinkoff.invest.schemas import CandleInterval
from datetime import datetime, timezone, timedelta
import pandas as pd

TOKEN = 't.3DhZAkbsSXelQ-Vn8VaZZL80aWFPya1rGkmfxBDYYflty6DBgbh79CRx2AdWntK39ztWFP7W-y9Rt0rk_yQ2JA'
FIGI = 'BBG004730N88' # Например, Сбербанк

def download_to_parquet(figi, filename):
    with Client(TOKEN) as client:
        # Запрашиваем данные за последние 5 лет (чтобы хватило для Walkforward)
        to_date = datetime.now(timezone.utc)
        from_date = to_date - timedelta(days=5*365)
        
        candles = []
        for candle in client.get_all_candles(
            figi=figi,
            from_=from_date,
            interval=CandleInterval.CANDLE_INTERVAL_HOUR,
        ):
            candles.append({
                'time': candle.time,
                'open': candle.open.units + candle.open.nano / 1e9,
                'high': candle.high.units + candle.high.nano / 1e9,
                'low': candle.low.units + candle.low.nano / 1e9,
                'close': candle.close.units + candle.close.nano / 1e9,
            })
        
        df = pd.DataFrame(candles)
        df.set_index('time', inplace=True)
        # Сохраняем в формате, который ожидает ваш скрипт
        df.to_parquet(filename)
        print(f"Данные сохранены в {filename}")

download_to_parquet(FIGI, 'SBER_HOUR.pq')