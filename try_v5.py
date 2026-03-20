import MetaTrader5 as mt5
import time as pytime
import pandas as pd
import numpy as np
from datetime import datetime, timedelta, time as dtime
import requests
import pytz

"""
we have all indicators - macd, bb, rsi, support and resistance and now adding timings also
BB + engulfing

"""

# Initialize connection to MetaTrader 5
if not mt5.initialize():
    print("Initialize failed, error code =", mt5.last_error())
    mt5.shutdown()
    exit()


# ====================== manual update =======================

buy_rsi = 30
sell_rsi = 70

profit_percentange = 400

BOT_TOKEN = "8534594469:AAHA-ly6Vb8U4Gsq7XwT_ysGoN5Wr4hL-6c"
CHAT_ID = "7372448734"

pips_500 = 500
pips_1000 = 1000

sl_pips = 500
tp_pips = 500
profit_target = 1000
martingale_lot_sizes = [0.01, 0.01, 0.01, 0.02, 0.02]
# martingale_lot_sizes = [0.01, 0.01, 0.01, 0.02, 0.02, 0.02, 0.03, 0.03, 0.04, 0.04, 0.05]
# martingale_lot_sizes = [0.01, 0.01, 0.01, 0.02, 0.02, 0.03, 0.04, 0.05]
diff_pips = 800
martingale_tp_pips = 1000
bb_gap = 0

bb15m_lower_tolerance = 5
bb15m_upper_tolerance = 5

NUM_CANDLES = 100
BARS = 100
sr_bars = 40
# Example usage
symbol = "XAUUSD"  # Change this to your desired trading symbol
# ====================== manual update =======================


buy_order_qty = 0
sell_order_qty = 0
latest_position_price = 0
profit_amount = 250

buy_ctr = 0
sell_ctr = 0


buy_ctr_00 = 0
sell_ctr_00 = 0
buy_ctr_01 = 0
sell_ctr_01 = 0

buy_ctr_02 = 0
sell_ctr_02 = 0

buy_ctr_03 = 0
sell_ctr_03 = 0
buy_ctr_04 = 0
sell_ctr_04 = 0
buy_ctr_05 = 0
sell_ctr_05 = 0



pips_200 = 200
pips_250 = 250
pips_300 = 300
pips_1000 = 1000
pips_400 = 400
pips_500 = 500
pips_800 = 800
pips_1200 = 1200

change_pips_for_sl_150 = 150
change_pips_for_sl_200 = 200
change_pips_for_sl_300 = 300
change_pips_for_sl_400 = 400
change_pips_for_sl_500 = 500
change_pips_for_sl_600 = 600
change_pips_for_sl_700 = 700
change_pips_for_sl_800 = 800
change_pips_for_sl_900 = 900
change_pips_for_sl_1000 = 1000
change_pips_for_sl_1100 = 1100
change_pips_for_sl_1200 = 1200
change_pips_for_sl_1300 = 1300
change_pips_for_sl_1400 = 1400
change_pips_for_sl_1600 = 1600
change_pips_for_sl_1500 = 1500
change_pips_for_sl_2000 = 2000
change_pips_for_sl_2300 = 2300
change_pips_for_sl_2500 = 2500
change_pips_for_sl_2800 = 2800
change_pips_for_sl_3000 = 3000
change_pips_for_sl_3500 = 3500
change_pips_for_sl_4000 = 4000
change_pips_for_sl_4500 = 4500
change_pips_for_sl_5000 = 5000
change_pips_for_sl_5500 = 5500

buy_magic_num = 101
sell_magic_num = 201

martingale_buy_magic = 101
martingale_sell_magic = 102


bb_buy_magic = 201
bb_sell_magic = 202

support_resistance_buy_magic = 301
support_resistance_sell_magic = 302

trend_buy_magic = 401
trend_sell_magic = 402
direc_buy_magic = 501
direc_sell_magic = 502
signal_buy_magic = 601
signal_sell_magic = 602

all_buy_magic = [101, 201, 301, 401, 501, 601]
all_sell_magic = [102, 202, 302, 402, 502, 602]

qty_1 = 0.01
qty_2 = 0.02
qty_3 = 0.03


buy_order_index = 0
sell_order_index = 0

buy_series = [100, 101, 102, 103, 104, 105]
sell_series = [200, 201, 202, 203, 204, 205]

start_balance = 0
target_balance = 0
current_equity = 0


def send_telegram_alert(message: str):
    """Send a message to your Telegram account."""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            print("✅ Message sent successfully!")
        # else:
        #     print(f"⚠️ Failed to send message: {response.text}")
    except Exception as e:
        print(f"Error: {e}")


def mt5_server_time(symbol):
    if not mt5.symbol_select(symbol, True):
        return None

    tick = mt5.symbol_info_tick(symbol)
    if tick and tick.time > 0:
        return datetime.fromtimestamp(tick.time)

    info = mt5.terminal_info()
    if info and hasattr(info, "server_time") and info.server_time > 0:
        return datetime.fromtimestamp(info.server_time)

    return None

def mt5_time_to_uk(server_time):
    # MT5 server time is usually UTC-based
    utc = pytz.utc.localize(server_time)

    uk_tz = pytz.timezone("Europe/London")
    uk_time = utc.astimezone(uk_tz)

    return uk_time


def is_trading_allowed_uk(symbol):
    server_time = mt5_server_time(symbol)

    if server_time is None:
        print("🚫 MT5 time unavailable – trading blocked")
        return False

    uk_time = mt5_time_to_uk(server_time)
    uk_now = uk_time.time()

    block_start = dtime(17, 30)
    block_end   = dtime(19, 15)

    if block_start <= uk_now < block_end:
        # print(f"🚫 Non-trading zone (UK): {uk_time.strftime('%H:%M:%S')}")
        return False

    # print(f"✅ Trading allowed (UK): {uk_time.strftime('%H:%M:%S')}")
    return True


def is_gold_trading_allowed(symbol):
    server_time = mt5_server_time(symbol)

    if server_time is None:
        print("🚫 MT5 time unavailable – trading blocked")
        return False

    uk_time = mt5_time_to_uk(server_time)
    uk_now = uk_time.time()

    # -----------------------------
    # UK NO-TRADE TIME WINDOWS
    # -----------------------------
# no_trade_ranges = [
#     (dtime(7, 55),  dtime(8, 15)),   # London FX open
#     (dtime(9, 55),  dtime(10, 10)),  # EU data / post-open spikes
#     (dtime(13, 0),  dtime(13, 30)),  # US data prep
#     (dtime(14, 30), dtime(14, 45)),  # COMEX open
#     (dtime(15, 30), dtime(15, 45)),  # US stock open
#     (dtime(18, 0),  dtime(18, 10)),  # London close
#     (dtime(4, 0),   dtime(4, 10)),   # Asia open
# ]

    #  mt5 timings are below (UK time - 4 hours)
    no_trade_ranges = [
        (dtime(3, 55),  dtime(4, 15)),   # London FX open
        (dtime(5, 55),  dtime(6, 15)),  # EU data / post-open spikes
        (dtime(9, 0),  dtime(12, 0)),  # US data prep
        (dtime(14, 0),  dtime(14, 30)),  # London close
        (dtime(22, 0),   dtime(22, 30)),   # China open
        (dtime(0, 0),   dtime(0, 30)),   # Asia open
    ]


        # (dtime(10, 30), dtime(11, 30)),  # US economic data release
        # (dtime(11, 30), dtime(12, 30)),  # US stock open


    for start, end in no_trade_ranges:
        # Normal (same-day) window
        if start <= end:
            if start <= uk_now < end:
                # print(f"🚫 No-trade window (UK): {uk_time.strftime('%H:%M:%S')}")
                return False
        else:
            # Cross-midnight window (not used here, but safe)
            if uk_now >= start or uk_now < end:
                return False

    # print(f"✅ Trading allowed (UK): {uk_time.strftime('%H:%M:%S')}")
    return True

def bb_momentum_exit_signal(symbol, timeframe=mt5.TIMEFRAME_M15, bars=50):
    """
    Returns:
        'EXIT_SELL'  -> strong bullish momentum
        'EXIT_BUY'   -> strong bearish momentum
        None         -> no strong momentum
    """

    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, bars)
    if rates is None or len(rates) < 25:
        return None

    df = pd.DataFrame(rates)
    df['close'] = df['close']
    df['open']  = df['open']

    # --- Bollinger Bands ---
    length = 20
    mult = 2

    df['sma'] = df['close'].rolling(length).mean()
    df['std'] = df['close'].rolling(length).std()

    df['upper'] = df['sma'] + mult * df['std']
    df['lower'] = df['sma'] - mult * df['std']

    # --- BB Width ---
    df['bb_width'] = df['upper'] - df['lower']

    # --- BB widening ---
    bb_widening = df['bb_width'].iloc[-1] > df['bb_width'].iloc[-2]

    # --- Candle direction ---
    last3 = df.iloc[-3:]

    three_bullish = all(last3['close'] > last3['open'])
    three_bearish = all(last3['close'] < last3['open'])

    # --- Final Signal ---
    if bb_widening and three_bullish:
        return 'EXIT_SELL'

    if bb_widening and three_bearish:
        return 'EXIT_BUY'

    return None

def is_high_volatility_bar(
    symbol,
    timeframe=mt5.TIMEFRAME_M15,
    points_threshold=10
):
    """
    Detects if the current candle moved
    >= points_threshold points UP or DOWN from open
    """

    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, 1)
    if rates is None or len(rates) == 0:
        return False, None

    candle = rates[0]

    open_price = candle['open']
    high_price = candle['high']
    low_price  = candle['low']

    # Convert points → price (Gold: 1 point = 0.01)
    price_threshold = points_threshold

    upward_move = high_price - open_price
    downward_move = open_price - low_price

    if upward_move >= price_threshold:
        return True, "UP"

    if downward_move >= price_threshold:
        return True, "DOWN"

    return False, None



