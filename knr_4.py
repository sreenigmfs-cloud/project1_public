
import MetaTrader5 as mt5
import time
import pandas as pd
import numpy as np
from datetime import datetime

"""
narayana_gold_v3 & v4 same. only change is SL update when 4 points up or down
"""

# Initialize connection to MetaTrader 5
if not mt5.initialize():
    print("Initialize failed, error code =", mt5.last_error())
    mt5.shutdown()
    exit()

lot_sizes = [0.01, 0.01, 0.01, 0.02, 0.03] 
opposite_size = 0.10

            #  0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01,
            #  0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01]

buy_order_qty = 0
sell_order_qty = 0
latest_position_price = 0
profit_amount = 500
profit_amount_small = 250
profit_target = 100

NUM_CANDLES = 100
BARS = 100

buy_ctr = 0
sell_ctr = 0

buy_ctr_11 = 0
sell_ctr_11 = 0

buy_ctr_09 = 0
sell_ctr_09 = 0

buy_ctr_08 = 0
sell_ctr_08 = 0

buy_ctr_07 = 0
sell_ctr_07 = 0

buy_ctr_06 = 0
sell_ctr_06 = 0

buy_ctr_04 = 0
sell_ctr_04 = 0

pips_200 = 200
pips_250 = 250
pips_300 = 300
pips_500 = 500
pips_1000 = 1000
pips_100 = 100

change_pips_for_sl_500 = 500
change_pips_for_sl_700 = 700
change_pips_for_sl_1000 = 1000

buy_magic_num = 1001
sell_magic_num = 2001
magic_num_24 = 24

small_qty = 0.01

opposite_qty04 = 0.04
opposite_qty06 = 0.06 
opposite_qty07 = 0.07
opposite_qty08 = 0.08
opposite_qty09 = 0.09
opposite_qty10 = 0.10
opposite_qty11 = 0.11
opposite_qty15 = 0.15

buy_order_index = 0
sell_order_index = 0

buy_series = [100, 101, 102, 103, 104, 105]
sell_series = [200, 201, 202, 203, 204, 205]

# Function to place a buy order
def place_buy_order(symbol, buy_order_qty, magic_num):

    print(f"buy magic number is : {magic_num}")
   
    price = mt5.symbol_info_tick(symbol).ask
    if price == 0:
        print(f"Error retrieving price for {symbol}.")
        return

    tp = price + pips_500 * mt5.symbol_info(symbol).point
  
    # Prepare the order request for buy
    if buy_order_qty in lot_sizes:

        order = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": buy_order_qty,
            "type": 0,  # Buy order type
            "price": price,
            # "tp": tp,
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

        if buy_order_qty in lot_sizes:
            print(f"update buy is enabled and bq is: {buy_order_qty}")    
            update_common_tp_for_buy(symbol, magic_num)
       

# Function to place a sell order
def place_sell_order(symbol, sell_order_qty, magic_num):

    print(f"sell magic number is : {magic_num}")
  
    price = mt5.symbol_info_tick(symbol).bid
    if price is None:
        print("Error retrieving bid price.")
        return

    tp = price - pips_500 * mt5.symbol_info(symbol).point
   
    if sell_order_qty in lot_sizes:

        # Prepare the sell order request
        sell_order = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": sell_order_qty,
            "type": 1,  # Sell order type
            "price": price,
            # "sl": sell_sl,
            # "tp": tp,
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

        if sell_order_qty in lot_sizes:
            print(f"update sell is enabled sq is: {sell_order_qty}")    
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
    buy_tp_price_common = avg_buy_price + pips_500 * mt5.symbol_info(symbol).point
    # buy_tp_price_single = get_latest_buy_tp(symbol, magic_num)

    # if len(buy_positions) <= 3:
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
    sell_tp_price_common = avg_sell_price - pips_500 * mt5.symbol_info(symbol).point
    # sell_tp_price_single = get_latest_sell_tp(symbol, magic_num)

    # if len(sell_positions) <= 3:
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

