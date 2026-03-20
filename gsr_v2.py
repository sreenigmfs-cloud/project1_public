import MetaTrader5 as mt5
import time
import pandas as pd
import numpy as np
from datetime import datetime

"""
risk managed program
"""

# Initialize connection to MetaTrader 5
if not mt5.initialize():
    print("Initialize failed, error code =", mt5.last_error())
    mt5.shutdown()
    exit()

diff_pips = 1200
profit_pips = 2000
special_magic_num = 555
profit_target = 100


lot_sizes = [0.01] * 200

# lot_sizes = [0.01, 0.01, 0.01, 0.01, 0.02, 
#              0.01, 0.01, 0.01, 0.01, 0.02, 
#              0.01, 0.01, 0.01, 0.01, 0.02,
#              0.01, 0.01, 0.01, 0.01, 0.02,
#              0.01, 0.01, 0.01, 0.01, 0.02,
#              0.01, 0.01, 0.01, 0.01, 0.02,
#              0.01, 0.01, 0.01, 0.01, 0.02,
#              0.01, 0.01, 0.01, 0.01, 0.02,
#              0.01, 0.01, 0.01, 0.01, 0.02,
#              0.01, 0.01, 0.01, 0.01, 0.02,
#              0.01, 0.01, 0.01, 0.01, 0.02]
 
buy_order_qty = 0
sell_order_qty = 0
latest_position_price = 0

buy_ctr = 0
sell_ctr = 0

pips_30 = 30
pips_50 = 50
pips_150 = 150
pips_200 = 200
pips_250 = 250
pips_300 = 300
pips_350 = 350
pips_400 = 400
pips_450 = 450
pips_500 = 500
pips_600 = 600
pips_650 = 650
pips_700 = 700
pips_800 = 800
pips_1000 = 1000
pips_1200 = 1200

change_pips_for_sl_50 = 50
change_pips_for_sl_150 = 150
change_pips_for_sl_200 = 200
change_pips_for_sl_250 = 250
change_pips_for_sl_300 = 300
change_pips_for_sl_350 = 350
change_pips_for_sl_400 = 400
change_pips_for_sl_450 = 450
change_pips_for_sl_500 = 500
change_pips_for_sl_550 = 550
change_pips_for_sl_600 = 600
change_pips_for_sl_650 = 650
change_pips_for_sl_700 = 700
change_pips_for_sl_750 = 750
change_pips_for_sl_850 = 850
change_pips_for_sl_900 = 900
change_pips_for_sl_950 = 950
change_pips_for_sl_1000 = 1000
change_pips_for_sl_1400 = 1400
change_pips_for_sl_1500 = 1550
change_pips_for_sl_2000 = 2050
change_pips_for_sl_3000 = 3050
change_pips_for_sl_4000 = 4050
change_pips_for_sl_5000 = 5050
change_pips_for_sl_6000 = 6050
change_pips_for_sl_7000 = 7050
change_pips_for_sl_8000 = 8050
change_pips_for_sl_9000 = 9050

buy_magic_num = 1001
sell_magic_num = 2001
magic_num_24 = 24

small_qty = 0.01
opposite_qty01 = 0.01
opposite_qty02 = 0.02
opposite_qty03 = 0.03
opposite_qty04 = 0.04
opposite_qty05 = 0.05
opposite_qty06 = 0.06
opposite_qty07 = 0.07
opposite_qty08 = 0.08
opposite_qty09 = 0.09
opposite_qty10 = 0.10
opposite_qty11 = 0.11
opposite_qty12 = 0.12
opposite_qty13 = 0.13
opposite_qty14 = 0.14
opposite_qty15 = 0.15
opposite_qty16 = 0.16
opposite_qty17 = 0.17
opposite_qty18 = 0.18
opposite_qty19 = 0.19
opposite_qty20 = 0.20
opposite_qty25 = 0.25
opposite_qty30 = 0.30
opposite_qty35 = 0.35
opposite_qty45 = 0.45

buy_order_index = 0
sell_order_index = 0

buy_series = [100, 101, 102, 103, 104, 105]
sell_series = [200, 201, 202, 203, 204, 205]

def get_current_equity():
    account_info = mt5.account_info()
    if account_info is not None:
        return account_info.equity
    else:
        print("Failed to retrieve account info.")
        return None
    