class TrendStabilizer:
    def __init__(self, confirm_count=10):
        self.confirm_count = confirm_count
        self.counter = 0
        self.last_candidate = None
        self.confirmed_trend = "RANGE"

    def update(self, trend_5m, trend_15m, trend_1h):
        """
        trend inputs must be: 'BUY', 'SELL', or 'RANGE'
        returns confirmed trend: 'BUY', 'SELL', or 'RANGE'
        """

        # --- All timeframes must agree ---
        if trend_5m == trend_15m == trend_1h and trend_5m in ("BUY", "SELL"):
            candidate = trend_5m
        else:
            # disagreement or RANGE → reset
            self.counter = 0
            self.last_candidate = None
            self.confirmed_trend = "RANGE"
            return self.confirmed_trend

        # --- Same candidate continuing ---
        if candidate == self.last_candidate:
            self.counter += 1
        else:
            # new candidate → restart count
            self.counter = 1
            self.last_candidate = candidate

        # --- Confirm trend only after enough confirmations ---
        if self.counter >= self.confirm_count:
            self.confirmed_trend = candidate

        return self.confirmed_trend

# ================== Support and resistance ========================
def get_mt5_data_for_sr(symbol, timeframe, sr_bars):
    # print("support and resistance related data receied")
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, sr_bars + 1)  # +1 for current forming bar
    if rates is None or len(rates) == 0:
        print(f"⚠️ No data received for {symbol} timeframe {timeframe}")
        return pd.DataFrame()

    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')

    # Patch latest bar with live tick
    tick = mt5.symbol_info_tick(symbol)
    if tick is not None:
        df.at[df.index[-1], 'close'] = tick.ask
        df.at[df.index[-1], 'high'] = max(df['high'].iloc[-1], tick.ask)
        df.at[df.index[-1], 'low']  = min(df['low'].iloc[-1], tick.bid)

    return df

def detect_sr(df, window=10, tolerance=1.0):
    supports = []
    resistances = []

    for i in range(window, len(df) - window):
        # Create local window
        local_highs = df['high'].iloc[i - window:i + window + 1]
        local_lows = df['low'].iloc[i - window:i + window + 1]

        # If current high is highest in local window → resistance
        if df['high'].iloc[i] == local_highs.max():
            price = df['high'].iloc[i]
            # Check tolerance to avoid duplicates
            if not any(abs(price - r[1]) < tolerance for r in resistances):
                resistances.append((df['time'].iloc[i], price))

        # If current low is lowest in local window → support
        if df['low'].iloc[i] == local_lows.min():
            price = df['low'].iloc[i]
            if not any(abs(price - s[1]) < tolerance for s in supports):
                supports.append((df['time'].iloc[i], price))

    return supports, resistances

# ========== GET DATA ==========

def detect_support_resistance_levels(symbol):

    df_5m_data_sr = get_mt5_data_for_sr(symbol, mt5.TIMEFRAME_M5, sr_bars)
    # df_1h_data_sr = get_mt5_data_for_sr(symbol, mt5.TIMEFRAME_H1, NUM_CANDLES)

    supports, resistances = detect_sr(df_5m_data_sr)

    if not supports:
        print("⚠️ No support levels detected. Using last known low.")
        last_support = df_5m_data_sr['low'].iloc[-1]
    else:
        last_support = supports[-1][1]

    if not resistances:
        print("⚠️ No resistance levels detected. Using last known high.")
        last_resistance = df_5m_data_sr['high'].iloc[-1]
    else:
        last_resistance = resistances[-1][1]

    current_price = mt5.symbol_info_tick(symbol).ask
    tolerance = 2.0  # e.g., price within 0.5 units of S/R level

    # ✅ Dynamically adjust resistance if price breaks above
    if current_price > last_resistance + tolerance:
        last_resistance = current_price

    # ✅ Dynamically adjust support if price drops below
    if current_price < last_support - tolerance:
        last_support = current_price

    # Check last support
    # if abs(current_price - last_support) <= tolerance:
    #     send_telegram_alert(f"📉 XAUUSD Price {current_price:.2f} is near SUPPORT {last_support:.2f}!")

    # Check last resistance
    # if abs(current_price - last_resistance) <= tolerance:
        # send_telegram_alert(f"📈 XAUUSD Price {current_price:.2f} is near RESISTANCE {last_resistance:.2f}!")

    # send_telegram_alert(f"XAUUSD support and resistance levels for 1H chart are - {last_support}, {last_resistance}")


    return last_support, last_resistance
# ================== Support and resistance ========================


def get_mt5_data(symbol, timeframe, num_bars):
    # print("bollinger bands related data receied")
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, num_bars)
    if rates is None or len(rates) == 0:
        print(f"⚠️ No data received for {symbol} timeframe {timeframe}")
        return pd.DataFrame()

    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df.rename(columns={'open': 'Open', 'high': 'High', 'low': 'Low',
                       'close': 'Close', 'tick_volume': 'Volume'}, inplace=True)
    df = df[['time', 'Open', 'High', 'Low', 'Close', 'Volume']]
    return df


# ========== BOLLINGER BAND CALCULATION ==========
def add_bollinger_bands(df, length=20, std=2):
    df['BB_Middle'] = df['Close'].rolling(window=length).mean()
    df['BB_Std'] = df['Close'].rolling(window=length).std()
    df['BB_Upper'] = df['BB_Middle'] + std * df['BB_Std']
    df['BB_Lower'] = df['BB_Middle'] - std * df['BB_Std']
    return df

# ========== GET DATA ==========
# df_1h_data = get_mt5_data(symbol, mt5.TIMEFRAME_H1, NUM_CANDLES)
# df_5m_data = get_mt5_data(symbol, mt5.TIMEFRAME_M5, NUM_CANDLES)
# df_5m_break = get_mt5_data(symbol, mt5.TIMEFRAME_M5, NUM_CANDLES)
# df_1h_bb = add_bollinger_bands(df_1h_data)
# df_5m_bb = add_bollinger_bands(df_5m_data)

# ========== DISPLAY LATEST ==========
# def show_bollinger(df, label):
#     row = df.iloc[-1]
    # print(f"\n📊 {label} Bollinger Summary ({row['time']})")
    # print(f"Current Price : {row['Close']:.2f}")
    # print(f"Upper Band    : {row['BB_Upper']:.2f}")
    # print(f"Middle Band   : {row['BB_Middle']:.2f}")
    # print(f"Lower Band    : {row['BB_Lower']:.2f}")

# show_bollinger(df_1h_bb, "1-Hour")
# show_bollinger(df_5m_bb, "5-Minute")

# ========== DETECT BAND TOUCH ==========
def detect_band_touch(df, label):
    price = df['Close'].iloc[-1]
    upper = df['BB_Upper'].iloc[-1]
    lower = df['BB_Lower'].iloc[-1]
    middle = df['BB_Middle'].iloc[-1]


    # if price >= upper:
    #     print(f"🚨 {label}: Price touched or exceeded the UPPER Bollinger Band!")
    #     # send_telegram_alert("XAUUSD touched the Upper Bollinger Band (1H chart)")

    # elif price <= lower:
    #     print(f"🚨 {label}: Price touched or dropped below the LOWER Bollinger Band!")
        # send_telegram_alert("XAUUSD touched the lower Bollinger Band (1H chart)")
    # else:
    #     print(f"✅ {label}: Price is within the bands.")
    #     send_telegram_alert("XAUUSD is not touched either upper or lower (1H chart)")

    return price, upper, lower, middle


# ----------------- Double Top / Bottom -----------------
def is_double_top(df, symbol, window=10):
    if len(df) < window:
        return False
    highs = df['high'].iloc[-window:]
    peaks = highs.nlargest(2)
    tolerance = 0.002 * df['close'].iloc[-1]  # 0.2% price tolerance
    
    if abs(peaks.iloc[0] - peaks.iloc[1]) <= tolerance:
        send_telegram_alert(f"📈 Double Top detected on {symbol} 5M chart near {peaks.iloc[0]:.2f}")
        return True
    return False


def is_double_bottom(df, symbol, window=10):
    if len(df) < window:
        return False
    lows = df['low'].iloc[-window:]
    bottoms = lows.nsmallest(2)
    tolerance = 0.002 * df['close'].iloc[-1]  # 0.2% price tolerance
    
    if abs(bottoms.iloc[0] - bottoms.iloc[1]) <= tolerance:
        send_telegram_alert(f"📉 Double Bottom detected on {symbol} 5M chart near {bottoms.iloc[0]:.2f}")
        return True
    return False


# -------------------
# Engulfing Patterns
# -------------------
def is_bullish_engulfing(df, symbol):
    if len(df) < 2:
        return False
    prev = df.iloc[-2]
    last = df.iloc[-1]

    if (last['close'] > last['open']) and \
       (prev['close'] < prev['open']) and \
       (last['close'] > prev['open']) and \
       (last['open'] < prev['close']):
        send_telegram_alert(f"📉 Bullish Engulfing detected on {symbol} 5M at {last['close']:.2f}")
        return True
    return False


def is_bearish_engulfing(df, symbol):
    if len(df) < 2:
        return False
    prev = df.iloc[-2]
    last = df.iloc[-1]

    if (last['close'] < last['open']) and \
       (prev['close'] > prev['open']) and \
       (last['open'] > prev['close']) and \
       (last['close'] < prev['open']):
        send_telegram_alert(f"📈 Bearish Engulfing detected on {symbol} 5M at {last['close']:.2f}")
        return True
    return False


# -------------------
# Hammer Patterns
# -------------------
def is_bullish_hammer(df, symbol):
    if len(df) < 1:
        return False
    last = df.iloc[-1]
    body = abs(last['close'] - last['open'])
    lower_shadow = min(last['open'], last['close']) - last['low']
    upper_shadow = last['high'] - max(last['open'], last['close'])

    if body < 0.2:  # ignore tiny candles
        return False

    if (lower_shadow >= 1.0 * body) and (upper_shadow <= 0.5 * body) and (last['close'] > last['open']):
        send_telegram_alert(f"📉 Bullish Hammer detected on {symbol} 5M at {last['close']:.2f}")
        return True
    return False