def close_orders_based_on_conditions(symbol, buy_magic_num, sell_magic_num):
    global target_balance

    # Get all positions for the symbol
    positions = mt5.positions_get(symbol=symbol)
    if not positions:
        print(f"No positions found for {symbol}.")
        return


# scenario 1 -- begins
    current_equity = get_equity(symbol)
    
    if current_equity >= target_balance:

        print(f"before clearing current equity and target balances are {current_equity}, {target_balance}")
        target_balance = current_equity + profit_target
        close_strategy_orders1(symbol)
        print(f"After clearing current equity and target balances are {current_equity}, {target_balance}")
# scenario 1 -- end


    buy_hedge_q06 = [pos for pos in positions if pos.magic == 1001 and pos.volume == opposite_qty06]
    sell_hedge_q06 = [pos for pos in positions if pos.magic == 2001 and pos.volume == opposite_qty06]
    buy_hedge_q07 = [pos for pos in positions if pos.magic == 1001 and pos.volume == opposite_qty07]
    sell_hedge_q07 = [pos for pos in positions if pos.magic == 2001 and pos.volume == opposite_qty07]
    buy_hedge_q08 = [pos for pos in positions if pos.magic == 1001 and pos.volume == opposite_qty08]
    sell_hedge_q08 = [pos for pos in positions if pos.magic == 2001 and pos.volume == opposite_qty08]
    buy_hedge_q09 = [pos for pos in positions if pos.magic == 1001 and pos.volume == opposite_qty09]
    sell_hedge_q09 = [pos for pos in positions if pos.magic == 2001 and pos.volume == opposite_qty09]
    buy_hedge_q15 = [pos for pos in positions if pos.magic == 1001 and pos.volume == opposite_qty15]
    sell_hedge_q15 = [pos for pos in positions if pos.magic == 2001 and pos.volume == opposite_qty15]
    buy_hedge_q11 = [pos for pos in positions if pos.magic == 1001 and pos.volume == opposite_qty11]
    sell_hedge_q11 = [pos for pos in positions if pos.magic == 2001 and pos.volume == opposite_qty11]
    
    # below logic is diff strategy ......... START
    buy_pos = [bpos for bpos in positions if bpos.type == mt5.ORDER_TYPE_BUY and bpos.magic == buy_magic_num]
    sell_pos = [spos for spos in positions if spos.type == mt5.ORDER_TYPE_SELL and spos.magic == sell_magic_num]


    total_profit = sum(pos.profit for pos in positions)
    total_positions = len(positions)


    if total_positions >= 4 and total_profit <= -50:
        close_strategy_orders1(symbol)



    if not buy_pos:
        close_strategy_orders(symbol, buy_magic_num)
    if not sell_pos:
        close_strategy_orders(symbol, sell_magic_num)


    # # Define thresholds for orders and net profit
    # condition_for_11 = [(10, -300)]
    # condition_for_09 = [(10, -250)]
    # condition_for_08 = [(10, -200)]
    # condition_for_07 = [(10, -150)]
    # condition_for_06 = [(10, -100)]

    # conditions = [
    #     (10, 0),       # Order 8: Close if profit >= 0
    # ]

    # total_profit = sum(pos.profit for pos in positions)
    # total_positions = len(positions)

    # for count_max, profit_max in conditions:
    #      if total_positions >= count_max and total_profit >= profit_max:
    #             close_strategy_orders1(symbol)
    #             break
    
    # if buy_hedge_q15 and not buy_hedge_q11:
    #     for count_max, profit_max in condition_for_11:
    #         if total_positions >= count_max and total_profit >= profit_max:
    #                 close_strategy_orders1(symbol)
    #                 break

    # if buy_hedge_q15 and not buy_hedge_q09:
    #     for count_max, profit_max in condition_for_09:
    #         if total_positions >= count_max and total_profit >= profit_max:
    #                 close_strategy_orders1(symbol)
    #                 break

    # if buy_hedge_q15 and not buy_hedge_q08:
    #     for count_max, profit_max in condition_for_08:
    #         if total_positions >= count_max and total_profit >= profit_max:
    #                 close_strategy_orders1(symbol)
    #                 break

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

