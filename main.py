import pandas as pd
import time
from binance.client import Client
from binance.exceptions import BinanceAPIException
from config.config import *
from utils.risk_management import (
    calculate_position_size,
    is_within_drawdown_limit,
    can_enter_new_trade,
)
from utils.logger import log_trade, log_error, log_info
from utils.database import Database
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_EXECUTED
from datetime import datetime
from strategy_manager import StrategyManager
from utils.email_reporter import send_email_report

def get_historical_data(client, symbol, lookback_days=500):
    klines = client.get_historical_klines(
        symbol,
        Client.KLINE_INTERVAL_1DAY,
        f"{lookback_days} days ago UTC"
    )
    data = pd.DataFrame(klines, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_asset_volume', 'number_of_trades',
        'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
    ])
    data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
    data[['open', 'high', 'low', 'close']] = data[['open', 'high', 'low', 'close']].astype(float)
    data.set_index('timestamp', inplace=True)
    return data

def run_strategy(strategy):
    log_info(f"Starting {strategy.get_name()}...")
    client = Client(API_KEY, API_SECRET)
    db = Database()
    open_trades = []  # Fetch open trades from database if necessary

    try:
        current_balance = float(client.get_asset_balance(asset='USDT')['free'])
        starting_balance = current_balance  # Update as needed

        if not is_within_drawdown_limit(current_balance, starting_balance):
            log_info("Maximum drawdown limit reached. Stopping the bot.")
            return

        for symbol in TRADING_PAIRS:
            data = get_historical_data(client, symbol)
            data = strategy.apply_indicators(data)
            signal = strategy.generate_signal(data)
            price = data['close'].iloc[-1]

            # Check if we can enter a new trade
            if not can_enter_new_trade(open_trades):
                log_info("Maximum concurrent trades limit reached.")
                break

            # Check if we already have an open trade for this symbol
            if any(trade['symbol'] == symbol for trade in open_trades):
                log_info(f"Trade already open for {symbol}.")
                continue

            if signal == 'buy':
                stop_loss_price = price * (1 - STOP_LOSS_PERCENTAGE)
                take_profit_price = price * (1 + TAKE_PROFIT_PERCENTAGE)
                quantity = calculate_position_size(current_balance, price, stop_loss_price)
                quantity = round(quantity, 6)  # Adjust precision as needed

                try:
                    # Place a limit buy order to ensure price
                    order = client.order_limit_buy(
                        symbol=symbol,
                        quantity=quantity,
                        price=str(price)
                    )
                    order_id = order['orderId']
                    log_trade('buy', symbol, quantity, price)
                    log_info(f"Limit buy order placed for {symbol} at price {price}, order ID: {order_id}")

                    # Wait for order to be filled
                    order_filled = False
                    attempts = 0
                    while not order_filled and attempts < 10:
                        order_status = client.get_order(symbol=symbol, orderId=order_id)
                        status = order_status['status']
                        if status == 'FILLED':
                            log_info(f"Order {order_id} for {symbol} filled.")
                            order_filled = True
                        elif status in ['CANCELED', 'REJECTED', 'EXPIRED']:
                            log_error(f"Order {order_id} for {symbol} not filled. Status: {status}")
                            break
                        else:
                            log_info(f"Waiting for order {order_id} to be filled. Current status: {status}")
                            time.sleep(30)  # Wait for 30 seconds before checking again
                            attempts += 1

                    if order_filled:
                        # Insert trade into database
                        trade_data = (
                            datetime.utcnow(), 'buy', symbol, quantity, price,
                            price, stop_loss_price, take_profit_price, None  # Profit is None for buy orders
                        )
                        db.insert_trade(trade_data)
                        open_trades.append({
                            'symbol': symbol,
                            'quantity': quantity,
                            'entry_price': price,
                            'stop_loss': stop_loss_price,
                            'take_profit': take_profit_price
                        })

                        # Place OCO order for stop-loss and take-profit
                        try:
                            oco_order = client.create_oco_order(
                                symbol=symbol,
                                side='SELL',
                                quantity=quantity,
                                price=str(round(take_profit_price, 2)),
                                stopPrice=str(round(stop_loss_price, 2)),
                                stopLimitPrice=str(round(stop_loss_price * 0.99, 2)),
                                stopLimitTimeInForce='GTC'
                            )
                            log_info(f"OCO order placed for {symbol}.")
                        except BinanceAPIException as e:
                            log_error(f"Failed to place OCO order for {symbol}: {e}")
                    else:
                        # Cancel the order if it was not filled after attempts
                        client.cancel_order(symbol=symbol, orderId=order_id)
                        log_info(f"Order {order_id} for {symbol} canceled after timeout.")
                except BinanceAPIException as e:
                    log_error(f"Binance API Exception occurred: {e}")
                except Exception as e:
                    log_error(f"An error occurred while placing buy order: {e}")

            elif signal == 'sell':
                # Implement sell logic if holding positions
                # Check if we have an open trade for this symbol
                trade = next((trade for trade in open_trades if trade['symbol'] == symbol), None)
                if trade:
                    quantity = trade['quantity']
                    entry_price = trade['entry_price']
                    try:
                        # Place market sell order
                        order = client.order_market_sell(
                            symbol=symbol,
                            quantity=quantity
                        )
                        # Assume we get the average price from the order fills
                        sell_price = float(order['fills'][0]['price'])
                        log_trade('sell', symbol, quantity, sell_price)
                        log_info(f"Market sell order placed for {symbol}, order ID: {order['orderId']}")

                        # Compute profit
                        profit = (sell_price - entry_price) * quantity

                        # Insert trade into database
                        trade_data = (
                            datetime.utcnow(), 'sell', symbol, quantity, sell_price,
                            None, None, None, profit
                        )
                        db.insert_trade(trade_data)

                        open_trades = [t for t in open_trades if t['symbol'] != symbol]
                    except BinanceAPIException as e:
                        log_error(f"Binance API Exception occurred while selling {symbol}: {e}")
                    except Exception as e:
                        log_error(f"An error occurred while placing sell order for {symbol}: {e}")
                else:
                    log_info(f"No open trade for {symbol} to sell.")

        log_info(f"{strategy.get_name()} run completed.")
    except Exception as e:
        log_error(f"An error occurred in {strategy.get_name()}: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    scheduler = BlockingScheduler()
    strategy_manager = StrategyManager()
    strategy_manager.load_strategies()

    def scheduler_error_listener(event):
        if event.exception:
            log_error(f"The scheduler job crashed: {event.exception}")
        else:
            log_info(f"Scheduler job executed successfully at {datetime.utcnow()}.")

    scheduler.add_listener(scheduler_error_listener, EVENT_JOB_ERROR | EVENT_JOB_EXECUTED)

    # Schedule each strategy with its own schedule
    for strategy in strategy_manager.get_strategies():
        params = STRATEGY_PARAMETERS[strategy.get_name()]
        schedule = params["schedule"]
        scheduler.add_job(
            run_strategy,
            'cron',
            args=[strategy],
            id=strategy.get_name(),
            **schedule
        )
        log_info(f"Scheduled {strategy.get_name()} to run at {schedule}")

    # Schedule the email report job (e.g., every Sunday at 12:00 UTC)
    scheduler.add_job(
        send_email_report,
        'cron',
        day_of_week='sun',
        hour=12,
        minute=0,
        id='email_report'
    )
    log_info("Scheduled email report to run every Sunday at 12:00 UTC")

    try:
        log_info("Scheduler started. Bot will run at scheduled times.")
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        log_info("Scheduler stopped.")
    except Exception as e:
        log_error(f"An unexpected error occurred in the scheduler: {e}")
        scheduler.shutdown()