def is_bearish_hammer(df, symbol):
    if len(df) < 1:
        return False
    last = df.iloc[-1]
    body = abs(last['close'] - last['open'])
    upper_shadow = last['high'] - max(last['open'], last['close'])
    lower_shadow = min(last['open'], last['close']) - last['low']

    if body < 0.2:
        return False

    if (upper_shadow >= 1.0 * body) and (lower_shadow <= 0.5 * body) and (last['close'] < last['open']):
        send_telegram_alert(f"📈 Bearish Hammer detected on {symbol} 5M at {last['close']:.2f}")
        return True
    return False


# -------------------
# Pin Bar Patterns
# -------------------
def is_bullish_pin_bar(df, symbol):
    if len(df) < 1:
        return False
    last = df.iloc[-1]
    body = abs(last['close'] - last['open'])
    lower_shadow = min(last['open'], last['close']) - last['low']
    upper_shadow = last['high'] - max(last['open'], last['close'])

    if lower_shadow >= 2.0 * body and upper_shadow <= 0.5 * body and last['close'] > last['open']:
        send_telegram_alert(f"📉 Bullish Pin Bar detected on {symbol} 5M at {last['close']:.2f}")
        return True
    return False


def is_bearish_pin_bar(df, symbol):
    if len(df) < 1:
        return False
    last = df.iloc[-1]
    body = abs(last['close'] - last['open'])
    upper_shadow = last['high'] - max(last['open'], last['close'])
    lower_shadow = min(last['open'], last['close']) - last['low']

    if upper_shadow >= 2.0 * body and lower_shadow <= 0.5 * body and last['close'] < last['open']:
        send_telegram_alert(f"📈 Bearish Pin Bar detected on {symbol} 5M at {last['close']:.2f}")
        return True
    return False


# -------------------
# Doji Pattern
# -------------------
def is_doji(df, symbol):
    if len(df) < 1:
        return False
    last = df.iloc[-1]
    body = abs(last['close'] - last['open'])
    total_range = last['high'] - last['low']

    if total_range == 0:
        return False

    if body / total_range <= 0.1:  # body ≤ 10% of candle range
        send_telegram_alert(f"⚖️ Doji detected on {symbol} 5M at {last['close']:.2f}")
        return True
    return False

def calculate_rsi(df, period=14, symbol="XAUUSD.r"):
    """
    Calculate RSI using closing prices.
    Adds 'RSI' column to the DataFrame and returns it.
    Sends Telegram alert when RSI crosses key levels (30 or 70).
    """
    if len(df) < period:
        return df  # Not enough data to calculate RSI
    
    delta = df['Close'].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss
    df['RSI'] = 100 - (100 / (1 + rs))

    # Latest RSI value
    rsi_value = df['RSI'].iloc[-1]
    # print(f"rsi value is {rsi_value}")
    # # ✅ Alert logic
    # if rsi_value >= 60:
    #     send_telegram_alert(f"📈 {symbol} RSI={rsi_value:.2f} → Overbought zone! Possible SELL setup.")
    # elif rsi_value <= 40:
    #     send_telegram_alert(f"📉 {symbol} RSI={rsi_value:.2f} → Oversold zone! Possible BUY setup.")
    # elif 40 < rsi_value < 60:
    #     send_telegram_alert(f"⚖️ {symbol} RSI={rsi_value:.2f} → Neutral zone. Market consolidating.")
    
    return df



# -------------------------------------------------------
# Utility: cluster nearby levels into zones
# -------------------------------------------------------
def cluster_levels(levels, tolerance=8):
    """
    Groups nearby price levels into zones
    """
    if len(levels) == 0:
        return []

    levels = sorted(levels)
    clustered = [levels[0]]

    for lvl in levels[1:]:
        if abs(lvl - clustered[-1]) > tolerance:
            clustered.append(lvl)

    return clustered


# -------------------------------------------------------
# MAIN FUNCTION
# -------------------------------------------------------
def support_resistance_with_breaks(
    df,
    left_bars=15,
    right_bars=15,
    lookback=120,
    volume_thresh=20,
    cluster_tolerance=8
):
    """
    df must contain:
    ['open', 'high', 'low', 'close', 'tick_volume']
    """

    df = df.copy().reset_index(drop=True)

    # ---------------------------------------------------
    # Volume Oscillator (same as LuxAlgo)
    # ---------------------------------------------------
    short_ema = df['tick_volume'].ewm(span=5, adjust=False).mean()
    long_ema = df['tick_volume'].ewm(span=10, adjust=False).mean()
    df['volume_osc'] = 100 * (short_ema - long_ema) / long_ema

    # ---------------------------------------------------
    # Work ONLY on recent candles
    # ---------------------------------------------------
    recent = df.iloc[-lookback:].copy()

    pivot_highs = []
    pivot_lows = []

    # ---------------------------------------------------
    # Detect pivot highs & lows
    # ---------------------------------------------------
    for i in range(left_bars, len(recent) - right_bars):
        high_range = recent['high'].iloc[i-left_bars:i+right_bars+1]
        low_range = recent['low'].iloc[i-left_bars:i+right_bars+1]

        if recent['high'].iloc[i] == high_range.max():
            pivot_highs.append(recent['high'].iloc[i])

        if recent['low'].iloc[i] == low_range.min():
            pivot_lows.append(recent['low'].iloc[i])

    # ---------------------------------------------------
    # Cluster levels into zones
    # ---------------------------------------------------
    resistance_levels = cluster_levels(pivot_highs, cluster_tolerance)
    support_levels = cluster_levels(pivot_lows, cluster_tolerance)

    # ---------------------------------------------------
    # Select ACTIVE levels relative to price
    # ---------------------------------------------------
    price = recent['close'].iloc[-1]

    active_resistance = min(
        [r for r in resistance_levels if r > price],
        default=None
    )

    active_support = max(
        [s for s in support_levels if s < price],
        default=None
    )

    # ---------------------------------------------------
    # Prepare signal columns
    # ---------------------------------------------------
    df['active_resistance'] = active_resistance
    df['active_support'] = active_support

    df['break_resistance'] = False
    df['break_support'] = False
    df['bull_wick'] = False
    df['bear_wick'] = False

    # ---------------------------------------------------
    # Signal logic (last candle only)
    # ---------------------------------------------------
    i = len(df) - 1

    if active_resistance and active_support:

        prev_close = df['close'].iloc[i-1]
        close = df['close'].iloc[i]
        open_ = df['open'].iloc[i]
        high = df['high'].iloc[i]
        low = df['low'].iloc[i]
        vol = df['volume_osc'].iloc[i]

        # Candle anatomy
        body = abs(close - open_)
        lower_wick = min(open_, close) - low
        upper_wick = high - max(open_, close)

        # Resistance break
        if prev_close < active_resistance and close > active_resistance and vol > volume_thresh:
            df.at[i, 'break_resistance'] = True

        # Support break
        if prev_close > active_support and close < active_support and vol > volume_thresh:
            df.at[i, 'break_support'] = True

        # Wick rejections
        if close < active_resistance and upper_wick > body * 1.5:
            df.at[i, 'bear_wick'] = True

        if close > active_support and lower_wick > body * 1.5:
            df.at[i, 'bull_wick'] = True

    return df


def detect_breakout(df, length=20, std_dev=2, bbw_mult=1.1):

    rename_map = {
        'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close',
        'O': 'open', 'H': 'high', 'L': 'low', 'C': 'close'
    }
    df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})

    required_cols = {'open', 'high', 'low', 'close'}
    if not required_cols.issubset(df.columns):
        raise ValueError(f"DataFrame missing required columns: {required_cols - set(df.columns)}")

    # --- Bollinger Bands ---
    df['middle'] = df['close'].rolling(length).mean()
    df['std'] = df['close'].rolling(length).std()
    df['upper'] = df['middle'] + std_dev * df['std']
    df['lower'] = df['middle'] - std_dev * df['std']

    # --- Bollinger Band Width ---
    df['bbw'] = (df['upper'] - df['lower']) / df['middle']
    df['bbw_ma'] = df['bbw'].rolling(length).mean()

    # --- Detect BB width expansion ---
    df['bb_expanding'] = df['bbw'] > (df['bbw_ma'] * bbw_mult)

    # --- Detect Breakout Candles ---
    df['above_upper'] = df['close'] > df['upper']
    df['below_lower'] = df['close'] < df['lower']

    # --- Confirm Breakout only if next candle also closes outside ---
    df['bull_breakout'] = (df['above_upper']) & (df['above_upper'].shift(1)) & (df['above_upper'].shift(2))
    df['bear_breakout'] = (df['below_lower']) & (df['below_lower'].shift(1)) & (df['below_lower'].shift(2))

    # --- Combine conditions ---
    df['confirmed_breakout'] = np.where(
        (df['bull_breakout'] | df['bear_breakout']),
        True,
        False
    )

    return df


def monitor_and_confirm(symbol, upper_band, lower_band, support, resistance, tolerance=4.0):
    """
    Check 1H levels (S/R + Bollinger) and confirm on 5M with candlestick patterns.
    Returns sell_signal, buy_signal as booleans.
    """
    sell_signal = False
    buy_signal = False
    bob_signal = False
    bos_signal = False

    current_price = mt5.symbol_info_tick(symbol).ask

    # Fetch 5M data once
    rates_5m = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M5, 0, 200)
    df_5m = pd.DataFrame(rates_5m)

    # ---- RSI Calculation ----
    df_5m_rsi = calculate_rsi(df_5m.copy())
    rsi_value = df_5m_rsi['RSI'].iloc[-1]

    # ---- VOLUME Calculation ----
    df_5m['avg_volume'] = df_5m['tick_volume'].rolling(window=20).mean()
    current_volume = df_5m['tick_volume'].iloc[-1]
    avg_volume = df_5m['avg_volume'].iloc[-1]
    high_volume = current_volume > 1.2 * avg_volume  # 20% above average

    # --BB breakout info-----
    df_5m_break = get_mt5_data(symbol, mt5.TIMEFRAME_M5, NUM_CANDLES)
    df_5m_bb = detect_breakout(df_5m_break)
    latest = df_5m_bb.iloc[-1]

    if latest['confirmed_breakout']:
        if latest['bull_breakout']:
            bob_signal = True
        elif latest['bear_breakout']:
            bos_signal = True

    # if (current_price >= resistance - tolerance or current_price >= upper_band - tolerance) and rsi_value >= 55:
    if current_price >= upper_band - tolerance and rsi_value >= 50:
        # send_telegram_alert(f"📈 SELL signal confirmed on 5M chart near resistance {resistance:.2f}, RSI={rsi_value:.2f} Volume: {current_volume:.0f} (> avg {avg_volume:.0f})")
        sell_signal = True
        # Place sell order logic here

    # if current_price <= support + tolerance or current_price <= lower_band + tolerance and rsi_value <= 45:
    if current_price <= lower_band + tolerance and rsi_value <= 50:
        # send_telegram_alert(f"📉 BUY signal confirmed on 5M chart near support {support:.2f}, RSI={rsi_value:.2f} Volume: {current_volume:.0f} (> avg {avg_volume:.0f})")
        buy_signal = True
        # Place buy order logic here

    return buy_signal, sell_signal, bob_signal, bos_signal