# Function to get the latest buy order TP price
def get_latest_buy_tp(symbol, magic_num):
    positions = mt5.positions_get(symbol=symbol)
    if not positions:
        print("No open buy positions found.")
        return None

    # Filter for buy positions
    buy_positions = [pos for pos in positions if pos.type == mt5.ORDER_TYPE_BUY and pos.volume == 0.02]
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
    sell_positions = [pos for pos in positions if pos.type == mt5.ORDER_TYPE_SELL and pos.volume == 0.02]
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


def hedging_buy_update_sl_all(symbol):
    """Updates stop-loss for hedging buy positions based on predefined thresholds."""
    
    symbol_info = mt5.symbol_info(symbol)
    if not symbol_info:
        print(f"Failed to get symbol info for {symbol}.")
        return
    
    point = symbol_info.point

   
    price_thresholds_all = {
        change_pips_for_sl_500: 100
        }

    positions = mt5.positions_get(symbol=symbol)
    if not positions:
        print(f"No positions found for {symbol}.")
        return

    buy_positions = [pos for pos in positions if pos.type == mt5.ORDER_TYPE_BUY 
                     and pos.magic == sell_magic_num and pos.volume in (opposite_qty06, opposite_qty07,
                                                                        opposite_qty09, opposite_qty08,
                                                                        opposite_qty11)]

    if not buy_positions:
        return

    # if len(buy_positions) > 2:
    for pos in buy_positions:
        buy_price = pos.price_open
        current_sl = pos.sl
        current_tp = pos.tp
        current_price = symbol_info.bid  

        for threshold, sl_offset in price_thresholds_all.items():

                if current_price >= buy_price + threshold * point:
                    new_sl = buy_price + sl_offset * point

                    if current_sl == 0.0:
                        update_sl(pos, new_sl)
                    else:
                        if current_sl != new_sl and new_sl > current_sl:
                            update_sl(pos, new_sl)
                            pass  # Successfully updated SL


def hedging_sell_update_sl_all(symbol):
    symbol_info = mt5.symbol_info(symbol)
    if not symbol_info:
        print(f"Failed to get symbol info for {symbol}.")
        return

    point = symbol_info.point

    price_thresholds_all = {
        change_pips_for_sl_500: 100
        }

    positions = mt5.positions_get(symbol=symbol)
    if not positions:
        print(f"No positions found for {symbol}.")
        return

    sell_positions = [pos for pos in positions if pos.type == mt5.ORDER_TYPE_SELL     
                     and pos.magic == buy_magic_num and pos.volume in (opposite_qty06, opposite_qty07,
                                                                    opposite_qty09, opposite_qty08,
                                                                    opposite_qty11)]
    
    if not sell_positions:
        return

    # if len(sell_positions) > 2:

    for pos in sell_positions:
        sell_price = pos.price_open
        current_sl = pos.sl
        current_tp = pos.tp
        current_price = symbol_info.ask  # Use ask price for sell positions

        for threshold, sl_offset in price_thresholds_all.items():

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

    # buy_orders_small = [pos for pos in positions if pos.magic == 1001 and pos.volume == small_qty]
    # sell_orders_small = [pos for pos in positions if pos.magic == 2001 and pos.volume == small_qty]

    # Separate orders by strategy and lot size
    buy_orders_small = [pos for pos in positions if pos.magic == 1001 and pos.volume in [0.01, 0.02, 0.03]]
    sell_orders_small = [pos for pos in positions if pos.magic == 2001 and pos.volume in [0.05, 0.02, 0.03]]

    buy_orders_hedge = [pos for pos in positions if pos.magic == 2001 and pos.volume in [0.11, 0.09, 0.08, 0.07, 0.06]]
    sell_orders_hedge = [pos for pos in positions if pos.magic == 1001 and pos.volume in [0.11, 0.09, 0.08, 0.07, 0.06]]
   
    # Process Buy Orders (0.01) & their Hedge Orders (opposite qty Sell)
    # if buy_orders_small:
    #     handle_order_closing(symbol, buy_orders_small)
    # if sell_orders_small:
    #     handle_order_closing(symbol, sell_orders_small)

    if sell_orders_hedge:
        handle_order_closing_big(symbol, buy_orders_small)
    else:
        handle_order_closing_all(symbol, buy_orders_small)

    if buy_orders_hedge:
        handle_order_closing_big(symbol, sell_orders_small)
    else:
        handle_order_closing_all(symbol, sell_orders_small)