# Function to place a buy order
def place_buy_order(symbol, buy_order_qty, magic_num):

    positions = mt5.positions_get(symbol=symbol)
    # buy_hedge_05 = [pos for pos in positions if pos.magic == 1001 and pos.volume == opposite_qty05]

    # buy_hedge_09 = [pos for pos in positions if pos.magic == 1001 and pos.volume == opposite_qty09]
    # buy_hedge_12 = [pos for pos in positions if pos.magic == 1001 and pos.volume == opposite_qty12]
    # buy_hedge_13 = [pos for pos in positions if pos.magic == 1001 and pos.volume == opposite_qty13]
    # buy_hedge_15 = [pos for pos in positions if pos.magic == 1001 and pos.volume == opposite_qty15]

    # buy_total = sum(order.volume for order in positions if order.type == mt5.ORDER_TYPE_BUY)
    # sell_total = sum(order.volume for order in positions if order.type == mt5.ORDER_TYPE_SELL)
    # print(f" buy and sell orders totals : {round(buy_total, 2)},  {round(sell_total, 2)}  Net is: {round(buy_total - sell_total, 2)}")

    # Get the current price for the symbol
    price = mt5.symbol_info_tick(symbol).ask
    if price == 0:
        print(f"Error retrieving price for {symbol}.")
        return

    tp = price + profit_pips * mt5.symbol_info(symbol).point
    # Prepare the order request for buy
    if buy_order_qty in lot_sizes and magic_num == 1001:

        order = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": buy_order_qty,
            "type": 0,  # Buy order type
            "price": price,
            "tp": tp,
            # "sl": buy_sl,
            "deviation": 20,  # Slippage
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
            # "tp": tp,
            # "sl": sl,
            "deviation": 20,  # Slippage
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

        # if buy_order_qty in lot_sizes:
        #     print(f"update buy is enabled and bq is: {buy_order_qty}")    
        #     update_common_tp_for_buy(symbol, magic_num)
            
        # if round(buy_total - sell_total, 2) > 0.10:
        #     place_sell_order(symbol, opposite_qty01, special_magic_num)


# Function to place a sell order
def place_sell_order(symbol, sell_order_qty, magic_num):

    print(f"sell magic number is : {magic_num}")
    positions = mt5.positions_get(symbol=symbol)

    # sell_hedge_05 = [pos for pos in positions if pos.magic == 2001 and pos.volume == opposite_qty05]

    # sell_hedge_09 = [pos for pos in positions if pos.magic == 2001 and pos.volume == opposite_qty09]
    # sell_hedge_12 = [pos for pos in positions if pos.magic == 2001 and pos.volume == opposite_qty12]
    # sell_hedge_13 = [pos for pos in positions if pos.magic == 2001 and pos.volume == opposite_qty13]
    # sell_hedge_15 = [pos for pos in positions if pos.magic == 2001 and pos.volume == opposite_qty15]

    # buy_total = sum(order.volume for order in positions if order.type == mt5.ORDER_TYPE_BUY)
    # sell_total = sum(order.volume for order in positions if order.type == mt5.ORDER_TYPE_SELL)
    # print(f" buy and sell orders totals : {round(buy_total, 2)},  {round(sell_total, 2)}  Net is: {round(buy_total - sell_total, 2)}")


    price = mt5.symbol_info_tick(symbol).bid
    if price is None:
        print("Error retrieving bid price.")
        return

    # Target price (TP) set 150 points above current price
    tp = price - profit_pips * mt5.symbol_info(symbol).point
    # sl = price + sl_pips * mt5.symbol_info(symbol).point

    # if sell_order_qty == opp_qty:
    # sl = get_latest_buy_tp(symbol, magic_num)

    if sell_order_qty in lot_sizes and magic_num == 2001:

        # Prepare the sell order request
        sell_order = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": sell_order_qty,
            "type": 1,  # Sell order type
            "price": price,
            # "sl": sell_sl,
            "tp": tp,
            "deviation": 20,  # Slippage
            "magic": magic_num,
            "comment": "sell",
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
    else:
        # Prepare the sell order request
        sell_order = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": sell_order_qty,
            "type": 1,  # Sell order type
            "price": price,
            # "sl": sl,
            # "tp": tp,
            "deviation": 20,  # Slippage
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

        # if sell_order_qty in lot_sizes:
        #     print(f"update sell is enabled sq is: {sell_order_qty}")    
        #     update_common_tp_for_sell(symbol, magic_num)

        # if round(sell_total - buy_total, 2) > 0.10:
        #     place_buy_order(symbol, opposite_qty01, special_magic_num)


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
                     and pos.magic == buy_magic_num]

    if not buy_positions:
        print("No buy positions to update TP.")
        return

    total_volume = sum(pos.volume for pos in buy_positions)
    weighted_sum_price = sum(pos.price_open * pos.volume for pos in buy_positions)

    if total_volume == 0:
        print(f"total volume is zero. no can't calculate avg price")
        return

    avg_buy_price = weighted_sum_price / total_volume
    buy_tp_price_common = avg_buy_price + pips_250 * mt5.symbol_info(symbol).point
    buy_tp_price_single = get_latest_buy_tp(symbol, magic_num)

    if len(buy_positions) <= 3:
        buy_tp_price = buy_tp_price_common
    else:
        buy_tp_price = buy_tp_price_single

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
                      and pos.magic == sell_magic_num]
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
    sell_tp_price_common = avg_sell_price - pips_250 * mt5.symbol_info(symbol).point
    sell_tp_price_single = get_latest_sell_tp(symbol, magic_num)

    if len(sell_positions) <= 3:
        sell_tp_price = sell_tp_price_common
    else:
        sell_tp_price = sell_tp_price_single

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