# Function to place a buy order
def place_buy_order(symbol, buy_order_qty, magic_num):

    print(f"buy magic number is : {magic_num}")
   
    price = mt5.symbol_info_tick(symbol).ask

    if price == 0:
        print(f"Error retrieving price for {symbol}.")
        return

    tp = price + pips_1000 * mt5.symbol_info(symbol).point
    sl = price - pips_1000 * mt5.symbol_info(symbol).point

    if magic_num == martingale_buy_magic:    
        order = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": buy_order_qty,
            "type": 0,  # Buy order type
            "price": price,
            # "tp": tp,
            # "sl": buy_sl,
            "deviation": 50,  # Slippage
            "magic": magic_num,
            "comment": "TP only",
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
    else:    
        order = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": buy_order_qty,
            "type": 0,  # Buy order type
            "price": price,
            "tp": tp,
            "sl": sl,
            "deviation": 50,  # Slippage
            "magic": magic_num,
            "comment": "TP only",
            "type_filling": mt5.ORDER_FILLING_IOC,
        }



    # Send the buy order
    result = mt5.order_send(order)

    # Check the result of the buy order
    if result is None:
        print("Buy order failed, error code:", mt5.last_error())
    elif result.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"Buy order failed. "
              f" price: {price} tp {tp} Vol: {buy_order_qty} EC: {result.retcode}")
    else:
        print(f"Buy order placed successfully: {result.order}")
        print(f"Buy order Success. "
              f" price: {price} tp {tp} Vol: {buy_order_qty}")

        if magic_num == martingale_buy_magic:
            update_common_tp_for_buy(symbol, magic_num)
       

# Function to place a sell order
def place_sell_order(symbol, sell_order_qty, magic_num):

    print(f"sell magic number is : {magic_num}")
  
    price = mt5.symbol_info_tick(symbol).bid
    if price is None:
        print("Error retrieving bid price.")
        return

    tp = price - pips_1000 * mt5.symbol_info(symbol).point
    sl = price + pips_1000 * mt5.symbol_info(symbol).point

    if magic_num == martingale_sell_magic:    
        sell_order = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": sell_order_qty,
            "type": 1,  # Sell order type
            "price": price,
            # "tp": tp,
            # "sl": sell_sl,
            "deviation": 50,  # Slippage
            "magic": magic_num,
            "comment": "TP only",
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
    else:
        sell_order = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": sell_order_qty,
            "type": 1,  # Sell order type
            "price": price,
            "sl": sl,
            "tp": tp,
            "deviation": 50,  # Slippage
            "magic": magic_num,
            "comment": "sell",
            "type_filling": mt5.ORDER_FILLING_IOC,
        }

    # Send the sell order
    result = mt5.order_send(sell_order)

    # Check the result of the sell order
    if result is None:
        print(f"Sell order failed, error code:, {mt5.last_error()} V is:{sell_order_qty} ")
    elif result.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"Sell order failed. "
              f" price: {price} tp {tp} Vol: {sell_order_qty} EC: {result.retcode}")
    else:
        print(f"Sell order placed successfully: {result.order}")
        print(f"Sell order Success. "
              f" price: {price} tp {tp} Vol: {sell_order_qty}")

        if magic_num == martingale_sell_magic:
            update_common_tp_for_sell(symbol, magic_num)


# Function to update TP for all buy orders to a common TP based on the latest buy order
def update_common_tp_for_buy(symbol, magic_num):

    # time.sleep(5)  # Adjust the duration as necessary

    positions = mt5.positions_get(symbol=symbol)
    if not positions:
        print("No open buy positions found.")
        return

    # Filter for buy positions
    # buy_positions = [pos for pos in positions if pos.magic == magic_num]
    buy_positions = [pos for pos in positions if pos.type == mt5.ORDER_TYPE_BUY
                     and pos.magic == magic_num]

    if not buy_positions:
        print("No buy positions to update TP.")
        return

    total_volume = sum(pos.volume for pos in buy_positions)
    weighted_sum_price = sum(pos.price_open * pos.volume for pos in buy_positions)

    if total_volume == 0:
        print(f"total volume is zero. no can't calculate avg price")
        return

    avg_buy_price = weighted_sum_price / total_volume
    buy_tp_price_common = avg_buy_price + martingale_tp_pips * mt5.symbol_info(symbol).point
    # buy_tp_price_single = get_latest_buy_tp(symbol, magic_num)

    # if len(buy_positions) <= 5:
    buy_tp_price = buy_tp_price_common
    # else:
    #     buy_tp_price = buy_tp_price_single

    # Update TP for each buy position to the new common TP
    for buy_pos in buy_positions:
        print(f"buy order ticket is : {buy_pos.ticket} TPis: {buy_tp_price}")
        modify_request = {
            "action": mt5.TRADE_ACTION_SLTP,
            "symbol": symbol,
            "position": buy_pos.ticket,
            "tp": buy_tp_price,  # Set the new common TP
            # "sl": sl,
            # "deviation": 20,
        }

        # Send the modify request
        modify_result = mt5.order_send(modify_request)
        
        # Check the result and output an appropriate message
        if modify_result is None or modify_result.retcode != mt5.TRADE_RETCODE_DONE:
            print(f"Failed to update TP for Buy order {buy_pos.ticket}. "
                  f"Error code: {modify_result.retcode if modify_result else 'None'} "
                  f"Message: {mt5.last_error()}")
        else:
            print(f"Successfully updated TP for Buy order {buy_pos.ticket} to {buy_tp_price}")


# Function to update TP for all buy orders to a common TP based on the latest buy order
def update_common_tp_for_sell(symbol, magic_num):

    # time.sleep(5)  # Adjust the duration as necessary
    positions = mt5.positions_get(symbol=symbol)
    if not positions:
        print("No open sell positions found.")
        return

    # Filter for sell positions
    sell_positions = [pos for pos in positions if pos.type == mt5.ORDER_TYPE_SELL
                      and pos.magic == magic_num]
    # print(f"all sell positions are: {sell_positions} ")

    if not sell_positions:
        print("No sell positions to update TP.")
        return

    total_volume = sum(pos.volume for pos in sell_positions)
    weighted_sum_price = sum(pos.price_open * pos.volume for pos in sell_positions)

    if total_volume == 0:
        print(f"total volume is zero. no can't calculate avg price")
        return

    avg_sell_price = weighted_sum_price / total_volume
    sell_tp_price_common = avg_sell_price - martingale_tp_pips * mt5.symbol_info(symbol).point
    # sell_tp_price_single = get_latest_sell_tp(symbol, magic_num)

    # if len(sell_positions) <= 5:
    sell_tp_price = sell_tp_price_common
    # else:
    #     sell_tp_price = sell_tp_price_single

    # Update TP for each sell position to the new common TP
    for sell_pos in sell_positions:
        print(f"sell order ticket is : {sell_pos.ticket} TPis: {sell_tp_price}")
        modify_request = {
            "action": mt5.TRADE_ACTION_SLTP,
            "symbol": symbol,
            "position": sell_pos.ticket,
            "tp": sell_tp_price,  # Set the new common TP
            # "sl": sl,
            # "deviation": 20,
        }


        # Send the modify request
        modify_result = mt5.order_send(modify_request)
        
        # Check the result and output an appropriate message
        if modify_result.retcode != mt5.TRADE_RETCODE_DONE:
            print(f"Failed to update TP for sell order {sell_pos.ticket}. "
                  f"Error code: {modify_result.retcode if modify_result else 'None'} "
                  f"Message: {mt5.last_error()} sell_tp : {sell_tp_price}" )
        else:
            print(f"Successfully updated TP for sell order {sell_pos.ticket} to {sell_tp_price}")
        # time.sleep(1)  # Adjust the duration as necessary

def close_orders_based_on_conditions(symbol, price_15m, upper_band_15m, lower_band_15m, middle_band_15m, allow_buy_orders, allow_sell_orders, m5_trend, m15_trend, h1_trend, signal, final_trend):
    global target_balance

    # Get all positions for the symbol
    positions = mt5.positions_get(symbol=symbol)
    if not positions:
        # print(f"No positions found for {symbol}.")
        return

# scenario 1 -- begins
    # current_equity = get_equity(symbol)
    
    # if current_equity >= target_balance:

    #     print(f"before clearing current equity and target balances are {current_equity}, {target_balance}")
    #     target_balance = current_equity + profit_target
    #     close_strategy_orders1(symbol)
    #     print(f"After clearing current equity and target balances are {current_equity}, {target_balance}")
# scenario 1 -- end

