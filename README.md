# Binance Trading Bot

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

A Python-based trading bot for Binance that implements various trading strategies with backtesting capabilities and risk management features.

---

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
  - [Running the Bot](#running-the-bot)
  - [API Server](#api-server)
  - [Updating Strategies at Runtime](#updating-strategies-at-runtime)
- [Strategies](#strategies)
- [Backtesting](#backtesting)
- [Risk Management](#risk-management)
- [Logging and Monitoring](#logging-and-monitoring)
- [Email Reporting](#email-reporting)
- [Contributing](#contributing)
- [License](#license)
- [Disclaimer](#disclaimer)
- [Contact](#contact)

---

## Features

- **Multiple Trading Strategies**: Supports strategies like Mean Reversion, Moving Average Crossover, RSI, Breakout, and Combined Strategies, located in the `strategies` directory.
- **Scheduled Trading**: Uses a scheduler to run different strategies at specified times, configured in `config/config.py`.
- **Risk Management**: Implements risk management techniques in `utils/risk_management.py`, including position sizing, stop-loss, and take-profit mechanisms.
- **Backtesting**: Includes backtesting capabilities in `backtesting/backtest.py` to evaluate strategy performance on historical data.
- **Logging**: Comprehensive logging of trading activities and errors in `utils/logger.py`.
- **Email Reporting**: Sends weekly email reports with trading summaries and backtest results using the `send_email_report` function in `main.py`.
- **Database Integration**: Stores trading data in a PostgreSQL database, managed via `utils/database.py`.
- **API Server**: Provides an API server in `api_server.py` for interacting with the bot programmatically.
- **Modular Design**: Easily add or modify strategies due to the modular structure.
- **Extensive Configuration Options**: Customize trading parameters, schedules, and risk settings.

---

## Prerequisites

Before you begin, ensure you have met the following requirements:

- **Python 3.7 or higher**: Install Python from the [official website](https://www.python.org/downloads/).
- **PostgreSQL database**: Install and set up a PostgreSQL database. Instructions can be found [here](https://www.postgresql.org/download/).
- **Binance account with API key and secret**: Sign up at [Binance](https://www.binance.com/) and create API keys.
- **An SMTP server for sending emails**: You can use services like Gmail SMTP, but make sure to enable less secure apps if required.

---

## Installation

Follow these steps to set up the trading bot on your local machine.

### 1. Clone the Repository

```sh
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name
```

### 2. Create a Virtual Environment

Create and activate a virtual environment to manage dependencies.

```sh
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install Required Packages

Install the necessary Python packages using `pip`.

```sh
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the root directory with the following content:

```env
# Binance API Keys
BINANCE_API_KEY=your_api_key
BINANCE_API_SECRET=your_api_secret

# Database Settings
DB_HOST=localhost
DB_PORT=5432
DB_NAME=trading_bot
DB_USER=your_db_user
DB_PASSWORD=your_db_password

# Email Settings
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email@example.com
EMAIL_HOST_PASSWORD=your_email_password
EMAIL_USE_TLS=True
EMAIL_RECEIVER=recipient_email@example.com
```

**Note**: Replace the placeholder values with your actual credentials. Keep this file secure and do not commit it to version control.

### 5. Initialize the Database

Create the necessary tables in your PostgreSQL database.

```python
# Initialize the database
from utils.database import Database
db = Database()
db.create_tables()
db.close()
```

Alternatively, you can run a script or use a database migration tool.

---

## Configuration

All configurable parameters are located in `config/config.py`.

- **API Keys and Secrets**: Loaded from the `.env` file.
- **Trading Settings**:
  - `TRADING_PAIRS`: List of trading pairs (e.g., `['BTCUSDT', 'ETHUSDT']`).
  - `TIMEFRAME`: Timeframe for candles (e.g., `'1d'` for daily).
- **Risk Management Settings**:
  - `RISK_PER_TRADE`: Percentage of account balance to risk per trade.
  - `MAX_DRAWDOWN`: Maximum allowed drawdown.
  - `MAX_CONCURRENT_TRADES`: Maximum number of trades at once.
  - `TAKE_PROFIT_PERCENTAGE`: Percentage for take-profit.
  - `STOP_LOSS_PERCENTAGE`: Percentage for stop-loss.
- **Logging Settings**:
  - `LOG_FILE`: File path for logging.
- **Database Settings**: Connection parameters, loaded from the `.env` file.
- **Email Settings**: SMTP server details for email reporting, loaded from the `.env` file.

---

## Usage

### Running the Bot

Start the trading bot by executing:

```sh
python main.py
```

This will initialize the scheduler and run the strategies at their configured times.

### API Server

To interact with the bot via API, run:

```sh
python api_server.py
```

Ensure that you have Flask installed and configured.

### Updating Strategies at Runtime

The bot supports updating strategy schedules and parameters at runtime via the API server or by modifying the configuration files and restarting the bot.

---

## Strategies

Strategies are located in the `strategies` directory and are modularly designed to facilitate easy addition and modification.

- **Base Strategy**: Defined in `strategies/base_strategy.py`, providing a template for all strategies.
- **Indicators**: Common indicators are implemented in `strategies/indicators.py`.
- **RSI Strategy**: Implemented in `strategies/rsi_strategy.py`.
- **Moving Average Strategy**: Implemented in `strategies/moving_average_strategy.py`.
- **Mean Reversion Strategy**: Implemented in `strategies/mean_reversion_strategy.py`.
- **Breakout Strategy**: Implemented in `strategies/breakout_strategy.py`.
- **Combined Strategy**: Combines multiple strategies in `strategies/combined_strategy.py`.

Strategy parameters and schedules can be configured in `config/config.py` under `STRATEGY_PARAMETERS`.

---

## Backtesting

Backtesting functionality is provided in `backtesting/backtest.py`.

- **Running Backtests**: Execute `backtest.py` to evaluate strategy performance on historical data.
- **Including in Reports**: Backtest results are included in the weekly email reports.
- **Data Storage**: Historical data is stored in `backtesting/historical_data/`.

### Example

```sh
python backtesting/backtest.py
```

---

## Risk Management

Risk management is handled in `utils/risk_management.py`.

- **Position Sizing**: Calculates position sizes based on account balance and risk per trade.
- **Stop-Loss and Take-Profit**: Automatically sets stop-loss and take-profit levels.
- **Maximum Drawdown**: Monitors and limits the maximum drawdown to prevent excessive losses.
- **Concurrency Limits**: Controls the maximum number of open trades.

---

## Logging and Monitoring

Logging is configured in `utils/logger.py`.

- **Log Files**: Logs are saved to `logs/trading_bot.log`.
- **Log Levels**: Includes information logs, error logs, and trade logs.
- **Usage**: Use `log_info`, `log_error`, and `log_trade` functions for consistent logging.

---

## Email Reporting

Weekly email reports are sent using the `send_email_report` function in `main.py`.

- **Report Contents**: Includes trade summaries, net profit, and backtest performance.
- **Scheduling**: Configured to run every Sunday at 12:00 UTC using the scheduler.
- **Configuration**: Email settings are specified in the `.env` file.

---

## Contributing

Contributions are welcome! Please follow these guidelines:

1. **Fork the Repository**: Click the "Fork" button on the top right to create a personal copy of the repository.

2. **Clone Your Fork**:

   ```sh
   git clone https://github.com/yourusername/your-repo-name.git
   ```

3. **Create a New Branch**:

   ```sh
   git checkout -b feature/your-feature-name
   ```

4. **Make Changes**: Implement your feature or bug fix.

5. **Commit Changes**:

   ```sh
   git commit -am 'Add new feature'
   ```

6. **Push to Your Fork**:

   ```sh
   git push origin feature/your-feature-name
   ```

7. **Submit a Pull Request**: Go to the original repository and open a pull request.

### Code of Conduct

Please adhere to the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md).

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Disclaimer

**Trading cryptocurrencies involves significant risk and may result in the loss of your capital.**

- **No Investment Advice**: This project is for educational purposes only and does not constitute investment advice.
- **Use at Your Own Risk**: The authors are not responsible for any financial losses incurred while using this bot.
- **Regulatory Compliance**: Ensure that you comply with all local laws and regulations before using the bot.

---

## Contact

For questions or support, please open an issue or contact the maintainer at [your_email@example.com](mailto:your_email@example.com).

---

_Back to top_

---

This README provides an overview of the trading bot, its features, and instructions for setting it up and running. For detailed implementation, refer to the individual modules in the codebase.

**Happy Trading!**