def close_orders_based_on_conditions(symbol, buy_magic_num, sell_magic_num):
    global target_balance, my_equity

    # Get all positions for the symbol
    positions = mt5.positions_get(symbol=symbol)
    if not positions:
        print(f"No positions found for {symbol}.")
        return

    conditions_1 = [
        (1, 10)
    ]

    total_profit = sum(pos.profit for pos in positions)
    total_positions = len(positions)

    for count_max, profit_max in conditions_1:
         if total_positions >= count_max and total_profit >= profit_max:
            print(f"closing all orders by taking min profit of 10")
            close_strategy_orders1(symbol)


    buy_price = mt5.symbol_info_tick(symbol).ask
    sell_price = mt5.symbol_info_tick(symbol).bid
    current_price = mt5.symbol_info_tick(symbol).ask
    
# scenario 1 -- begins
    current_equity = get_equity(symbol)


    if current_equity >= my_equity + 100:
        close_strategy_orders1(symbol)


    if current_equity >= target_balance:

        print(f"before clearing current equity and target balances are {current_equity}, {target_balance}")
        my_equity = current_equity
        target_balance = current_equity + profit_target
        close_strategy_orders1(symbol)
        print(f"After clearing current equity and target balances are {current_equity}, {target_balance}")
# scenario 1 -- end


    buy_total = sum(order.volume for order in positions if order.type == mt5.ORDER_TYPE_BUY)
    sell_total = sum(order.volume for order in positions if order.type == mt5.ORDER_TYPE_SELL)
    print(f" buy and sell orders totals : {round(buy_total, 2)},  {round(sell_total, 2)}  Net is: {round(buy_total - sell_total, 2)}")


    spl_buy_positions = sorted(
        [pos for pos in positions if pos.type == mt5.ORDER_TYPE_BUY and pos.magic == special_magic_num],
        key=lambda x: x.time,
        reverse=True
    )

    spl_sell_positions = sorted(
        [pos for pos in positions if pos.type == mt5.ORDER_TYPE_SELL and pos.magic == special_magic_num],
        key=lambda x: x.time,
        reverse=True
    )

    if round(buy_total - sell_total, 2) > 0.03:
        if can_place_new_sell(sell_price, spl_sell_positions, buffer_points=6.0):
            place_sell_order(symbol, opposite_qty01, special_magic_num)

    if round(sell_total - buy_total, 2) > 0.03:
        if can_place_new_buy(buy_price, spl_buy_positions, buffer_points=6.0):
            place_buy_order(symbol, opposite_qty01, special_magic_num)

        
 
def get_buy_price_range(buy_positions):
    if not buy_positions:
        return None, None

    prices = [pos.price_open for pos in buy_positions]
    return min(prices), max(prices)

def get_sell_price_range(sell_positions):
    if not sell_positions:
        return None, None

    prices = [pos.price_open for pos in sell_positions]
    return min(prices), max(prices)


def can_place_new_buy(current_price, buy_positions, buffer_points=6.0):
    """
    buffer_points: extra distance to avoid very close orders (optional)
    """
    low_buy, high_buy = get_buy_price_range(buy_positions)

    # No existing buys → allow first order
    if low_buy is None:
        return True

    if current_price < (low_buy - buffer_points):
        return True  # Better price (averaging down)

    if current_price > (high_buy + buffer_points):
        return True  # Breakout / continuation

    return False  # ❌ Middle zone

def can_place_new_sell(current_price, sell_positions, buffer_points=6.0):
    high_sell, low_sell = get_sell_price_range(sell_positions)

    # No existing sells → allow first order
    if high_sell is None:
        return True

    if current_price > (high_sell + buffer_points):
        return True  # Worse price (averaging up)

    if current_price < (low_sell - buffer_points):
        return True  # Breakdown / continuation

    return False  # ❌ Middle zone


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