# scenairo 1
    martingale_sell_positions = [pos for pos in positions if pos.type == mt5.ORDER_TYPE_SELL and pos.magic == martingale_sell_magic]
    if martingale_sell_positions:
        if final_trend == "BUY" or signal == "EXIT_SELL":
            print(f"closing all sell orders because all trend indicators are showing BUY")
            close_strategy_orders(symbol, martingale_sell_magic)

    # if allow_sell_orders and not allow_buy_orders: # and m5_trend == "SELL":
    martingale_buy_positions = [pos for pos in positions if pos.type == mt5.ORDER_TYPE_BUY and pos.magic == martingale_buy_magic]
    if martingale_buy_positions:
        if final_trend == "SELL" or signal == "EXIT_BUY":
            print(f"closing all buy orders because all trend indicators are showing SELL")
            close_strategy_orders(symbol, martingale_buy_magic)


    # if allow_buy_orders and not allow_sell_orders:  # and m5_trend == "BUY":
    # trend_sell_positions = [pos for pos in positions if pos.type == mt5.ORDER_TYPE_SELL and pos.magic == trend_sell_magic]
    # if trend_sell_positions:
    #     if m5_trend == "BUY" and m15_trend == "BUY" and h1_trend == "BUY":
    #         print(f"closing all trend based sell orders as only buy orders are allowed now")
    #         close_strategy_orders(symbol, trend_sell_magic)

    # # if allow_sell_orders and not allow_buy_orders: # and m5_trend == "SELL":
    # trend_buy_positions = [pos for pos in positions if pos.type == mt5.ORDER_TYPE_BUY and pos.magic == trend_buy_magic]
    # if trend_buy_positions:
    #     if m5_trend == "SELL" and m15_trend == "SELL" and h1_trend == "SELL":
    #         print(f"closing all trend based buy orders as only sell orders are allowed now")
    #         close_strategy_orders(symbol, trend_buy_magic)


# scenario 2 - Max loss -- begins

    martingale_positions = [pos for pos in positions if pos.magic == martingale_buy_magic or pos.magic == martingale_sell_magic]

    conditions_1 = [
        (1, -100)
    ]

    total_profit = sum(pos.profit for pos in martingale_positions)
    total_positions = len(martingale_positions)

    for count_max, profit_max in conditions_1:
         if total_positions >= count_max and total_profit <= profit_max:
            print(f"closing all orders due to max loss and 2 hours delay from now to restart the logic")
            close_strategy_orders1(symbol)
            pytime.sleep(60)
            break


# scenario 3 - min loss -- begins
    # martingale_positions = [pos for pos in positions if pos.magic == martingale_buy_magic or pos.magic == martingale_sell_magic]

    # conditions_2 = [
    #     (5, 0)
    # ]

    # total_profit = sum(pos.profit for pos in martingale_positions)
    # total_positions = len(martingale_positions)

    # for count_max, profit_max in conditions_2:
    #      if total_positions >= count_max and total_profit >= profit_max:
    #             print(f"closing all orders at break even and 2 min delay from now to restart the logic")
    #             close_strategy_orders1(symbol)
    #             time.sleep(120)
    #             break


# scenario 4 - min loss -- begins

    martingale_buy_pos = [bpos for bpos in positions if bpos.type == mt5.ORDER_TYPE_BUY and bpos.magic in all_buy_magic]
    martingale_sell_pos = [spos for spos in positions if spos.type == mt5.ORDER_TYPE_SELL and spos.magic in all_sell_magic]


    if martingale_buy_pos:
        for order in martingale_buy_pos:
            if order.volume == 0.01:
                if order.profit >= 5:
                    close_order(order, symbol)
            elif order.volume == 0.02:
                if order.profit >= 10:
                    close_order(order, symbol)            
            elif order.volume == 0.03:
                if order.profit >= 15:
                    close_order(order, symbol)            
            else:
                if order.profit >= 20:
                    close_order(order, symbol)

    if martingale_sell_pos:
        for order in martingale_sell_pos:
            if order.volume == 0.01:
                if order.profit >= 5:
                    close_order(order, symbol)
            elif order.volume == 0.02:
                if order.profit >= 10:
                    close_order(order, symbol)            
            elif order.volume == 0.03:
                if order.profit >= 15:
                    close_order(order, symbol)            
            else:
                if order.profit >= 20:
                    close_order(order, symbol)

    # =========== Scenario 4 -- End


def close_strategy_orders(symbol, magic_number):

    positions = mt5.positions_get(symbol=symbol)
    if positions is None:
        print("No positions found. Error code:", mt5.last_error())
        return False

    # Filter positions by the specified magic number
    strategy_positions = [pos for pos in positions if pos.magic == magic_number]

    if not strategy_positions:
        print(f"No positions found for magic number {magic_number}.")
        return False

    # Close all positions one by one
    for position in strategy_positions:
        order_type = mt5.ORDER_TYPE_BUY if position.type == mt5.ORDER_TYPE_BUY else mt5.ORDER_TYPE_SELL
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": position.volume,
            "type": mt5.ORDER_TYPE_SELL if order_type == mt5.ORDER_TYPE_BUY else mt5.ORDER_TYPE_BUY,
            "position": position.ticket,
            "price": mt5.symbol_info_tick(symbol).ask if order_type == mt5.ORDER_TYPE_BUY else mt5.symbol_info_tick(symbol).bid,
            "deviation": 20,
            "magic": magic_number,  # Use the same magic number for tracking
            "comment": "Closing strategy position",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        result = mt5.order_send(request)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print(f"Failed to close position {position.ticket}. Error code: {result.retcode}")
            return False
        else:
            print(f"Closed position {position.ticket} successfully.")
    return True

# Function to get the latest buy order TP price
def get_latest_buy_tp(symbol, magic_num):
    positions = mt5.positions_get(symbol=symbol)
    if not positions:
        print("No open buy positions found.")
        return None

    # Filter for buy positions
    buy_positions = [pos for pos in positions if pos.type == mt5.ORDER_TYPE_BUY and pos.volume == 0.03]
    if not buy_positions:
        print("No buy positions found.")
        return None

    latest_buy_position = max(buy_positions, key=lambda pos: pos.time)

    return latest_buy_position.price_open  # Corrected from `.open_price` to `.price_open`
   

# Function to get the latest sell order TP price
def get_latest_sell_tp(symbol, magic_num):
    positions = mt5.positions_get(symbol=symbol)
    if not positions:
        print("No open buy positions found.")
        return None

    # Filter for sell positions
    sell_positions = [pos for pos in positions if pos.type == mt5.ORDER_TYPE_SELL and pos.volume == 0.03]
    if not sell_positions:
        print("No buy positions found.")
        return None

    latest_sell_position = max(sell_positions, key=lambda pos: pos.time)

    return latest_sell_position.price_open  # Corrected from `.open_price` to `.price_open`

# -----------------------------
# MACD Calculation
# -----------------------------
def get_macd_trend(symbol, timeframe, bars=200):
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, bars)
    if rates is None or len(rates) < 50:
        return "NO DATA", None

    df = pd.DataFrame(rates)

    df['ema_fast'] = df['close'].ewm(span=12, adjust=False).mean()
    df['ema_slow'] = df['close'].ewm(span=26, adjust=False).mean()
    df['macd'] = df['ema_fast'] - df['ema_slow']
    df['signal'] = df['macd'].ewm(span=9, adjust=False).mean()
    df['hist'] = df['macd'] - df['signal']

    macd = df['macd'].iloc[-1]
    signal = df['signal'].iloc[-1]

    if macd < 0 and macd < signal:
        return "SELL", macd
    elif macd > 0 and macd > signal:
        return "BUY", macd
    else:
        return "RANGE", macd

# -----------------------------
# Hourly Market reversal indication
# -----------------------------

def detect_h1_reversal(symbol):
    rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_H1, 0, 200)
    if rates is None or len(rates) < 50:
        return False, None

    df = pd.DataFrame(rates)

    df['ema_fast'] = df['close'].ewm(span=12, adjust=False).mean()
    df['ema_slow'] = df['close'].ewm(span=26, adjust=False).mean()
    df['macd'] = df['ema_fast'] - df['ema_slow']
    df['signal'] = df['macd'].ewm(span=9, adjust=False).mean()

    macd_prev = df['macd'].iloc[-2]
    signal_prev = df['signal'].iloc[-2]
    macd_curr = df['macd'].iloc[-1]
    signal_curr = df['signal'].iloc[-1]

    if macd_prev < signal_prev and macd_curr > signal_curr:
        return True, "BULLISH"
    elif macd_prev > signal_prev and macd_curr < signal_curr:
        return True, "BEARISH"

    return False, None


def monitor_and_place_new_orders(symbol, buy_magic_num, sell_magic_num):

    # Get all positions for the symbol
    positions = mt5.positions_get(symbol=symbol)
    if not positions:
        # print(f"No positions found for {symbol}.")
        return

    # atr_value = get_atr(symbol, timeframe=mt5.TIMEFRAME_M15, period=14, bars=200)
    # print("Current ATR:", atr_value)

    # # Example adaptive logic
    # if atr_value > 10:
    #     print("High volatility → use wider stop loss.")
    # else:
    #     print("Low volatility → tighten stop loss.")

    buy_ord = [pos for pos in positions if pos.type == mt5.ORDER_TYPE_BUY]
    sell_ord = [pos for pos in positions if pos.type == mt5.ORDER_TYPE_SELL]

    buy_pos_tot = sum(pos.volume for pos in positions if pos.type == mt5.ORDER_TYPE_BUY)
    sell_pos_tot = sum(pos.volume for pos in positions if pos.type == mt5.ORDER_TYPE_SELL)

    buy_count = round(buy_pos_tot - sell_pos_tot, 2)
    sell_count = round(sell_pos_tot - buy_pos_tot, 2)

    buy_order_qty = 0.01
    sell_order_qty = 0.01
    # buy_magic_num = 101
    # sell_magic_num = 201

    if sell_count >= 0.03:
        place_buy_order(symbol, buy_order_qty, magic_num=101)
    if buy_count >= 0.03:
        place_sell_order(symbol, sell_order_qty, magic_num=201)


def update_sl(position, new_sl):
    """Helper function to update stop-loss for a given position."""
    modify_request = {
        "action": mt5.TRADE_ACTION_SLTP,
        "symbol": position.symbol,
        "position": position.ticket,
        "sl": new_sl,
        "tp": position.tp,  # Retain the existing TP
        "deviation": 20,  # Slippage tolerance
    }

    result = mt5.order_send(modify_request)
    return result and result.retcode == mt5.TRADE_RETCODE_DONE

