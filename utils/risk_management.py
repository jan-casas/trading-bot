from config.config import RISK_PER_TRADE, MAX_DRAWDOWN, MAX_CONCURRENT_TRADES

def calculate_position_size(account_balance, entry_price, stop_loss_price):
    risk_amount = account_balance * RISK_PER_TRADE
    stop_loss_amount = abs(entry_price - stop_loss_price)
    quantity = risk_amount / stop_loss_amount
    return quantity

def is_within_drawdown_limit(current_balance, starting_balance):
    drawdown = (starting_balance - current_balance) / starting_balance
    return drawdown <= MAX_DRAWDOWN

def can_enter_new_trade(open_trades):
    return len(open_trades) < MAX_CONCURRENT_TRADES


def calculate_position_size(account_balance, entry_price, stop_loss_price, atr):
    risk_amount = account_balance * RISK_PER_TRADE
    stop_loss_amount = atr  # Use ATR instead of fixed stop loss
    quantity = risk_amount / stop_loss_amount
    return quantity