def close_strategy1_orders(symbol, magic_number):

    positions = mt5.positions_get(symbol=symbol)
    if positions is None:
        print("No positions found. Error code:", mt5.last_error())
        return False

    # Filter positions by the specified magic number
    strategy_positions = [pos for pos in positions if pos.magic == magic_number 
                          and pos.volume == 0.13]

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

    latest_buy_position = min(buy_positions, key=lambda pos: pos.time)

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

    latest_sell_position = min(sell_positions, key=lambda pos: pos.time)

    return latest_sell_position.price_open  # Corrected from `.open_price` to `.price_open`


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

def update_sl_tp(position, new_sl, new_tp):
    """Helper function to update stop-loss for a given position."""

    # print(f"update_sl_tp reached for order {position.ticket}")
    # print(f"Current SL: {position.sl}, Current TP: {position.tp}")
    # print(f"New SL: {new_sl}, New TP: {new_tp}")
        
    # Prepare modification request
    modify_request = {
        "action": mt5.TRADE_ACTION_SLTP,
        "symbol": position.symbol,
        "position": position.ticket,
        "sl": new_sl,
        "tp": new_tp,
        "deviation": 20,  # Slippage tolerance
    }

    result = mt5.order_send(modify_request)

    if result is None:
        print(f"Order modification failed: {mt5.last_error()}")
        return False
    elif result.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"Failed to update SL/TP for order {position.ticket}. Error: {result.retcode}")
        return False
    else:
        print(f"Order {position.ticket} SL/TP updated successfully!")
        return True


def hedging_buy_update_sl_13(symbol):
    """Updates stop-loss for hedging buy positions based on predefined thresholds."""
    
    symbol_info = mt5.symbol_info(symbol)
    if not symbol_info:
        print(f"Failed to get symbol info for {symbol}.")
        return
    
    point = symbol_info.point

    price_thresholds_13 = {
        # change_pips_for_sl_550: 30,
        change_pips_for_sl_2000: 50
        }

    positions = mt5.positions_get(symbol=symbol)
    if not positions:
        print(f"No positions found for {symbol}.")
        return

    buy_positions = [pos for pos in positions if pos.type == mt5.ORDER_TYPE_BUY 
                     and pos.magic == special_magic_num and pos.volume == 0.01]

    if not buy_positions:
        return

    # if len(buy_positions) > 2:
    for pos in buy_positions:
        buy_price = pos.price_open
        current_sl = pos.sl
        current_tp = pos.tp
        current_price = symbol_info.bid  

        for threshold, sl_offset in price_thresholds_13.items():

            if current_price >= buy_price + threshold * point:
                new_sl = buy_price + sl_offset * point

                if current_sl == 0.0:
                    update_sl(pos, new_sl)
                else:
                    if current_sl != new_sl and new_sl > current_sl:
                        update_sl(pos, new_sl)
                        pass  # Successfully updated SL

def hedging_sell_update_sl_13(symbol):
    symbol_info = mt5.symbol_info(symbol)
    if not symbol_info:
        print(f"Failed to get symbol info for {symbol}.")
        return

    point = symbol_info.point

    price_thresholds_13 = {
        # change_pips_for_sl_550: 30,
        change_pips_for_sl_2000: 50
        }

    positions = mt5.positions_get(symbol=symbol)
    if not positions:
        print(f"No positions found for {symbol}.")
        return

    sell_positions = [pos for pos in positions if pos.type == mt5.ORDER_TYPE_SELL 
                      and pos.magic == special_magic_num and pos.volume == 0.01]
    
    if not sell_positions:
        return

    # if len(sell_positions) > 2:

    for pos in sell_positions:
        sell_price = pos.price_open
        current_sl = pos.sl
        current_tp = pos.tp
        current_price = symbol_info.ask  # Use ask price for sell positions

        for threshold, sl_offset in price_thresholds_13.items():

            if current_price <= sell_price - threshold * point:  # For SELL: price drops below threshold
                new_sl = sell_price - sl_offset * point  # Move SL lower as price moves down
                
                if current_sl == 0.0:
                    update_sl(pos, new_sl)
                else:
                    if current_sl != new_sl and new_sl < current_sl:
                        update_sl(pos, new_sl)
                        pass  # Successfully updated SL