def update_sl_for_buy(symbol):
    """Updates stop-loss for hedging buy positions based on predefined thresholds."""
    
    symbol_info = mt5.symbol_info(symbol)
    if not symbol_info:
        print(f"Failed to get symbol info for {symbol}.")
        return
    
    point = symbol_info.point

    price_thresholds = {
        change_pips_for_sl_500: 50,
        change_pips_for_sl_1000: 500,
        change_pips_for_sl_1500: 1000,
        change_pips_for_sl_2000: 1500,
        change_pips_for_sl_2500: 2000,
        change_pips_for_sl_3000: 2500,
        change_pips_for_sl_3500: 3000,
        change_pips_for_sl_4000: 3500,
        change_pips_for_sl_4500: 4000,
        change_pips_for_sl_5500: 5000
        }
    
    positions = mt5.positions_get(symbol=symbol)
    if not positions:
        print(f"No positions found for {symbol}.")
        return

    buy_positions = [pos for pos in positions if pos.type == mt5.ORDER_TYPE_BUY and pos.magic == 101]

    if not buy_positions:
        return


    for pos in buy_positions:
        buy_price = pos.price_open
        current_sl = pos.sl
        current_tp = pos.tp
        current_price = symbol_info.bid  

        for threshold, sl_offset in price_thresholds.items():

            if current_price >= buy_price + threshold * point:
                new_sl = buy_price + sl_offset * point

                if current_sl == 0.0:
                    update_sl(pos, new_sl)
                else:
                    if current_sl != new_sl and new_sl > current_sl:
                        update_sl(pos, new_sl)
                        pass  # Successfully updated SL


def update_sl_for_sell(symbol):
    symbol_info = mt5.symbol_info(symbol)
    if not symbol_info:
        print(f"Failed to get symbol info for {symbol}.")
        return

    point = symbol_info.point
   
    price_thresholds = {
        change_pips_for_sl_500: 50,
        change_pips_for_sl_1000: 500,
        change_pips_for_sl_1500: 1000,
        change_pips_for_sl_2000: 1500,
        change_pips_for_sl_2500: 2000,
        change_pips_for_sl_3000: 2500,
        change_pips_for_sl_3500: 3000,
        change_pips_for_sl_4000: 3500,
        change_pips_for_sl_4500: 4000,
        change_pips_for_sl_5500: 5000
        }

    positions = mt5.positions_get(symbol=symbol)
    if not positions:
        print(f"No positions found for {symbol}.")
        return

    sell_positions = [pos for pos in positions if pos.type == mt5.ORDER_TYPE_SELL and pos.magic == 201]
    
    if not sell_positions:
        return


    for pos in sell_positions:
        sell_price = pos.price_open
        current_sl = pos.sl
        current_tp = pos.tp
        current_price = symbol_info.ask  # Use ask price for sell positions

        for threshold, sl_offset in price_thresholds.items():

            if current_price <= sell_price - threshold * point:  # For SELL: price drops below threshold
                new_sl = sell_price - sl_offset * point  # Move SL lower as price moves down
                
                if current_sl == 0.0:
                    update_sl(pos, new_sl)
                else:
                    if current_sl != new_sl and new_sl < current_sl:
                        update_sl(pos, new_sl)
                        pass  # Successfully updated SL



def close_strategy_orders1(symbol):

    positions = mt5.positions_get(symbol=symbol)
    if positions is None:
        print("No positions found. Error code:", mt5.last_error())
        return False

    # Close all positions one by one
    for position in positions:
        order_type = mt5.ORDER_TYPE_BUY if position.type == mt5.ORDER_TYPE_BUY else mt5.ORDER_TYPE_SELL
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": position.volume,
            "type": mt5.ORDER_TYPE_SELL if order_type == mt5.ORDER_TYPE_BUY else mt5.ORDER_TYPE_BUY,
            "position": position.ticket,
            "price": mt5.symbol_info_tick(symbol).ask if order_type == mt5.ORDER_TYPE_BUY else mt5.symbol_info_tick(symbol).bid,
            "deviation": 20,
            # "magic": magic_number,  # Use the same magic number for tracking
            "comment": "Closing strategy position",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        result = mt5.order_send(request)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print(f"Failed to close position {position.ticket}. Error code: {result.retcode}")
            return False
        else:
            print(f"Closed position {position.ticket} successfully.")
    return True


def close_orphan_orders(symbol, buy_ind, sell_ind, bob_ind, bos_ind):
    # Get all open positions for the given symbol
    positions = mt5.positions_get(symbol=symbol)
    if positions is None or len(positions) == 0:
        print("No open positions found.")
        return

    buy_orders = [pos for pos in positions if pos.magic == 1001]
    sell_orders = [pos for pos in positions if pos.magic == 2001]

   
    # Process Buy Orders (0.01) & their Hedge Orders (opposite qty Sell)
    buy_pos_tot = sum(pos.volume for pos in positions if pos.magic == 1001 and pos.type == mt5.ORDER_TYPE_BUY)
    sell_pos_tot = sum(pos.volume for pos in positions if pos.magic == 2001 and pos.type == mt5.ORDER_TYPE_SELL)

    buy_count = round(buy_pos_tot - sell_pos_tot, 2)
    sell_count = round(sell_pos_tot - buy_pos_tot, 2)

    if buy_orders:
        if buy_count >= 0.01:
            for order in buy_orders:
                if order.profit >= 3:
                    close_order(order, symbol)


    if sell_orders:
        if sell_count >= 0.01:
            for order in sell_orders:
                if order.profit >= 3:
                    close_order(order, symbol)

     
def close_order(position, symbol):
    """Function to close a specific order in MT5"""

    # Get latest symbol tick
    tick_info = mt5.symbol_info_tick(symbol)
    if tick_info is None:
        print(f"Could not retrieve tick info for {symbol}")
        return False

    # Validate volume
    if position.volume <= 0:
        print(f"Invalid volume {position.volume} for order {position.ticket}")
        return False

    # Get correct price for closing the position
    if position.type == mt5.ORDER_TYPE_BUY:
        close_price = tick_info.ask  # Close Buy orders at Bid price
    else:
        close_price = tick_info.bid  # Close Sell orders at Ask price

    # Prepare close request
    close_request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": float(position.volume),  # Ensure volume is a float
        "type": mt5.ORDER_TYPE_SELL if position.type == mt5.ORDER_TYPE_BUY else mt5.ORDER_TYPE_BUY,  # Opposite order type
        "position": position.ticket,
        "price": close_price,  # Correct closing price
        "deviation": 20,  # Increase deviation to allow for price fluctuations
        "magic": position.magic,  # Ensure correct magic number
        "comment": "Auto-close",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    # Send close request
    result = mt5.order_send(close_request)

    if result is None:
        print(f"Order send failed for {position.ticket}: {mt5.last_error()}")
        return False
    elif result.retcode != mt5.TRADE_RETCODE_DONE:
        print(f" Failed to close order {position.ticket}. Error: {result.retcode} vol: {position.volume} type: {position.type} magic: {position.magic}")
        return False
    else:
        print(f" Order {position.ticket} closed successfully with profit: {position.profit}")
        return True


def get_last_closed_15m_candle(symbol):
    rates = mt5.copy_rates_from_pos(
        symbol,
        mt5.TIMEFRAME_M15,
        1,      # ← VERY IMPORTANT: 1 = last CLOSED candle
        1
    )

    if rates is None or len(rates) == 0:
        return None

    return rates[0]

def upper_wick_rejection_15m(symbol, wick_ratio=1.5):
    c = get_last_closed_15m_candle(symbol)
    if c is None:
        return False

    open_  = c["open"]
    high   = c["high"]
    low    = c["low"]
    close  = c["close"]

    # MUST be bearish candle
    if close >= open_:
        return False

    body = abs(close - open_)
    if body == 0:
        return False

    upper_wick = high - max(open_, close)
    lower_wick = min(open_, close) - low

    # Reject indecision candles
    if upper_wick >= body * wick_ratio and lower_wick >= body * wick_ratio:
        return False

    return upper_wick >= body * wick_ratio

def lower_wick_rejection_15m(symbol, wick_ratio=1.5):
    c = get_last_closed_15m_candle(symbol)
    if c is None:
        return False

    open_  = c["open"]
    high   = c["high"]
    low    = c["low"]
    close  = c["close"]

    # MUST be bullish candle
    if close <= open_:
        return False

    body = abs(close - open_)
    if body == 0:
        return False

    upper_wick = high - max(open_, close)
    lower_wick = min(open_, close) - low

    # Reject indecision candles
    if upper_wick >= body * wick_ratio and lower_wick >= body * wick_ratio:
        return False

    return lower_wick >= body * wick_ratio

def bullish_engulf_after_m15_lower_bb(
    symbol,
    lower_bb_value,
    max_m5_candles=5
):
    """
    Returns True if:
    1) Last CLOSED M15 candle touched lower Bollinger Band
    2) Within next N M5 candles, a bullish engulfing appears
    """

    # -----------------------------
    # 1️⃣ Get last CLOSED M15 candle
    # -----------------------------
    m15_rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M15, 1, 1)
    if m15_rates is None or len(m15_rates) == 0:
        return False

    m15 = m15_rates[0]

    # Check BB touch
    if m15['low'] > lower_bb_value:
        return False  # No BB touch → stop here

    m15_close_time = datetime.fromtimestamp(m15['time'])

    # -----------------------------
    # 2️⃣ Fetch M5 candles AFTER M15 close
    # -----------------------------
    m5_rates = mt5.copy_rates_from(
        symbol,
        mt5.TIMEFRAME_M5,
        m15_close_time,
        max_m5_candles + 1
    )

    if m5_rates is None or len(m5_rates) < 2:
        return False

    # -----------------------------
    # 3️⃣ Scan for bullish engulfing
    # -----------------------------
    for i in range(1, len(m5_rates)):
        prev = m5_rates[i - 1]
        curr = m5_rates[i]

        # Previous bearish
        if prev['close'] >= prev['open']:
            continue

        # Current bullish
        if curr['close'] <= curr['open']:
            continue

        # Body engulfing
        if (
            curr['open'] <= prev['close'] and
            curr['close'] >= prev['open'] and
            curr['close'] > prev['high']
        ):
            return True  # ✅ CONFIRMED

    return False