def handle_order_closing_big(symbol, small_orders):
    """ Handles closing of 0.01 orders based on the hedge position. """
    positions = mt5.positions_get(symbol=symbol)
    big_orders = sorted(small_orders, key=lambda x: x.time, reverse=True)

    # if len(small_orders) >= 1:   
    for pos in positions:
        if pos.volume == 0.03 and pos.profit >= pos.volume * profit_amount:
            close_order(pos, symbol)
    
def handle_order_closing_all(symbol, small_orders):
    """ Handles closing of 0.01 orders based on the hedge position. """
    positions = mt5.positions_get(symbol=symbol)
    small_orders = sorted(small_orders, key=lambda x: x.time, reverse=True)

    # if len(small_orders) >= 1:   
    for pos in positions:
        if pos.profit >= pos.volume * profit_amount_small:
            close_order(pos, symbol)
 
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


def hedging_buy_update_sl_04(symbol):
    """Updates stop-loss for hedging buy positions based on predefined thresholds."""
    
    symbol_info = mt5.symbol_info(symbol)
    if not symbol_info:
        print(f"Failed to get symbol info for {symbol}.")
        return
    
    point = symbol_info.point

    price_thresholds_04 = {
        change_pips_for_sl_700: 100        
        }
    
    positions = mt5.positions_get(symbol=symbol)
    if not positions:
        print(f"No positions found for {symbol}.")
        return

    buy_positions_04 = [pos for pos in positions if pos.type == mt5.ORDER_TYPE_BUY 
                     and pos.magic == 3001 and pos.volume == opposite_qty04]

    if not buy_positions_04:
        return

    # if any(order.profit <= -6 for order in buy_positions_04):
    for pos in buy_positions_04:
        buy_price = pos.price_open
        current_sl = pos.sl
        current_tp = pos.tp
        current_price = symbol_info.bid  

        for threshold, sl_offset in price_thresholds_04.items():

            # if current_sl == 0.0:
            #     new_sl = buy_price - pips_100 * point
            #     update_sl(pos, new_sl)

            if current_price >= buy_price + threshold * point:
                new_sl = buy_price + sl_offset * point

                if current_sl == 0.0:
                    update_sl(pos, new_sl)
                else:
                    if current_sl != new_sl and new_sl > current_sl:
                        update_sl(pos, new_sl)
                        pass  # Successfully updated SL


def hedging_sell_update_sl_04(symbol):
    symbol_info = mt5.symbol_info(symbol)
    if not symbol_info:
        print(f"Failed to get symbol info for {symbol}.")
        return

    point = symbol_info.point
   
    price_thresholds_04 = {
        change_pips_for_sl_700: 100        
        }

    positions = mt5.positions_get(symbol=symbol)
    if not positions:
        print(f"No positions found for {symbol}.")
        return

    sell_positions_04 = [pos for pos in positions if pos.type == mt5.ORDER_TYPE_SELL 
                     and pos.magic == 4001 and pos.volume == opposite_qty04]
    
    if not sell_positions_04:
        return

    # if any(order.profit < -10 for order in sell_positions_04):
    for pos in sell_positions_04:
        sell_price = pos.price_open
        current_sl = pos.sl
        current_tp = pos.tp
        current_price = symbol_info.ask  # Use ask price for sell positions

        for threshold, sl_offset in price_thresholds_04.items():
            # if current_sl == 0.0:
            #     new_sl = sell_price + pips_100 * point
            #     update_sl(pos, new_sl)

            if current_price <= sell_price - threshold * point:  # For SELL: price drops below threshold
                new_sl = sell_price - sl_offset * point  # Move SL lower as price moves down
                
                if current_sl == 0.0:
                    update_sl(pos, new_sl)
                else:
                    if current_sl != new_sl and new_sl < current_sl:
                        update_sl(pos, new_sl)
                        pass  # Successfully updated SL
    