def hedging_buy_update_sl_for_special(symbol):
    """Updates stop-loss for hedging buy positions based on predefined thresholds."""
    
    symbol_info = mt5.symbol_info(symbol)
    if not symbol_info:
        print(f"Failed to get symbol info for {symbol}.")
        return
    
    point = symbol_info.point

    price_thresholds_09 = {
        change_pips_for_sl_700: 100,
        change_pips_for_sl_1400: 1000,
        change_pips_for_sl_2000: 1700,
        change_pips_for_sl_3000: 2700,
        change_pips_for_sl_4000: 3700,
        change_pips_for_sl_5000: 4700
        }
    
    price_thresholds_10 = {     
        change_pips_for_sl_150: 20,
        change_pips_for_sl_350: 100,
        change_pips_for_sl_550: 200,
        change_pips_for_sl_750: 300,
        change_pips_for_sl_1000: 800,
        change_pips_for_sl_1500: 1400
        }

    price_thresholds_11 = {
        change_pips_for_sl_700: 100,
        change_pips_for_sl_1400: 1000,
        change_pips_for_sl_2000: 1700,
        change_pips_for_sl_3000: 2700,
        change_pips_for_sl_4000: 3700,
        change_pips_for_sl_5000: 4700
        }

    price_thresholds_12 = {     
        change_pips_for_sl_150: 50,
        change_pips_for_sl_350: 200,
        change_pips_for_sl_550: 300,
        change_pips_for_sl_750: 400,
        change_pips_for_sl_950: 500,
        change_pips_for_sl_1400: 1000
        }
    
    positions = mt5.positions_get(symbol=symbol)
    if not positions:
        print(f"No positions found for {symbol}.")
        return

    buy_positions = [pos for pos in positions if pos.type == mt5.ORDER_TYPE_BUY 
                     and pos.magic == sell_magic_num 
                     and pos.volume in (opposite_qty09, opposite_qty10, opposite_qty11, opposite_qty19, 
                                        opposite_qty19, opposite_qty14, opposite_qty15, opposite_qty16,
                                        opposite_qty17, opposite_qty18, opposite_qty19, opposite_qty20,
                                        opposite_qty25, opposite_qty30, opposite_qty45)]

    if not buy_positions:
        return

    for pos in buy_positions:
        buy_price = pos.price_open
        current_sl = pos.sl
        current_tp = pos.tp
        current_price = symbol_info.bid  

        if pos.volume == 0.09:
            for threshold, sl_offset in price_thresholds_09.items():

                if current_price >= buy_price + threshold * point:
                    new_sl = buy_price + sl_offset * point

                    if current_sl == 0.0:
                        update_sl(pos, new_sl)
                    else:
                        if current_sl != new_sl and new_sl > current_sl:
                            update_sl(pos, new_sl)
                            pass  # Successfully updated SL
        elif pos.volume == 0.10:
            for threshold, sl_offset in price_thresholds_10.items():

                if current_price >= buy_price + threshold * point:
                    new_sl = buy_price + sl_offset * point

                    if current_sl == 0.0:
                        update_sl(pos, new_sl)
                    else:
                        if current_sl != new_sl and new_sl > current_sl:
                            update_sl(pos, new_sl)
                            pass  # Successfully updated SL
        elif pos.volume == 0.11:
            for threshold, sl_offset in price_thresholds_11.items():

                if current_price >= buy_price + threshold * point:
                    new_sl = buy_price + sl_offset * point

                    if current_sl == 0.0:
                        update_sl(pos, new_sl)
                    else:
                        if current_sl != new_sl and new_sl > current_sl:
                            update_sl(pos, new_sl)
                            pass  # Successfully updated SL
        else:
            for threshold, sl_offset in price_thresholds_12.items():
                if current_price >= buy_price + threshold * point:
                    new_sl = buy_price + sl_offset * point

                    if current_sl == 0.0:
                        update_sl(pos, new_sl)
                    else:
                        if current_sl != new_sl and new_sl > current_sl:
                            update_sl(pos, new_sl)
                            pass  # Successfully updated SL


