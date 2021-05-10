import logging.handlers

from time import sleep
from .notifications import NotificationHandler
from telebot import TeleBot


class Logger:

    Logger = None
    NotificationHandler = None

    def __init__(self, logging_service="crypto_trading", enable_notifications=True):
        # Logger setup
        self.Logger = logging.getLogger(f"{logging_service}_logger")

        self.telegram_bot = TeleBot("1341634120:AAGlTBi6QTvgGwf9C5VDZGldLTEXgAtVUjQ", parse_mode=None)

        self.Logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        # default is "logs/crypto_trading.log"
        fh = logging.FileHandler(f"logs/{logging_service}.log")
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        self.Logger.addHandler(fh)

        # logging to console
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(formatter)
        self.Logger.addHandler(ch)

        # notification handler
        self.NotificationHandler = NotificationHandler(enable_notifications)

    def log(self, message, level="info", notification=True, telegram_highlight=True, telegram_parse_mode=None):
        if level == "info":
            self.Logger.info(message)
        elif level == "warning":
            self.Logger.warning(message)
        elif level == "error":
            self.Logger.error(message)
        elif level == "debug":
            self.Logger.debug(message)

        if telegram_highlight:
            parse_mode = telegram_parse_mode
            try:
                self.telegram_bot.send_message(182552976, message, parse_mode=parse_mode)
                sleep(0.3)
            except Exception as e:
                sleep(5)
                self.telegram_bot.send_message(182552976, str(e))

        if notification and self.NotificationHandler.enabled:
            self.NotificationHandler.send_notification(message)

    def info(self, message, notification=True, telegram_highlight=True, telegram_parse_mode=None):
        self.log(message, "info", notification, telegram_highlight, telegram_parse_mode)

    def warning(self, message, notification=True, telegram_highlight=True, telegram_parse_mode=None):
        self.log(message, "warning", notification, telegram_highlight, telegram_parse_mode)

    def error(self, message, notification=True, telegram_highlight=True, telegram_parse_mode=None):
        self.log(message, "error", notification, telegram_highlight, telegram_parse_mode)

    def debug(self, message, notification=True, telegram_highlight=True, telegram_parse_mode=None):
        self.log(message, "debug", notification, telegram_highlight, telegram_parse_mode)