def monitor_and_place_opposite_orders(symbol):
    global buy_ctr, sell_ctr, buy_ctr_04, sell_ctr_04, buy_ctr_06, sell_ctr_06, buy_ctr_07, sell_ctr_07
    global buy_ctr_08, sell_ctr_08, buy_ctr_09, sell_ctr_09, buy_ctr_11, sell_ctr_11 

    # Get all open positions for the given symbol
    positions = mt5.positions_get(symbol=symbol)
    if positions is None or len(positions) == 0:
        print("No open positions found.")
        return

    # Separate orders by strategy and lot size
    buy_only = [pos for pos in positions if pos.magic == 1001 and pos.type == mt5.ORDER_TYPE_BUY]
    sell_only = [pos for pos in positions if pos.magic == 2001 and pos.type == mt5.ORDER_TYPE_SELL]

    # buy_orders = [pos for pos in positions if pos.magic == 1001 and pos.volume == small_qty]
    # sell_orders = [pos for pos in positions if pos.magic == 2001 and pos.volume == small_qty]
    # buy_hedge_q06 = [pos for pos in positions if pos.magic == 1001 and pos.volume == opposite_qty06]
    # sell_hedge_q06 = [pos for pos in positions if pos.magic == 2001 and pos.volume == opposite_qty06]
    # buy_hedge_q07 = [pos for pos in positions if pos.magic == 1001 and pos.volume == opposite_qty07]
    # sell_hedge_q07 = [pos for pos in positions if pos.magic == 2001 and pos.volume == opposite_qty07]
    # buy_hedge_q08 = [pos for pos in positions if pos.magic == 1001 and pos.volume == opposite_qty08]
    # sell_hedge_q08 = [pos for pos in positions if pos.magic == 2001 and pos.volume == opposite_qty08]
    # buy_hedge_q09 = [pos for pos in positions if pos.magic == 1001 and pos.volume == opposite_qty09]
    # sell_hedge_q09 = [pos for pos in positions if pos.magic == 2001 and pos.volume == opposite_qty09]
    # buy_hedge_q15 = [pos for pos in positions if pos.magic == 1001 and pos.volume == opposite_qty15]
    # sell_hedge_q15 = [pos for pos in positions if pos.magic == 2001 and pos.volume == opposite_qty15]
    buy_hedge_q10 = [pos for pos in positions if pos.magic == 1001 and pos.volume == opposite_qty10]
    sell_hedge_q10 = [pos for pos in positions if pos.magic == 2001 and pos.volume == opposite_qty10]
    
    # buy_ord_hedge_04 = [pos for pos in positions if pos.magic == 3001 and pos.volume == opposite_qty04]
    # sell_ord_hedge_04 = [pos for pos in positions if pos.magic == 4001 and pos.volume == opposite_qty04]
   

    # print(f"buy and sell orders counts for 0.01's are: {len(buy_orders)}, {len(sell_orders)}")
   

    if len(buy_only) == 5 and all(order.profit < -4 for order in buy_only):
        if len(buy_hedge_q10) < 1:        
            place_sell_order(symbol, opposite_size, magic_num=1001)

    if len(sell_only) == 5 and all(order.profit < -4 for order in sell_only):
        if len(sell_hedge_q10) < 1: 
            place_buy_order(symbol, opposite_size, magic_num=2001)


#     if len(buy_orders) == 7 and all(order.profit < -1 for order in buy_orders):
#             if len(buy_hedge_q09) < 1 and sell_ctr_09 == 0:
#                 place_sell_order(symbol, opposite_qty09, magic_num=1001)
#                 sell_ctr_09 += 1
#                 print(f" sell counter is: {sell_ctr_09} ")