def hedging_sell_update_sl_for_special(symbol):

    symbol_info = mt5.symbol_info(symbol)
    if not symbol_info:
        print(f"Failed to get symbol info for {symbol}.")
        return

    point = symbol_info.point

    price_thresholds_09 = {     
        change_pips_for_sl_700: 100,
        change_pips_for_sl_1400: 1000,
        change_pips_for_sl_2000: 1700,
        change_pips_for_sl_3000: 2700,
        change_pips_for_sl_4000: 3700,
        change_pips_for_sl_5000: 4700
        }

    price_thresholds_10 = {     
        change_pips_for_sl_150: 20,
        change_pips_for_sl_350: 100,
        change_pips_for_sl_550: 200,
        change_pips_for_sl_750: 300,
        change_pips_for_sl_1000: 800,
        change_pips_for_sl_1500: 1400
        }

    price_thresholds_11 = {     
        change_pips_for_sl_700: 100,
        change_pips_for_sl_1400: 1000,
        change_pips_for_sl_2000: 1700,
        change_pips_for_sl_3000: 2700,
        change_pips_for_sl_4000: 3700,
        change_pips_for_sl_5000: 4700
        }

    price_thresholds_12 = {     
        change_pips_for_sl_150: 50,
        change_pips_for_sl_350: 200,
        change_pips_for_sl_550: 300,
        change_pips_for_sl_750: 400,
        change_pips_for_sl_950: 500,
        change_pips_for_sl_1400: 1000
        }


    positions = mt5.positions_get(symbol=symbol)
    if not positions:
        print(f"No positions found for {symbol}.")
        return

    sell_positions = [pos for pos in positions if pos.type == mt5.ORDER_TYPE_SELL 
                      and pos.magic == buy_magic_num 
                      and pos.volume in (opposite_qty09, opposite_qty10, opposite_qty11, opposite_qty19, 
                                        opposite_qty19, opposite_qty14, opposite_qty15, opposite_qty16,
                                        opposite_qty17, opposite_qty18, opposite_qty19, opposite_qty20,
                                        opposite_qty25, opposite_qty30, opposite_qty45)]
    
    if not sell_positions:
        return

    for pos in sell_positions:
        sell_price = pos.price_open
        current_sl = pos.sl
        current_tp = pos.tp
        current_price = symbol_info.ask  # Use ask price for sell positions

        if pos.volume == 0.09:
            for threshold, sl_offset in price_thresholds_09.items():

                if current_price <= sell_price - threshold * point:  # For SELL: price drops below threshold
                    new_sl = sell_price - sl_offset * point  # Move SL lower as price moves down
                    
                    if current_sl == 0.0:
                        update_sl(pos, new_sl)
                    else:
                        if current_sl != new_sl and new_sl < current_sl:
                            update_sl(pos, new_sl)
                            pass  # Successfully updated SL
        elif pos.volume == 0.10:
            for threshold, sl_offset in price_thresholds_10.items():

                if current_price <= sell_price - threshold * point:  # For SELL: price drops below threshold
                    new_sl = sell_price - sl_offset * point  # Move SL lower as price moves down
                    
                    if current_sl == 0.0:
                        update_sl(pos, new_sl)
                    else:
                        if current_sl != new_sl and new_sl < current_sl:
                            update_sl(pos, new_sl)
                            pass  # Successfully updated SL
        elif pos.volume == 0.11:
            for threshold, sl_offset in price_thresholds_11.items():
                if current_price <= sell_price - threshold * point:  # For SELL: price drops below threshold
                    new_sl = sell_price - sl_offset * point  # Move SL lower as price moves down
                    
                    if current_sl == 0.0:
                        update_sl(pos, new_sl)
                    else:
                        if current_sl != new_sl and new_sl < current_sl:
                            update_sl(pos, new_sl)
                            pass  # Successfully updated SL
        else:
            for threshold, sl_offset in price_thresholds_12.items():
                if current_price <= sell_price - threshold * point:  # For SELL: price drops below threshold
                    new_sl = sell_price - sl_offset * point  # Move SL lower as price moves down
                    
                    if current_sl == 0.0:
                        update_sl(pos, new_sl)
                    else:
                        if current_sl != new_sl and new_sl < current_sl:
                            update_sl(pos, new_sl)
                            pass  # Successfully updated SL


def close_profitable_small_orders(symbol):
    # Get all open positions for the given symbol
    positions = mt5.positions_get(symbol=symbol)
    if positions is None or len(positions) == 0:    
        print("No open positions found.")
        return

    buys = [pos for pos in positions if pos.magic == special_magic_num and pos.type == mt5.ORDER_TYPE_BUY]
    sells = [pos for pos in positions if pos.magic == special_magic_num and pos.type == mt5.ORDER_TYPE_SELL]

    if len(buys) > 5:
        handle_order_closing(symbol, buys)
    if len(sells) > 5:
        handle_order_closing(symbol, sells)


    # Process Buy Orders (0.01) & their Hedge Orders (opposite qty Sell)
    # if len(buy_orders) > 0:
    #     if len(buy_orders) in (5, 10, 15, 20, 25, 30, 35, 45, 50, 55):
    #         handle_order_closing(symbol, buy_orders)
    # if len(sell_orders) > 0:
    #     if len(sell_orders) in (5, 10, 15, 20, 25, 30, 35, 45, 50, 55):
    #         handle_order_closing(symbol, sell_orders)

    # after creating 4 to close all 1s
    # if len(buy_orders) > 0:
    #     if len(buy_orders) not in (5, 10, 15, 20, 25, 30, 35, 45, 50, 55):
    #         handle_order_closing1(symbol, buy_small_orders)
    # if len(sell_orders) > 0:
    #     if len(sell_orders) not in (5, 10, 15, 20, 25, 30, 35, 45, 50, 55):
    #         handle_order_closing1(symbol, sell_small_orders)

    # to close all 2s
    # if len(hedge_orders_buys) > 0:
    #     handle_order_closing2(symbol, hedge_orders_buys)
    # if len(hedge_orders_sell) > 0:
    #     handle_order_closing2(symbol, hedge_orders_sell)

    # if len(buy_orders) == 13:
    #     handle_order_closing3(symbol, buy_orders)
    # if len(sell_orders) == 13:
    #     handle_order_closing3(symbol, sell_orders)

    # if len(buy_orders) == 18:
    #     handle_order_closing4(symbol, buy_orders)
    # if len(sell_orders) == 18:
    #     handle_order_closing4(symbol, sell_orders)