def bearish_engulf_after_m15_upper_bb(
    symbol,
    upper_bb_value,
    max_m5_candles=5
):
    """
    Returns True if:
    1) Last CLOSED M15 candle touched upper Bollinger Band
    2) Within next N M5 candles, a bearish engulfing appears
    """

    # -----------------------------
    # 1️⃣ Get last CLOSED M15 candle
    # -----------------------------
    m15_rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M15, 1, 1)
    if m15_rates is None or len(m15_rates) == 0:
        return False

    m15 = m15_rates[0]

    # Check BB touch
    if m15['high'] < upper_bb_value:
        return False  # No BB touch → stop here

    m15_close_time = datetime.fromtimestamp(m15['time'])

    # -----------------------------
    # 2️⃣ Fetch M5 candles AFTER M15 close
    # -----------------------------
    m5_rates = mt5.copy_rates_from(
        symbol,
        mt5.TIMEFRAME_M5,
        m15_close_time,
        max_m5_candles + 1
    )

    if m5_rates is None or len(m5_rates) < 2:
        return False

    # -----------------------------
    # 3️⃣ Scan for bearish engulfing
    # -----------------------------
    for i in range(1, len(m5_rates)):
        prev = m5_rates[i - 1]
        curr = m5_rates[i]

        # Previous bullish
        if prev['close'] <= prev['open']:
            continue

        # Current bearish
        if curr['close'] >= curr['open']:
            continue

        # Body engulfing + momentum
        if (
            curr['open'] >= prev['close'] and
            curr['close'] <= prev['open'] and
            curr['close'] < prev['low']
        ):
            return True  # ✅ SELL CONFIRMED

    return False


def place_general_orders_buy_sell(symbol, final_trend):

    changing_to_bullish = False
    changing_to_bearish = False
    block_new_sell_orders = False
    block_new_buy_orders = False
    block_new_sell_orders1 = False
    block_new_buy_orders1 = False
    allow_buy_orders = False
    allow_sell_orders = False
    allow_buy_orders1 = False
    allow_sell_orders1 = False
    m5_trend = m15_trend = h1_trend = "RANGE"

    buy_price = mt5.symbol_info_tick(symbol).ask
    sell_price = mt5.symbol_info_tick(symbol).bid
    point1 = mt5.symbol_info(symbol).point

    # print(f"point value is - {point1}")
    # Retrieve all open positions for the symbol
    positions = mt5.positions_get(symbol=symbol)

    # ========== GET Bollinger bands DATA ==========
    df_15m_data = get_mt5_data(symbol, mt5.TIMEFRAME_M15, NUM_CANDLES)
    df_15m_bb = add_bollinger_bands(df_15m_data)
    price_15m, upper_band_15m, lower_band_15m, middle_band_15m = detect_band_touch(df_15m_bb, "15-Minute")
    bb_gap = round(upper_band_15m - lower_band_15m, 0)

    bb15m_tolerance = round(bb_gap * 0.2, 0)
    # print(f"15 min price, upper, lower and Middle levels are - {price_15m}, {upper_band_15m:.2f}, {lower_band_15m:.2f}, {middle_band_15m:.2f}")

    # df_1h_data = get_mt5_data(symbol, mt5.TIMEFRAME_H1, NUM_CANDLES)
    # df_1h_bb = add_bollinger_bands(df_1h_data)
    # price_1h, upper_band_1h, lower_band_1h, middle_band_1h = detect_band_touch(df_1h_bb, "1-Hour")
    # print(f"1 hour price, upper, lower and Middle levels are - {price_1h}, {upper_band_1h:.2f}, {lower_band_1h:.2f}, {middle_band_1h:.2f}")


    rates = mt5.copy_rates_from_pos("XAUUSD", mt5.TIMEFRAME_H1, 0, 500)
    df = pd.DataFrame(rates)

    df = support_resistance_with_breaks(df)

    latest = df.iloc[-1]


    sell_now_confirmed = upper_wick_rejection_15m(symbol)
    buy_now_confirmed  = lower_wick_rejection_15m(symbol)


    # print("──────── H1 STRUCTURE ────────")
    # print(f"Support     : {latest['support']:.2f}")
    # print(f"Resistance  : {latest['resistance']:.2f}")

    # if latest['break_resistance']:
    #     print("🔥 Resistance broken with volume")

    # if latest['break_support']:
    #     print("🔻 Support broken with volume")

    # if latest['bull_wick']:
    #     print("Bull wick rejection")

    # if latest['bear_wick']:
    #     print("Bear wick rejection")

    # print(f"Active Support: {latest['active_support']:.2f}, Active Resistance: {latest['active_resistance']:.2f}, latest bull wick: {latest['bull_wick']}, latest bear wick: {latest['bear_wick']}")

# ========== Bollinger bands  & SR calculation
    # rates_1h = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_H1, 0, 100)
    # df_1h = pd.DataFrame(rates_1h)
    # df_1h_bb = add_bollinger_bands(df_1h)
    # rates_5m = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M5, 0, 200)
 
    # df_5m = pd.DataFrame(rates_5m)
    df_5m_rsi = calculate_rsi(df_15m_data.copy())
    rsi = round(df_5m_rsi['RSI'].iloc[-1], 0)

    # df_5m_data = get_mt5_data(symbol, mt5.TIMEFRAME_M5, NUM_CANDLES)
    # df_5m_break = get_mt5_data(symbol, mt5.TIMEFRAME_M5, NUM_CANDLES)
    # df_5m_bb = add_bollinger_bands(df_5m_data)

    # price, upper_band, lower_band = detect_band_touch(df_1h_bb, "1-Hour")
    # price, upper_band, lower_band, middle_band = detect_band_touch(df_1h_bb, "1-Hour")
    # band_diff = round(upper_band - lower_band, 2)

    # support,resistance = detect_support_resistance_levels(symbol)
    # print(f"price, upper, lower and Middle levels are - {price}, {upper_band:.2f}, {lower_band:.2f}, {middle_band:.2f}")

    # buy_ind, sell_ind, bob_ind, bos_ind = monitor_and_confirm(symbol, upper_band, lower_band, support, resistance)
    # print(f"buy, sell and breakout signals are - {buy_ind}, {sell_ind}, {bob_ind}, {bos_ind} and RSI is {rsi}")
    # monitor_and_place_new_orders(symbol, buy_magic_num, sell_magic_num)
# ========== Bollinger bands & SR calculation

