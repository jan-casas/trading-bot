import os
from dotenv import load_dotenv

load_dotenv()

# Binance API Keys
API_KEY = os.getenv('BINANCE_API_KEY')
API_SECRET = os.getenv('BINANCE_API_SECRET')

# Trading Settings
TRADING_PAIRS = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT']
TIMEFRAME = '1d'  # Daily candles

# Risk Management Settings
RISK_PER_TRADE = 0.02  # 2% of account balance
MAX_DRAWDOWN = 0.20  # 20% maximum drawdown
MAX_CONCURRENT_TRADES = 5
TAKE_PROFIT_PERCENTAGE = 0.10  # 10% take profit
STOP_LOSS_PERCENTAGE = 0.05  # 5% stop loss

# Logging Settings
LOG_FILE = 'logs/trading_bot.log'

# Database Settings
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'trading_bot')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')


# Email Settings
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True') == 'True'
EMAIL_RECEIVER = os.getenv('EMAIL_RECEIVER')

ACTIVE_STRATEGIES = [
    'strategies.combined_strategy.CombinedStrategy',
    'strategies.rsi_strategy.RSIStrategy',
    'strategies.moving_average_strategy.MovingAverageStrategy',
    'strategies.mean_reversion_strategy.MeanReversionStrategy',
    'strategies.breakout_strategy.BreakoutStrategy',
]

STRATEGY_PARAMETERS = {
    "Combined Strategy": {
        "RSI Strategy": {
            "rsi_period": 14,
            "buy_threshold": 30,
            "sell_threshold": 70,
        },
        "Moving Average Strategy": {
            "short_window": 50,
            "long_window": 200,
        },
        "Mean Reversion Strategy": {
            "z_score_window": 20,
            "buy_threshold": -2,
            "sell_threshold": 2,
        },
        "Breakout Strategy": {
            "atr_window": 14,
            "lookback_window": 20,
        },
        "schedule": {"hour": 6, "minute": 0},
    },
    "RSI Strategy": {
        "rsi_period": 14,
        "buy_threshold": 30,
        "sell_threshold": 70,
        "schedule": {"hour": 6, "minute": 0},
    },
    "Moving Average Strategy": {
        "short_window": 50,
        "long_window": 200,
        "schedule": {"hour": 7, "minute": 0},
    },
    "Mean Reversion Strategy": {
        "z_score_window": 20,
        "buy_threshold": -2,
        "sell_threshold": 2,
        "schedule": {"hour": 8, "minute": 0},
    },
    "Breakout Strategy": {
        "atr_window": 14,
        "lookback_window": 20,
        "schedule": {"hour": 9, "minute": 0},
    },
}