#     if len(buy_orders) == 10 and all(order.profit < -1 for order in buy_orders):
#             if len(buy_hedge_q08) < 1 and sell_ctr_08 == 0:
#                 place_sell_order(symbol, opposite_qty08, magic_num=1001)
#                 sell_ctr_08 += 1
#                 print(f" sell counter is: {sell_ctr_08} ")


#     if len(buy_orders) == 13 and all(order.profit < -1 for order in buy_orders):
#             if len(buy_hedge_q07) < 1 and sell_ctr_07 == 0:
#                 place_sell_order(symbol, opposite_qty07, magic_num=1001)
#                 sell_ctr_07 += 1
#                 print(f" sell counter is: {sell_ctr_07} ")


#     if len(buy_orders) == 16 and all(order.profit < -1 for order in buy_orders):
#             if len(buy_hedge_q06) < 1 and sell_ctr_06 == 0:
#                 place_sell_order(symbol, opposite_qty06, magic_num=1001)
#                 sell_ctr_06 += 1
#                 print(f" sell counter is: {sell_ctr_06} ")


#     if len(buy_orders) == 20 and all(order.profit < -1 for order in buy_orders):
#             if len(buy_hedge_q15) < 1:
#                 place_sell_order(symbol, opposite_qty15, magic_num=1001)
    

# #***************************************************RESET SELL COUNTERS***************************
#     if len(buy_hedge_q15) > 0 or len(buy_hedge_q06) > 0 or len(buy_hedge_q07) > 0 or len(buy_hedge_q08) > 0 or len(buy_hedge_q09) > 0: 
#         if len(buy_orders) < 1:
#             sell_ctr_11 = 0
#     elif len(buy_orders) <= 1:
#             sell_ctr_11 = 0 

#     if len(buy_hedge_q15) > 0 or len(buy_hedge_q06) > 0 or len(buy_hedge_q07) > 0 or len(buy_hedge_q08) > 0: 
#         if len(buy_orders) <= 3:
#             sell_ctr_09 = 0
#     elif len(buy_orders) <= 4:
#             sell_ctr_09 = 0 

#     if len(buy_hedge_q15) > 0 or len(buy_hedge_q06) > 0 or len(buy_hedge_q07) > 0: 
#         if len(buy_orders) <= 6:
#             sell_ctr_08 = 0
#     elif len(buy_orders) <= 7:
#             sell_ctr_08 = 0 
    
#     if len(buy_hedge_q15) > 0 or len(buy_hedge_q06) > 0: 
#         if len(buy_orders) <= 9:
#             sell_ctr_07 = 0
#     elif len(buy_orders) <= 10:
#             sell_ctr_07 = 0 
    

#     if len(buy_hedge_q15) > 0: 
#         if len(buy_orders) <= 12:
#             sell_ctr_06 = 0
#     elif len(buy_orders) <= 13:
#             sell_ctr_06 = 0 
    
# #***************************************************

    
# #####        
#     if len(sell_orders) == 4 and all(order.profit < -1 for order in sell_orders):
#             if len(sell_hedge_q11) < 1 and buy_ctr_11 == 0:
#                 place_buy_order(symbol, opposite_qty11, magic_num=2001)
#                 buy_ctr_11 += 1
#                 print(f" buy counter is: {buy_ctr_11} ")
 
#     if len(sell_orders) == 7 and all(order.profit < -1 for order in sell_orders):
#             if len(sell_hedge_q09) < 1 and buy_ctr_09 == 0:
#                 place_buy_order(symbol, opposite_qty09, magic_num=2001)
#                 buy_ctr_09 += 1
#                 print(f" buy counter is: {buy_ctr_09} ")
 
#     if len(sell_orders) == 10 and all(order.profit < -1 for order in sell_orders):
#             if len(sell_hedge_q08) < 1 and buy_ctr_08 == 0:
#                 place_buy_order(symbol, opposite_qty08, magic_num=2001)
#                 buy_ctr_08 += 1
#                 print(f" buy counter is: {buy_ctr_08} ")
    

