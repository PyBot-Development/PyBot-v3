import threading
from resources import bot
import sys
import colorama

# Setting up variables
__version__ = "1.0.9"
sys.dont_write_bytecode = True
bot = threading.Thread(target=bot.run())
# Setting up variables

bot.start()