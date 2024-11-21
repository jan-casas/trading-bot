import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from utils.database import Database
from utils.logger import log_info, log_error
from config.config import (
    EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD,
    EMAIL_USE_TLS, EMAIL_RECEIVER, TRADING_PAIRS
)
from backtesting.backtest import backtest  # Adjust the import path as needed
import os

def send_email_report():
    log_info("Preparing to send email report...")
    db = Database()
    try:
        # Fetch data from database
        summary = db.get_trades_summary()
        total_trades = summary.get('total_trades', 0)
        total_buys = summary.get('total_buys', 0)
        total_sells = summary.get('total_sells', 0)
        net_profit = summary.get('net_profit', 0.0)

        # Compose email
        subject = "Weekly Trading Bot Report"
        body = f"""
        <html>
        <body>
        <h2>Weekly Trading Bot Report</h2>
        <p>Total Trades: {total_trades}</p>
        <p>Total Buys: {total_buys}</p>
        <p>Total Sells: {total_sells}</p>
        <p>Net Profit: {net_profit:.2f} USDT</p>
        """

        message = MIMEMultipart('related')
        message['From'] = EMAIL_HOST_USER
        message['To'] = EMAIL_RECEIVER
        message['Subject'] = subject

        message_alternative = MIMEMultipart('alternative')
        message.attach(message_alternative)

        # Backtest and attach plots for each symbol
        for idx, symbol in enumerate(TRADING_PAIRS):
            total_return, plot_filename = backtest(symbol)
            body += f"""
            <h3>Backtest Performance for {symbol}</h3>
            <p>Total Return: {total_return * 100:.2f}%</p>
            <img src="cid:backtest_plot_{idx}" alt="Backtest Plot for {symbol}" />
            """
            with open(plot_filename, 'rb') as f:
                img_data = f.read()
            image = MIMEImage(img_data)
            image.add_header('Content-ID', f'<backtest_plot_{idx}>')
            message.attach(image)

        body += "</body></html>"
        message_alternative.attach(MIMEText(body, 'html'))

        # Connect to SMTP server and send email
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        if EMAIL_USE_TLS:
            server.starttls()
        server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
        server.send_message(message)
        server.quit()
        log_info("Email report sent successfully.")

        # Clean up plot images
        for idx, symbol in enumerate(TRADING_PAIRS):
            plot_filename = f'backtest_{symbol}.png'
            if os.path.exists(plot_filename):
                os.remove(plot_filename)
    except Exception as e:
        log_error(f"An error occurred while sending email report: {e}")
    finally:
        db.close()