#     if len(sell_orders) == 13 and all(order.profit < -1 for order in sell_orders):
#             if len(sell_hedge_q07) < 1 and buy_ctr_07 == 0:
#                 place_buy_order(symbol, opposite_qty07, magic_num=2001)
#                 buy_ctr_07 += 1
#                 print(f" buy counter is: {buy_ctr_07} ")
    

#     if len(sell_orders) == 16 and all(order.profit < -1 for order in sell_orders):
#             if len(sell_hedge_q06) < 1 and buy_ctr_06 == 0:
#                 place_buy_order(symbol, opposite_qty06, magic_num=2001)
#                 buy_ctr_06 += 1
#                 print(f" buy counter is: {buy_ctr_06} ")
          
#     if len(sell_orders) == 20 and all(order.profit < -1 for order in sell_orders):
#             if len(sell_hedge_q15) < 1:
#                 place_buy_order(symbol, opposite_qty15, magic_num=2001)
 
#   #*********************************RESET COUNTER************************
      
#     if len(sell_hedge_q15) > 0 or len(sell_hedge_q06) > 0 or len(sell_hedge_q07) > 0 or len(sell_hedge_q08) > 0 or len(sell_hedge_q09) > 0: 
#         if len(sell_orders) < 1:
#             buy_ctr_11 = 0
#     elif len(sell_orders) <= 1:
#             buy_ctr_11 = 0 
   
#     if len(sell_hedge_q15) > 0 or len(sell_hedge_q06) > 0 or len(sell_hedge_q07) > 0 or len(sell_hedge_q08) > 0: 
#         if len(sell_orders) <= 3:
#             buy_ctr_09 = 0
#     elif len(sell_orders) <= 4:
#             buy_ctr_09 = 0 


#     if len(sell_hedge_q15) > 0 or len(sell_hedge_q06) > 0 or len(sell_hedge_q07) > 0: 
#         if len(sell_orders) <= 6:
#             buy_ctr_08 = 0
#     elif len(sell_orders) <= 7:
#             buy_ctr_08 = 0 
    

#     if len(sell_hedge_q15) > 0 or len(sell_hedge_q06) > 0: 
#         if len(sell_orders) <= 9:
#             buy_ctr_07 = 0
#     elif len(sell_orders) <= 10:
#             buy_ctr_07 = 0 
   
#     if len(sell_hedge_q15) > 0: 
#         if len(sell_orders) <= 12:
#             buy_ctr_06 = 0
#     elif len(sell_orders) <= 13:
#             buy_ctr_06 = 0 
 
#  #*****************************
 
#     if len(sell_hedge_q15) > 0:
#         for i in range(1, 50):  # i goes from 1 to 50
#             if any(order.profit <= i * -100 for order in sell_hedge_q15) and buy_ctr_04 < i:
#                 if not any(-6 <= order.profit <= 6 for order in buy_ord_hedge_04):
#                     place_sell_order(symbol, opposite_qty04, magic_num=4001)
#                     buy_ctr_04 += 1
#                     print(f" buy counter is: {buy_ctr_04} ")
#                     break
#     else:
#         buy_ctr_04 = 0

#     if len(buy_hedge_q15) > 0:
#         for i in range(1, 50):  # i goes from 1 to 50
#             if any(order.profit <= i * -100 for order in buy_hedge_q15) and sell_ctr_04 < i:
#                 if not any(-6 <= order.profit <= 6 for order in sell_ord_hedge_04):
#                     place_buy_order(symbol, opposite_qty04, magic_num=3001)
#                     sell_ctr_04 += 1
#                     print(f" sell counter is: {sell_ctr_04} ")
#                     break
#     else:
#         sell_ctr_04 = 0
   

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


# ========== DETECT BAND TOUCH ==========
def detect_band_touch(df, label):
    price = df['Close'].iloc[-1]
    upper = df['BB_Upper'].iloc[-1]
    lower = df['BB_Lower'].iloc[-1]
    middle = df['BB_Middle'].iloc[-1]

    return price, upper, lower, middle


