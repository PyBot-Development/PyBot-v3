import threading
from resources import bot
import sys
import colorama

__version__ = "1.0.6"
sys.dont_write_bytecode = True
bot = threading.Thread(target=bot.run())
bot.start()