def handle_order_closing(symbol, small_orders):
    """Closes the order with the highest positive profit if it exceeds 10."""

    # Filter only profitable orders
    profitable_orders = [o for o in small_orders if o.profit > 0]

    if not profitable_orders:
        return  # No profitable orders to consider

    # Get the order with the highest profit
    best_order = max(profitable_orders, key=lambda x: x.profit)

    # Close it if profit is greater than 10
    if best_order.profit > 30:
        close_order(best_order, symbol)


def handle_order_closing1(symbol, small_orders):
    """ Handles closing of 0.01 orders based on the hedge position. """

    latest_bors_order = max(small_orders, key=lambda x: x.time)  # Get latest hedge order by time

    if latest_bors_order.profit > 4:  # If the latest hedge order is in loss
        close_order(latest_bors_order, symbol)

def handle_order_closing2(symbol, small_orders):
    """ Handles closing of 0.01 orders based on the hedge position. """

    positions = mt5.positions_get(symbol=symbol)
    if positions is None or len(positions) == 0:    
        print("No open positions found.")
        return

    buy_total = sum(order.volume for order in positions if order.type == mt5.ORDER_TYPE_BUY)
    sell_total = sum(order.volume for order in positions if order.type == mt5.ORDER_TYPE_SELL)

    for order in small_orders:
        if order.profit >= 50 and order.magic == 1001:
            if round(sell_total - buy_total, 2) > 5:
                close_order(order, symbol)

    for order in small_orders:
        if order.profit >= 50 and order.magic == 2001:
            if round(buy_total - sell_total, 2) > 5:
                close_order(order, symbol)


def handle_order_closing3(symbol, small_orders):
    """ Handles closing of 0.01 orders based on the hedge position. """

    # small_orders = sorted(small_orders, key=lambda x: x.time, reverse=True)
    # last_3_small_orders = sorted(small_orders, key=lambda x: x.time, reverse=True)[:3]
    latest_bors_order = max(small_orders, key=lambda x: x.time)  # Get latest hedge order by time

    if latest_bors_order.profit > 30:  # If the latest hedge order is in loss
        close_order(latest_bors_order, symbol)


def handle_order_closing4(symbol, small_orders):
    """ Handles closing of 0.01 orders based on the hedge position. """

    # small_orders = sorted(small_orders, key=lambda x: x.time, reverse=True)
    # last_3_small_orders = sorted(small_orders, key=lambda x: x.time, reverse=True)[:3]
    latest_bors_order = max(small_orders, key=lambda x: x.time)  # Get latest hedge order by time

    if latest_bors_order.profit > 40:  # If the latest hedge order is in loss
        close_order(latest_bors_order, symbol)

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

def monitor_and_place_opposite_orders(symbol):
    global initial_equity

    # Get all open positions for the given symbol
    positions = mt5.positions_get(symbol=symbol)
    if positions is None or len(positions) == 0:
        print("No open positions found.")
        return

    current_equity = get_current_equity()

    # print (f"current_equity is: {current_equity} and initial_equity: {initial_equity} and expected: {initial_equity + 100}")
    if current_equity >= initial_equity + 100:
        close_all_orders()


def close_all_orders():
    global initial_equity

    orders = mt5.positions_get()
    if orders is None or len(orders) == 0:
        print("No open orders to close.")
        return

    for order in orders:
        close_request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": order.symbol,
            "volume": order.volume,
            "type": mt5.ORDER_TYPE_SELL if order.type == mt5.ORDER_TYPE_BUY else mt5.ORDER_TYPE_BUY,
            "position": order.ticket,
            "price": mt5.symbol_info_tick(order.symbol).bid if order.type == mt5.ORDER_TYPE_BUY else mt5.symbol_info_tick(order.symbol).ask,
            "deviation": 20,
            "magic": order.magic,
            "comment": "Equity Target Hit",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        result = mt5.order_send(close_request)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print(f"Failed to close order {order.ticket}, Error: {result.comment}")
        else:
            print(f"Closed order {order.ticket} successfully.")
            initial_equity = get_current_equity()
            print(f"Closing function - initial equity is: {initial_equity}")
            
