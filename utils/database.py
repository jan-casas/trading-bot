# database.py

import psycopg2
from psycopg2.extras import execute_values
from config.config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
from utils.logger import log_error

class Database:
    def __init__(self):
        try:
            self.conn = psycopg2.connect(
                host=DB_HOST,
                port=DB_PORT,
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )
            self.cursor = self.conn.cursor()
            self.create_tables()
        except Exception as e:
            log_error(f"Database connection failed: {e}")

    def create_tables(self):
        create_trades_table = """
        CREATE TABLE IF NOT EXISTS trades (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP,
            action VARCHAR(10),
            symbol VARCHAR(10),
            quantity NUMERIC,
            price NUMERIC,
            entry_price NUMERIC,
            stop_loss NUMERIC,
            take_profit NUMERIC,
            profit NUMERIC
        );
        """
        self.cursor.execute(create_trades_table)
        self.conn.commit()

    def insert_trade(self, trade_data):
        insert_query = """
        INSERT INTO trades (timestamp, action, symbol, quantity, price, entry_price, stop_loss, take_profit, profit)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        try:
            self.cursor.execute(insert_query, trade_data)
            self.conn.commit()
        except Exception as e:
            log_error(f"Failed to insert trade data: {e}")

    def get_trades_summary(self):
        query = """
        SELECT
            COUNT(*) FILTER (WHERE action = 'buy') AS total_buys,
            COUNT(*) FILTER (WHERE action = 'sell') AS total_sells,
            SUM(profit) AS net_profit
        FROM trades;
        """
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchone()
            total_buys = result[0] or 0
            total_sells = result[1] or 0
            net_profit = result[2] or 0.0
            total_trades = total_buys + total_sells
            summary = {
                'total_trades': total_trades,
                'total_buys': total_buys,
                'total_sells': total_sells,
                'net_profit': net_profit
            }
            return summary
        except Exception as e:
            log_error(f"Failed to get trades summary: {e}")
            return {}
    
    def close(self):
        self.cursor.close()
        self.conn.close()