# ========= GET MACD TRENDS DATA ========== 
    m5_trend, m5_macd = get_macd_trend(symbol, mt5.TIMEFRAME_M5)
    m15_trend, m15_macd = get_macd_trend(symbol, mt5.TIMEFRAME_M15)
    h1_trend, h1_macd = get_macd_trend(symbol, mt5.TIMEFRAME_H1)

    # is_volatile = is_high_volatility_bar(symbol)
    high_vol, direction = is_high_volatility_bar(symbol)
    signal = bb_momentum_exit_signal(symbol)

    buy_conf = bullish_engulf_after_m15_lower_bb(symbol,lower_bb_value=lower_band_15m,max_m5_candles=5)
    sell_conf = bearish_engulf_after_m15_upper_bb(symbol,upper_bb_value=upper_band_15m,max_m5_candles=5)

    h1_reversal, reversal_type = detect_h1_reversal(symbol)
    # print(f"M5: {m5_trend} ({m5_macd:.5f}), M15: {m15_trend} ({m15_macd:.5f}), H1: {h1_trend} ({h1_macd:.5f}), Rev: {h1_reversal}, Type: {reversal_type}, RSI: {rsi}, buy: {buy_now_confirmed}, sell: {sell_now_confirmed}, bb_gap: {bb_gap}, direc: {direction}, sig: {signal}")
    print(f" final_trend: {final_trend}, M5: {m5_trend}, M15: {m15_trend}, H1: {h1_trend}, Rev: {h1_reversal}, Type: {reversal_type}, RSI: {rsi}, bb_gap: {bb_gap}, direc: {direction}, sig: {signal}, buy_conf: {buy_conf}, sell_conf: {sell_conf}")


    if h1_reversal:
        if reversal_type == "BULLISH":
            changing_to_bullish = True
        elif reversal_type == "BEARISH":
            changing_to_bearish = True

    if h1_trend == "BUY" and m15_trend == "BUY":
        block_new_sell_orders = True
        allow_buy_orders = True
    elif h1_trend == "SELL" and m15_trend == "SELL":
        block_new_buy_orders = True
        allow_sell_orders = True

    # if m5_trend == "BUY" and m15_trend == "BUY":
    #     block_new_sell_orders1 = True
    #     allow_buy_orders1 = True
    # elif m5_trend == "SELL" and m15_trend == "SELL":
    #     block_new_buy_orders1 = True
    #     allow_sell_orders1 = True



    close_orders_based_on_conditions(symbol, price_15m, upper_band_15m, lower_band_15m, middle_band_15m, allow_buy_orders, allow_sell_orders, m5_trend, m15_trend, h1_trend, signal, final_trend)

    buy_positions = sorted([pos for pos in positions if pos.type == mt5.ORDER_TYPE_BUY],key=lambda x: x.time,reverse=True)
    sell_positions = sorted([pos for pos in positions if pos.type == mt5.ORDER_TYPE_SELL],key=lambda x: x.time,reverse=True)


    martingale_buy_positions = sorted([pos for pos in positions if pos.type == mt5.ORDER_TYPE_BUY and pos.magic == martingale_buy_magic],key=lambda x: x.time,reverse=True)
    martingale_sell_positions = sorted([pos for pos in positions if pos.type == mt5.ORDER_TYPE_SELL and pos.magic == martingale_sell_magic],key=lambda x: x.time,reverse=True)

    trend_buy_positions = sorted([pos for pos in positions if pos.type == mt5.ORDER_TYPE_BUY and pos.magic == trend_buy_magic],key=lambda x: x.time,reverse=True)
    trend_sell_positions = sorted([pos for pos in positions if pos.type == mt5.ORDER_TYPE_SELL and pos.magic == trend_sell_magic],key=lambda x: x.time,reverse=True)

    bb15m_buy_positions = sorted([pos for pos in positions if pos.type == mt5.ORDER_TYPE_BUY and pos.magic == bb_buy_magic],key=lambda x: x.time,reverse=True)
    bb15m_sell_positions = sorted([pos for pos in positions if pos.type == mt5.ORDER_TYPE_SELL and pos.magic == bb_sell_magic],key=lambda x: x.time,reverse=True)

    direc_buy_positions = sorted([pos for pos in positions if pos.type == mt5.ORDER_TYPE_BUY and pos.magic == direc_buy_magic],key=lambda x: x.time,reverse=True)
    direc_sell_positions = sorted([pos for pos in positions if pos.type == mt5.ORDER_TYPE_SELL and pos.magic == direc_sell_magic],key=lambda x: x.time,reverse=True)

    signal_buy_positions = sorted([pos for pos in positions if pos.type == mt5.ORDER_TYPE_BUY and pos.magic == signal_buy_magic],key=lambda x: x.time,reverse=True)
    signal_sell_positions = sorted([pos for pos in positions if pos.type == mt5.ORDER_TYPE_SELL and pos.magic == signal_sell_magic],key=lambda x: x.time,reverse=True)


    martingale_buy_order_index = len(martingale_buy_positions)
    martingale_sell_order_index = len(martingale_sell_positions)

    # print(f"middle band value is - {middle_band_15m - 2}")

    # if not martingale_buy_positions and not martingale_sell_positions and not trend_buy_positions and not trend_sell_positions:
    if not is_trading_allowed_uk(symbol):
        if buy_positions or sell_positions:
            print(f"no trading - {mt5_server_time(symbol)} - Closing all open orders now")
            close_strategy_orders1(symbol)
            return
        else:   
            return
    # else:
    #     print(f"trading started now - {mt5_server_time(symbol)}")

    # if is_gold_trading_allowed(symbol) and bb_gap < 60:
    if bb_gap < 100:
        if not martingale_buy_positions:    
            martingale_buy_order_qty = martingale_lot_sizes[0]
            # if buy_price <= lower_band_15m and not block_new_buy_orders and not changing_to_bearish and rsi < 50 and bb_gap < 50:  # Initial buy condition
            # if buy_price <= lower_band_15m + bb15m_lower_tolerance and rsi < 50 and bb_gap < 50 and m5_trend != "SELL":  # Initial buy condition
            if buy_price <= lower_band_15m + 5:  # Initial buy condition
                if final_trend == "SELL" or direction == "DOWN" or rsi > sell_rsi or signal == "EXIT_BUY":
                    pass
                else:
                    place_buy_order(symbol, martingale_buy_order_qty, martingale_buy_magic)
                    print(f"MACD Trends - M5: {m5_trend} ({m5_macd:.5f}), M15: {m15_trend} ({m15_macd:.5f}), H1: {h1_trend} ({h1_macd:.5f}) - H1 Reversal: {h1_reversal}, Type: {reversal_type}, RSI: {rsi}, Supp: {latest['active_support']}, Res: {latest['active_resistance']}")
        else:
            latest_buy_position_price = martingale_buy_positions[0].price_open
            martingale_buy_order_qty = martingale_lot_sizes[martingale_buy_order_index] if martingale_buy_order_index < len(martingale_lot_sizes) else martingale_lot_sizes[-1]
            if buy_price <= latest_buy_position_price - diff_pips * mt5.symbol_info(symbol).point:
                # if not block_new_buy_orders and not changing_to_bearish:
                if final_trend == "SELL" or direction == "DOWN" or rsi > sell_rsi or signal == "EXIT_BUY":
                    pass
                else:
                    place_buy_order(symbol, martingale_buy_order_qty, martingale_buy_magic)
                    print(f"MACD Trends - M5: {m5_trend} ({m5_macd:.5f}), M15: {m15_trend} ({m15_macd:.5f}), H1: {h1_trend} ({h1_macd:.5f}) - H1 Reversal: {h1_reversal}, Type: {reversal_type}, RSI: {rsi}, Supp: {latest['active_support']}, Res: {latest['active_resistance']}")

        if not martingale_sell_positions:
            martingale_sell_order_qty = martingale_lot_sizes[0]
            # if sell_price >= upper_band_15m and not block_new_sell_orders and not changing_to_bullish and rsi > 50:  # Initial sell condition
            # if sell_price >= upper_band_15m - bb15m_upper_tolerance and rsi > 50 and bb_gap < 50 and m5_trend != "BUY":  # Initial sell condition
            if sell_price >= upper_band_15m - 5:  # Initial sell condition
                if final_trend == "BUY" or  direction == "UP" or rsi < buy_rsi or signal == "EXIT_SELL":
                    pass
                else:
                    place_sell_order(symbol, martingale_sell_order_qty, martingale_sell_magic)
                    print(f"MACD Trends - M5: {m5_trend} ({m5_macd:.5f}), M15: {m15_trend} ({m15_macd:.5f}), H1: {h1_trend} ({h1_macd:.5f}) - H1 Reversal: {h1_reversal}, Type: {reversal_type}, RSI: {rsi}, Supp: {latest['active_support']}, Res: {latest['active_resistance']}")
        else:
            latest_sell_position_price = martingale_sell_positions[0].price_open
            martingale_sell_order_qty = martingale_lot_sizes[martingale_sell_order_index] if martingale_sell_order_index < len(martingale_lot_sizes) else martingale_lot_sizes[-1]
            if sell_price >= latest_sell_position_price + diff_pips * mt5.symbol_info(symbol).point:
                # if not block_new_sell_orders and not changing_to_bullish:
                if final_trend == "BUY" or  direction == "UP"  or rsi < buy_rsi or signal == "EXIT_SELL":
                    pass
                else:
                    place_sell_order(symbol, martingale_sell_order_qty, martingale_sell_magic)
                    print(f"MACD Trends - M5: {m5_trend} ({m5_macd:.5f}), M15: {m15_trend} ({m15_macd:.5f}), H1: {h1_trend} ({h1_macd:.5f}) - H1 Reversal: {h1_reversal}, Type: {reversal_type}, RSI: {rsi}, Supp: {latest['active_support']}, Res: {latest['active_resistance']}")


    # if not trend_buy_positions:    
    #     martingale_buy_order_qty = martingale_lot_sizes[0]
    #     if final_trend == "BUY" and rsi < 70 and bb_gap > 30 and (signal == "EXIT_SELL" or direction == "UP"):  # Initial buy condition
    #         place_buy_order(symbol, martingale_buy_order_qty, trend_buy_magic)
    #         print(f"MACD Trends - final trend is: {final_trend} H1 Reversal: {h1_reversal}, Type: {reversal_type}, RSI: {rsi}, Supp: {latest['active_support']}, Res: {latest['active_resistance']}")
    # if not trend_sell_positions:
    #     martingale_sell_order_qty = martingale_lot_sizes[0]
    #     if final_trend == "SELL" and rsi > 30 and bb_gap > 30 and (signal == "EXIT_BUY" or direction == "DOWN"):  # Initial sell condition
    #         place_sell_order(symbol, martingale_sell_order_qty, trend_sell_magic)
    #         print(f"MACD Trends - final trend is: {final_trend} H1 Reversal: {h1_reversal}, Type: {reversal_type}, RSI: {rsi}, Supp: {latest['active_support']}, Res: {latest['active_resistance']}")

    # if not direc_buy_positions:    
    #     martingale_buy_order_qty = martingale_lot_sizes[0]
    #     if rsi < 70 and bb_gap > 30 and direction == "UP":  # Initial buy condition
    #         place_buy_order(symbol, martingale_buy_order_qty,direc_buy_magic)
    #         print(f"MACD Trends - final trend is: {final_trend} H1 Reversal: {h1_reversal}, Type: {reversal_type}, RSI: {rsi}, Supp: {latest['active_support']}, Res: {latest['active_resistance']}")
    # if not direc_sell_positions:
    #     martingale_sell_order_qty = martingale_lot_sizes[0]
    #     if rsi > 30 and bb_gap > 30 and direction == "DOWN":  # Initial sell condition
    #         place_sell_order(symbol, martingale_sell_order_qty, direc_sell_magic)
    #         print(f"MACD Trends - final trend is: {final_trend} H1 Reversal: {h1_reversal}, Type: {reversal_type}, RSI: {rsi}, Supp: {latest['active_support']}, Res: {latest['active_resistance']}")


    # if not signal_buy_positions:    
    #     martingale_buy_order_qty = martingale_lot_sizes[0]
    #     if rsi < 70 and bb_gap > 30 and signal == "EXIT_SELL":  # Initial buy condition
    #         place_buy_order(symbol, martingale_buy_order_qty, signal_buy_magic)
    #         print(f"MACD Trends - final trend is: {final_trend} H1 Reversal: {h1_reversal}, Type: {reversal_type}, RSI: {rsi}, Supp: {latest['active_support']}, Res: {latest['active_resistance']}")
    # if not signal_sell_positions:
    #     martingale_sell_order_qty = martingale_lot_sizes[0]
    #     if rsi > 30 and bb_gap > 30 and signal == "EXIT_BUY":  # Initial sell condition
    #         place_sell_order(symbol, martingale_sell_order_qty, signal_sell_magic)
    #         print(f"MACD Trends - final trend is: {final_trend} H1 Reversal: {h1_reversal}, Type: {reversal_type}, RSI: {rsi}, Supp: {latest['active_support']}, Res: {latest['active_resistance']}")



def get_equity(symbol):
        account_info = mt5.account_info()
        if account_info is None:
            return None
        return account_info.equity



# Function to manage the Martingale strategy
def martingale_strategy(symbol):
    global target_balance


    start_balance = get_equity(symbol)
    target_balance = start_balance + profit_target
    print(f"star and target balances are {start_balance}, {target_balance}")
    trend_filter = TrendStabilizer(confirm_count=10)

    while True:

        m5_trend, m5_macd = get_macd_trend(symbol, mt5.TIMEFRAME_M5)
        m15_trend, m15_macd = get_macd_trend(symbol, mt5.TIMEFRAME_M15)
        h1_trend, h1_macd = get_macd_trend(symbol, mt5.TIMEFRAME_H1)

        final_trend = trend_filter.update(m5_trend, m15_trend, h1_trend)

        place_general_orders_buy_sell(symbol, final_trend)
        
        # Sleep to avoid excessive API calls
        pytime.sleep(5)


# Start the Martingale strategy
martingale_strategy(symbol)

# Shutdown the connection (unreachable in infinite loop above)
mt5.shutdown()