def process_hedging_orders(symbol):

    hedging_buy_update_sl_13(symbol)
    hedging_sell_update_sl_13(symbol)

    # hedging_buy_update_sl_for_special(symbol)
    # hedging_sell_update_sl_for_special(symbol)

def place_general_orders_buy_sell(symbol):
    # global buy_magic_num, sell_magic_num
    # time.sleep(10)
    # Get the current price for the symbol
    buy_price = mt5.symbol_info_tick(symbol).ask
    sell_price = mt5.symbol_info_tick(symbol).bid

    # Retrieve all open positions for the symbol
    positions = mt5.positions_get(symbol=symbol)

    if positions:
        # Find the latest position by sorting or using max
        latest_position = max(positions, key=lambda x: x.time)
        latest_position_price = latest_position.price_open
        # print(f"Latest Position Price: {latest_position_price}")
    else:
        print("No open positions found.")

    # monitor_and_place_opposite_orders(symbol)

    process_hedging_orders(symbol)

    close_orders_based_on_conditions(symbol, buy_magic_num, sell_magic_num)

    # buy_magic_num, sell_magic_num = calculate_magic_numbers(positions, lot_sizes)
    # print(f"buy and sell magic numbers are: {buy_magic_num} {sell_magic_num}")
    # Filter to include only open buy positions (type 0), exclude volumes 4 and 6, and sort by open time to get the latest
    buy_positions = sorted(
        [pos for pos in positions if pos.type == mt5.ORDER_TYPE_BUY and pos.magic == buy_magic_num],
        key=lambda x: x.time,
        reverse=True
    )

    # Filter to include only open buy positions (type 0), exclude volumes 4 and 6, and sort by open time to get the latest
    sell_positions = sorted(
        [pos for pos in positions if pos.type == mt5.ORDER_TYPE_SELL and pos.magic == sell_magic_num],
        key=lambda x: x.time,
        reverse=True
    )

    if buy_positions:
        close_profitable_small_orders(symbol)
    if sell_positions:
        close_profitable_small_orders(symbol)

    buy_positions_with_initial_order = [
    pos for pos in positions if pos.type == mt5.ORDER_TYPE_BUY and pos.magic == buy_magic_num]

    sell_positions_with_initial_order = [
    pos for pos in positions if pos.type == mt5.ORDER_TYPE_SELL and pos.magic == sell_magic_num]

    buy_order_index = len(buy_positions)
    sell_order_index = len(sell_positions)

    if not buy_positions:
        buy_order_qty = lot_sizes[0]
        place_buy_order(symbol, buy_order_qty, buy_magic_num)
    else:
        latest_buy_position_price = buy_positions[0].price_open
        buy_order_qty = lot_sizes[buy_order_index] if buy_order_index < len(lot_sizes) else lot_sizes[-1]

        if buy_price <= latest_buy_position_price - diff_pips * mt5.symbol_info(symbol).point:
            if buy_order_index < len(lot_sizes):
                place_buy_order(symbol, buy_order_qty, buy_magic_num)

    if not sell_positions:
        sell_order_qty = lot_sizes[0]
        place_sell_order(symbol, sell_order_qty, sell_magic_num)
    else:
        latest_sell_position_price = sell_positions[0].price_open
        sell_order_qty = lot_sizes[sell_order_index] if sell_order_index < len(lot_sizes) else lot_sizes[-1]

        if sell_price >= latest_sell_position_price + diff_pips * mt5.symbol_info(symbol).point:
            if sell_order_index < len(lot_sizes): 
                place_sell_order(symbol, sell_order_qty, sell_magic_num)


def get_equity(symbol):
        account_info = mt5.account_info()
        if account_info is None:
            return None
        return account_info.equity


# Function to manage the Martingale strategy
def martingale_strategy(symbol):
    global target_balance, my_equity


    start_balance = get_equity(symbol)
    my_equity = start_balance
    target_balance = start_balance + profit_target
    print(f"start and target balances are {start_balance}, {target_balance}")


    while True:

        place_general_orders_buy_sell(symbol)
        
        # Sleep to avoid excessive API calls
        time.sleep(5)


# Example usage
symbol = "XAUUSD"  # Change this to your desired trading symbol

# Start the Martingale strategy
martingale_strategy(symbol)

# Shutdown the connection (unreachable in infinite loop above)
mt5.shutdown()