def process_hedging_orders(symbol):

    hedging_sell_update_sl_all(symbol)
    hedging_buy_update_sl_all(symbol)
    hedging_sell_update_sl_04(symbol)
    hedging_buy_update_sl_04(symbol)

def place_general_orders_buy_sell(symbol):
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

    monitor_and_place_opposite_orders(symbol)

    # process_hedging_orders(symbol)

    close_profitable_small_orders(symbol)
    close_orders_based_on_conditions(symbol, buy_magic_num, sell_magic_num)

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

    m5_trend, m5_macd = get_macd_trend(symbol, mt5.TIMEFRAME_M5)
    m15_trend, m15_macd = get_macd_trend(symbol, mt5.TIMEFRAME_M15)
    h1_trend, h1_macd = get_macd_trend(symbol, mt5.TIMEFRAME_H1)

    # ========== GET Bollinger bands DATA ==========
    df_15m_data = get_mt5_data(symbol, mt5.TIMEFRAME_M15, NUM_CANDLES)
    df_15m_bb = add_bollinger_bands(df_15m_data)
    price_15m, upper_band_15m, lower_band_15m, middle_band_15m = detect_band_touch(df_15m_bb, "15-Minute")
    bb_gap = round(upper_band_15m - lower_band_15m, 0)

    # print(f"15m BB Gap: {bb_gap} | M5 trend: {m5_trend} | M15 trend: {m15_trend} | H1 trend: {h1_trend}, low: {lower_band_15m}, mid: {middle_band_15m}, up: {upper_band_15m }")

    buy_positions_with_initial_order = [
    pos for pos in positions if pos.type == mt5.ORDER_TYPE_BUY and pos.magic == buy_magic_num]

    sell_positions_with_initial_order = [
    pos for pos in positions if pos.type == mt5.ORDER_TYPE_SELL and pos.magic == sell_magic_num]

    buy_order_index = len(buy_positions)
    sell_order_index = len(sell_positions)

    if not buy_positions:
        # if ((m5_trend == "BUY" or m15_trend == "BUY" or h1_trend == "BUY") \
        # or (m5_trend == "RANGE" and m15_trend == "RANGE" and h1_trend == "RANGE")) and buy_price <= middle_band_15m:  # Initial buy condition
        buy_order_qty = lot_sizes[0]
        place_buy_order(symbol, buy_order_qty, buy_magic_num)
    else:
        latest_buy_position_price = buy_positions[0].price_open
        buy_order_qty = lot_sizes[buy_order_index] if buy_order_index < len(lot_sizes) else lot_sizes[-1]

        if buy_price <= latest_buy_position_price - pips_300 * mt5.symbol_info(symbol).point:
            # if buy_order_index < len(lot_sizes) and (m5_trend == "BUY" or m15_trend == "BUY" or h1_trend == "BUY"):
            if buy_order_index < len(lot_sizes):
                place_buy_order(symbol, buy_order_qty, buy_magic_num)

    if not sell_positions:
        # if ((m5_trend == "SELL" or m15_trend == "SELL" or h1_trend == "SELL") \
        # or (m5_trend == "RANGE" and m15_trend == "RANGE" and h1_trend == "RANGE")) and sell_price >= middle_band_15m:
        sell_order_qty = lot_sizes[0]
        place_sell_order(symbol, sell_order_qty, sell_magic_num)
    else:
        latest_sell_position_price = sell_positions[0].price_open
        sell_order_qty = lot_sizes[sell_order_index] if sell_order_index < len(lot_sizes) else lot_sizes[-1]

        if sell_price >= latest_sell_position_price + pips_300 * mt5.symbol_info(symbol).point:
            # if sell_order_index < len(lot_sizes) and (m5_trend == "SELL" or m15_trend == "SELL" or h1_trend == "SELL"):
            if sell_order_index < len(lot_sizes):
                place_sell_order(symbol, sell_order_qty, sell_magic_num)


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
