import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound
from discord.ext.commands import cooldown, BucketType
import yaml
import asyncio
from datetime import datetime
from colorama import *
import random
try: import support
except: from resources import support
import urllib.parse, urllib.request, re
import pyfiglet
import io
import aiohttp
import string
import sqlite3
import tweepy
import os
import sys
import json
import re
try: import quotes
except: from resources import quotes
try: import processing
except: from resources import processing

startup_time=datetime.utcnow().strftime("%c")
path=f"{__file__}".replace("\\resources\\bot.py", "").replace("/resources/bot.py", "")
config=open(f"{path}/config.yaml")
config=yaml.load(config, Loader=yaml.FullLoader)
_prefix=config.get("prefix")
_cooldown=config.get("cooldown")
bot=commands.Bot(command_prefix=commands.when_mentioned_or(_prefix), case_insensitive=True)
bot.remove_command('help')
bot.ascii_font = pyfiglet.Figlet(font='roman')
b_react=False
consumer_key=config.get("Twitter_Consumer_Key")
consumer_secret=config.get("Twitter_Consumer_Secret")
access_token=config.get("Twitter_Access_Token")
access_token_secret=config.get("Twitter_Access_Token_Secret")
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
con = sqlite3.connect(f'{path}/data/database.db')
c = con.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (id text, username text, admin text, banned text, ban_reason text, banned_by text, banned_date text, ban_duration text)''')
c.execute('''CREATE TABLE IF NOT EXISTS banned_channels (id text, channel_name text)''')
c.execute('''CREATE TABLE IF NOT EXISTS badwords (word text)''')
c.execute('''CREATE TABLE IF NOT EXISTS disabled_cmds (command text)''')
#c.execute('''ALTER TABLE users ADD COLUMN ban_duration text;''')
log_location = startup_time.replace(":", "_").replace(" ", "-")
with open(f"{path}/logs/{log_location}.log", "a+") as file:
    file.write(f"[STARTUP] {startup_time}       {random.choice(quotes.prequel)}\n")
class colours:
    red = 0xff3d3d
    green = 0xb8ff3d
    blue = 0x2e66ff
    yellow = 0xfff94d

def ban_check_by_id(user_id):
    l_banned = c.execute(f"SELECT banned FROM users WHERE id=\"{user_id}\"").fetchall()
    timetounban = c.execute(f"SELECT ban_duration FROM users WHERE id=\"{user_id}\"").fetchall()
    try: timetounban = int(round(float(list(timetounban[0])[0]))); tmp_ban = True
    except: tmp_ban = False
    con.commit()
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    if tmp_ban and l_banned == [('1',)] and timetounban <= timestamp:
        c.execute(f'''UPDATE users SET banned="0" WHERE id={user_id} ''')
        con.commit()
        return(False)
    if l_banned == [('1',)]: return(True)
    else: return(False)
def admin_check_by_id(user_id):
    l_admins = c.execute(f"SELECT admin FROM users WHERE id=\"{user_id}\"").fetchall()
    con.commit()
    if l_admins == [('1',)]: return(True)
    else: return(False)
def check_for_badwords(mess, prefix, command):
    l_badwords = []
    for row in c.execute(f"SELECT word FROM badwords"): l_badwords.append(row[0])
    con.commit()
    l_strip = [".", ",", ";", ":", "\\", "/", "-", "_", "​", " ", " ", " ", " ", " ", " ", " ", " ", " ", "⠀", " ", f"{prefix}{command}"]
    for letter in l_strip: mess = mess.replace(letter, "")
    if any(item.lower() in mess for item in l_badwords):
        return(True)
    else:
        return(False)
def disabled_cmd_check(command):
    l_disabled_commands=[]
    for row in c.execute(f'SELECT * FROM disabled_cmds'): l_disabled_commands.append(str(row[0]))
    con.commit()
    for item in l_disabled_commands:
        if item in str(command): return(True)
    return(False)
def banned_channel_check(channel_id):
    l_banned_channels=[]
    for row in c.execute(f'SELECT * FROM banned_channels WHERE id="{channel_id}"'): l_banned_channels.append(int(row[0]))
    con.commit()
    if len(l_banned_channels)!=0: return(True)
    else: return(False)
def c_chck():
    async def checker(ctx):
        if c.execute(f'SELECT * FROM users WHERE id={ctx.message.author.id}').fetchone() == None or c.execute(f'SELECT * FROM users WHERE id={ctx.message.author.id}').fetchone() == "None":
            c.execute(f'''INSERT INTO users VALUES ("{int(ctx.message.author.id)}", "{str(ctx.message.author)}", "0", "0", "Null", "Null", "Null", "Null")''')
        else: pass
        con.commit()
        b_disabled_cmd = disabled_cmd_check(ctx.command)
        b_banned_channel = banned_channel_check(ctx.message.channel.id)
        b_banned = ban_check_by_id(ctx.message.author.id)
        b_admin = admin_check_by_id(ctx.message.author.id)
        b_badwords = check_for_badwords(ctx.message.content, _prefix, ctx.command)

        now=datetime.now()
        date=('%02d:%02d:%02d'%(now.hour,now.minute,now.second))
        with open(f"{path}/logs/{log_location}.log", "a+") as file:
            file.write("\n" + f"{date} [CMD] \'{ctx.message.author}\': \'{ctx.message.content}\' guild: \'{ctx.message.guild}\' channel: \'{ctx.message.channel}\'")
        print(f"{Back.BLACK}{Fore.WHITE}{date}{Style.RESET_ALL}{Fore.LIGHTYELLOW_EX} [CMD]{Style.RESET_ALL} {Fore.LIGHTBLUE_EX}{ctx.message.author}: {Fore.LIGHTGREEN_EX}{ctx.message.content}{Style.RESET_ALL} {Fore.LIGHTBLUE_EX}channel: {Fore.LIGHTGREEN_EX}{ctx.message.channel}{Style.RESET_ALL} {Fore.LIGHTBLUE_EX}guild: {Fore.LIGHTGREEN_EX}{ctx.message.guild}{Style.RESET_ALL}")
        if ctx.message.author.id == 846298981797724161 or b_admin: 
            if b_react: 
                try: await ctx.message.add_reaction("✅")
                except: pass
            return(True)
        elif b_banned_channel==True: await ctx.message.add_reaction("❌"); channel=await ctx.message.author.create_dm(); await channel.send(embed=discord.Embed(description=f"Channel <#{ctx.message.channel.id}> is not allowed. Try again in different one.", color=colours.blue)); return(False)
        elif b_disabled_cmd==True: await ctx.message.add_reaction("❌") ; await ctx.send(embed=discord.Embed(description=f"❌ Command `{ctx.command}` is disabled.", color=colours.blue), delete_after=10); return(False)
        elif b_badwords==True: await ctx.message.add_reaction("❌"); await ctx.send(embed=discord.Embed(description="❌ Sorry, but some word isn't allowed here.", color=colours.blue), delete_after=10); return(False)
        elif b_banned==True: await ctx.message.add_reaction("❌"); await ctx.send(embed=discord.Embed(description="❌ Sorry, but you're banned from using any bot commands.", color=colours.blue), delete_after=10); return(False)
        else: 
            if b_react: 
                try: await ctx.message.add_reaction("✅")
                except: pass
            return(True)
    return commands.check(checker)
def c_achck():
    async def checker(ctx):
        b_admin = admin_check_by_id(ctx.message.author.id)
        if b_admin or ctx.message.author.id==846298981797724161: return(True); 
        else: await ctx.send(embed=discord.Embed(description=config.get("no-perms"), color=colours.yellow), delete_after=10); print(f"{Back.LIGHTYELLOW_EX}{Fore.BLACK}[NO PERMS]{Style.RESET_ALL} {ctx.message.author} {Fore.LIGHTBLUE_EX}channel: {Fore.LIGHTGREEN_EX}{ctx.message.channel}{Style.RESET_ALL} {Fore.LIGHTBLUE_EX}guild: {Fore.LIGHTGREEN_EX}{ctx.message.guild}{Style.RESET_ALL}");return False
    return commands.check(checker)
@bot.listen('on_message')
async def BadWordOnChat(message):
    if message.author.id == 846298981797724161: return True
    now=datetime.now()
    date=('%02d:%02d:%02d'%(now.hour,now.minute,now.second))
    mess = str(message.content.lower())
    strip_things = ["]", "[", "\'", "\"",".", ",", ";", ":", "\\", "/", "-", "_", "​", " ", " ", " ", " ", " ", " ", " ", " ", " ", "⠀", " "]
    data = c.execute(f"SELECT admin FROM users WHERE id=\"{message.author.id}\"")
    l_admins = data.fetchall()
    con.commit()
    l_badwords = []
    for row in c.execute(f"SELECT word FROM badwords"): l_badwords.append(row[0])
    con.commit()
    for letter in strip_things: _mess = mess.replace(letter, "")
    if any(item in mess for item in l_badwords) and str(l_admins)!="[('1',)]" or any(item in _mess for item in l_badwords) and str(l_admins)!="[('1',)]":
        with open(f"{path}/logs/{log_location}.log", "a+") as file:
            file.write(f"{date} [BADWORD] {message.author}: '{message.content}' guild: '{message.guild}' channel: '{message.channel}' \n")
        print(f"{Back.BLACK}{Fore.WHITE}{date}{Style.RESET_ALL} {Back.LIGHTRED_EX}{Fore.BLACK}[BADWORD]{Style.RESET_ALL} {Fore.LIGHTBLUE_EX}{message.author}: {message.content}{Style.RESET_ALL} {Fore.LIGHTBLUE_EX}channel: {Fore.LIGHTGREEN_EX}{message.channel}{Style.RESET_ALL} {Fore.LIGHTBLUE_EX}guild: {Fore.LIGHTGREEN_EX}{message.guild}{Style.RESET_ALL}")
        try:
            channel = await message.author.create_dm()
            embed=discord.Embed(description="❌ Watch your language.", color=colours.blue)
            await channel.send(embed=embed)
        except: await message.send(f"Watch your language {message.author.mention}!")
        try: await message.delete()
        except: 
            try: await message.add_reaction("😠")
            except: pass
@bot.event
async def on_command_error(ctx, error):
    now=datetime.now()
    date=('%02d:%02d:%d'%(now.hour,now.minute,now.second))
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(embed=discord.Embed(description=config.get("command-on-cooldown").format(error.retry_after), color=colours.yellow), delete_after=10)
        return
    elif isinstance(error, commands.CheckFailure): return
    elif isinstance(error, CommandNotFound):
        await ctx.send(embed=discord.Embed(description=config.get("command-not-found"), color=colours.blue), delete_after=10)
        return
    elif isinstance(error, commands.MissingRequiredArgument):
        #help(ctx.command, _prefix)
        await ctx.send(embed=support.cmd_help(str(ctx.command), _prefix, len(bot.commands)), delete_after=30)
        return
    else:
        print(f"{Back.BLACK}{Fore.WHITE}{date}{Style.RESET_ALL} {Fore.RED}{Back.LIGHTBLACK_EX}[ERROR]{Style.RESET_ALL} {error}")
        await ctx.send(embed=discord.Embed(description=config.get("unknown").format(error), color=colours.blue), delete_after=10)
        raise error
        return
no_alts = False
try:
    try: alts = open(f"{path}/data/alts/mc.txt.txt", "r")
    except: alts = open(f"{path}/data/alts/raw/mc.txt", "r")
    alts_mc = []
    for item in alts:
        item = item.split("\n")
        alts_mc.append(item[0])
    alts.close()
except:
    no_alts = True
    print(f"{Fore.LIGHTWHITE_EX}{Back.RED}[E] No minecraft alts file found.{Style.RESET_ALL}")
@c_chck()
@bot.command(aliases=["?"])
@cooldown(1, _cooldown, BucketType.user)
async def help(ctx, arg="list"):
    async with ctx.typing():
        embed=support.cmd_help(arg,_prefix, len(bot.commands))
        embed.set_footer(text=f"""Requester: {ctx.message.author} • Today at: {datetime.utcnow().strftime("%X")} UTC""")
        channel = await ctx.message.author.create_dm()
        await channel.send(embed=embed)
@c_chck()
@bot.command(aliases=["tell", "sudo", "you-fat-bitch-say"])
@cooldown(1, _cooldown, BucketType.user)
async def say(ctx, *, arg):
    async with ctx.typing():
        await ctx.send(arg)
@c_chck()
@bot.command()
@cooldown(1, _cooldown, BucketType.user)
async def edited(ctx, msg_before, msg_after, time=2):
    if time > 120: await ctx.send(embed=discord.Embed(description="⚠️ Time max is 120", color=colours.blue), delete_after=10); return
    if msg_after == "": msg_after == "^ Idiot"
    elif msg_before == "": msg_before == "^ Idiot"
    try: float(time)
    except: await ctx.send(embed=discord.Embed(description="⚠️ Time must be float", color=colours.blue), delete_after=10)
    async with ctx.typing():
        Message = await ctx.send(msg_before)
        await asyncio.sleep(time)
        await Message.edit(content=msg_after)
@c_chck()
@bot.command(aliases=["mc_alt", "mcalt"])
@cooldown(1, 60, BucketType.user)
async def alt(ctx):
    async with ctx.typing():
        if no_alts == True: await ctx.send(embed=discord.Embed(description="No Alts left :(", color=colours.blue), delete_after=10); return
        alt = random.choice(alts_mc)
        channel = await ctx.message.author.create_dm()
        await channel.send(embed=discord.Embed(description=f"||{alt}||", color=colours.blue))
        alts_mc.remove(alt)
        alts = open(f"{path}/data/alts/mc.txt", "w+")
        alts.seek(0)
        for item in alts_mc:
            alts.write(f"{item}\n")
        alts.truncate()
        alts.close()
@c_chck()
@cooldown(1, _cooldown, BucketType.user)
@bot.command(aliases=['r', 'meter'])
async def rate(ctx, user, *, rest_of_the_text=""):
    async with ctx.typing():
        picked_random=random.randint(0, 100)
        thestuff = {
        "gay":   '%02x%02x%02x' % ( int(picked_random*random.uniform(0, 2.55)), int(picked_random*random.uniform(0, 2.55)), int(picked_random*random.uniform(0, 2.55))),
        "black": '%02x%02x%02x' % ( int(253-(picked_random*2.53)),              int(231-(picked_random*2.31)),              int(214-(picked_random*2.14))),
        "furry": '%02x%02x%02x' % ( int(picked_random*1.67),                    int(picked_random*1.99),                    int(picked_random*2.3)),
        "cum":   '%02x%02x%02x' % ( int(picked_random*2.55),                    int(picked_random*2.55),                    int(picked_random*2.55)),
        }
        if(picked_random > 50 and user.lower() == "gay" or picked_random > 50 and rest_of_the_text.lower() == "gay"):  rest_of_the_text = rest_of_the_text+"🏳️‍🌈"
        elif(picked_random > 50 and user.lower() == "furry" or picked_random > 50 and rest_of_the_text.lower() == "furry"): rest_of_the_text = f"{rest_of_the_text}<a:uwu:870669804233707580>"
        try:
            user = await commands.UserConverter().convert(ctx, user); msg = f"{user} is {picked_random}% {rest_of_the_text}."
            colour_hex = thestuff.get(rest_of_the_text.lower(), '%02x%02x%02x' % ( int(picked_random*1.55), int(picked_random*2.55), int(picked_random*1.33) ))
        except:
            if user.startswith("@$"):
                colour_hex = thestuff.get(rest_of_the_text.lower(), '%02x%02x%02x' % ( int(picked_random*1.55), int(picked_random*2.55), int(picked_random*1.33) ))
                msg = f"{user[2:]} is {picked_random}% {rest_of_the_text}."
            elif rest_of_the_text == "":
                colour_hex = thestuff.get(user.lower(), '%02x%02x%02x' % ( int(picked_random*1.55), int(picked_random*2.55), int(picked_random*1.33) ))
                msg = f"You're {picked_random}% {user}{rest_of_the_text}."
            else:
                colour_hex = thestuff.get(user.lower(), '%02x%02x%02x' % ( int(picked_random*1.55), int(picked_random*2.55), int(picked_random*1.33) ))
                msg = f"You're {picked_random}% {user} {rest_of_the_text}."
        colour = int(colour_hex, 16)
        embed=discord.Embed(title=msg, color=colour)
        embed.set_footer(text=f"""Requester: {ctx.message.author} • Today at: {datetime.utcnow().strftime("%X")} UTC""")
        await ctx.send(embed=embed)
@c_chck()
@cooldown(1, _cooldown, BucketType.user)
@bot.command(aliases=["cf"])
async def coinflip(ctx):
    async with ctx.typing():
        if(random.randint(0, 1)==1): embed=discord.Embed(description="It landed on Heads!", color=colours.blue); embed.set_image(url="attachment://heads.gif"); await ctx.send(file=discord.File(f"{path}/data/coinflip/heads.gif"), embed=embed)
        else: embed=discord.Embed(description="It landed on Tails!", color=colours.blue); embed.set_image(url="attachment://tails.gif"); await ctx.send(file=discord.File(f"{path}/data/coinflip/tails.gif"), embed=embed)
@c_chck()
@cooldown(1, _cooldown, BucketType.user)
@bot.command(aliases=["video", "youtube"])
async def yt(ctx, *, search):
    async with ctx.typing():
        query_string = urllib.parse.urlencode({'search_query': search})
        htm_content = urllib.request.urlopen('http://www.youtube.com/results?' + query_string)
        search_results = re.findall(r'/watch\?v=(.{11})', htm_content.read().decode())
        await ctx.send('http://www.youtube.com/watch?v=' + search_results[0])
@c_chck()
@cooldown(1, _cooldown, BucketType.user)
@bot.command()
async def ascii(ctx, *, arg):
    await ctx.send(f"```{bot.ascii_font.renderText(arg)}```")
@c_chck()
@cooldown(1, _cooldown, BucketType.user)
@bot.command()
async def font(ctx, *, arg):
    try:
        bot.ascii_font = pyfiglet.Figlet(font=arg)
        await ctx.send(embed=discord.Embed(description=f"Changed font to `{arg}`", color=colours.blue), delete_after=10)
    except: await ctx.send(embed=discord.Embed(description=f"Font `{arg}` not found.", color=colours.blue), delete_after=10)
@c_chck()
@bot.command(aliases=['dick', 'penis', 'cock'])
@cooldown(1, _cooldown, BucketType.user)
async def pp(ctx, *,user: discord.User=None):
        ppsize = random.uniform(0.00, 200.00); ppsize_inch = ppsize/2.54; colour_hex = '%02x%02x%02x' % ( int((ppsize/2)*2.31), int((ppsize/2)*1.45), int((ppsize/2)*2.55) ); colour = int(colour_hex, 16)
        if user == None: user = ctx.message.author
        embed=discord.Embed(description=f"{user} pp size is {ppsize:.2f}cm/{ppsize_inch:.2f}inch.", color=colour)
        embed.set_footer(text=f"""Requester: {ctx.message.author} • Today at: {datetime.utcnow().strftime("%X")} UTC""")
        await ctx.send(embed=embed)
@c_chck()
@bot.command()
@cooldown(1, _cooldown, BucketType.user)
async def hex(ctx, colour="random"):
    if colour=="random": colour = '%02x%02x%02x' %  ( int(random.randint(0, 255)), int(random.randint(0, 255)), int(random.randint(0, 255)))
    try: colour_send = colour.replace("#", "")
    except:
        await ctx.send('Enter Valid Hex')
        return
    if len(colour_send) < 6:
        num = 6 - len(colour_send)
        for i in range(0, num): colour_send = f"{colour_send}0"
    colour_int = int(colour_send, 16); rgb = tuple(int(colour_send[i:i+2], 16) for i in (0, 2, 4))
    await ctx.trigger_typing()
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f'https://some-random-api.ml/canvas/colorviewer?hex={colour_send}'
        ) as af:
            if 300 > af.status >= 200:
                fp = io.BytesIO(await af.read())
                file = discord.File(fp, "colour.png")
                colour = colour.replace("#", "")
                embed = discord.Embed(title=f"Colour: #{colour}", description=f"RGB: {rgb}",color=colour_int)
                embed.set_thumbnail(url="attachment://colour.png")
                embed.set_footer(text=f"""Requester: {ctx.message.author} • Today at: {datetime.utcnow().strftime("%X")} UTC""")
                await ctx.send(embed=embed, file=file)
            else:
                await ctx.send('Enter Valid Hex', delete_after=10)
            await session.close()
@c_chck()
@bot.command(aliases=["math", "cal", "calculate"])
@cooldown(1,_cooldown, BucketType.user)
async def calc(ctx, *, cal):
    chars = string.printable.replace("0123456789", "").replace("/", "").replace("+", "").replace("*", "").replace("-", "").replace(".", "").replace("(", "").replace(")", "")
    _math = str(cal.lower()).replace("pi", "3.141592653589793").replace("^", "**").replace("e", "2.71828")
    for item in chars: _math = _math.replace(item, "")
    for item in ["*", "/", "-", "+"]: __math = _math.split(item)
    _math_ = []
    for item in __math:
        if "**" in item: _math_.append(item)
    for item in _math_:
        x = item.split("**")
        if any(int(thing) > 1000 for thing in x): raise ValueError("Power Too Great.")
    z = []
    for item in _math_:
        x = item.split("**")
        for thing in x: z.append(thing)
    if len(z) > 3: raise ValueError("Too much powers.")
    if sum(z) > 5000: raise ValueError("Too much powers.")
    await ctx.send(embed=discord.Embed(description=f"{_math} = {eval(_math)}", color=colours.green).set_footer(text=f"""Requester: {ctx.message.author} • Today at: {datetime.utcnow().strftime("%X")} UTC"""))
@c_chck()
@c_achck()
@bot.command()
@cooldown(1,_cooldown, BucketType.user)
async def ban(ctx, user, *, reason="Not Specified."):
    reason=reason.replace("'", "\\'")
    user = await commands.UserConverter().convert(ctx, user)
    data = c.execute(f'SELECT * FROM users WHERE id={user.id}')
    con.commit()
    x = data.fetchone()
    if x == "None" or x == None:
        c.execute(f'''INSERT INTO users VALUES ("{int(user.id)}", "{str(user)}", "0", "1", "{str(reason)}", "{str(ctx.message.author.mention)}", "{datetime.utcnow()}", "Null")''')
        con.commit()
        await ctx.send(embed=discord.Embed(description=f"⚠️ Banned user {user.mention} from using bot commands.", color=colours.blue))
    else:
        c.execute(f'''UPDATE users SET banned="1", ban_reason="{reason}", banned_by="{str(ctx.message.author.mention)}", banned_date="{datetime.utcnow()}" WHERE id={user.id} ''')
        con.commit()
        await ctx.send(embed=discord.Embed(description="⚠️ Updated user ban.", color=colours.blue))
    channel = await user.create_dm()
    await channel.send(embed=discord.Embed(description=f"""You've been banned from using bot by {ctx.message.author.mention}.
Reason: `{reason}`""",color=colours.blue))
    con.commit()

@c_chck()
@c_achck()
@bot.command()
@cooldown(1,_cooldown, BucketType.user)
async def tempban(ctx, user, time, *, reason="Not Specified."):
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    time=time.replace("s", "*1+").replace("m", "*60+").replace("h", "*(60*60)+").replace("d", "*86400+").replace("w", "*604800+")
    time=int(eval(time[:-1]))
    timestamp=timestamp+time
    time=datetime.fromtimestamp(timestamp)
    reason=reason.replace("'", "\\'")

    user = await commands.UserConverter().convert(ctx, user)
    data = c.execute(f'SELECT * FROM users WHERE id={user.id}')
    con.commit()
    x = data.fetchone()
    if x == "None" or x == None:
        c.execute(f'''INSERT INTO users VALUES ("{int(user.id)}", "{str(user)}", "0", "1", "{str(reason)}", "{str(ctx.message.author.mention)}", "{datetime.utcnow()}, "{timestamp}")''')
        con.commit()
        await ctx.send(embed=discord.Embed(description=f"⚠️ Banned user {user.mention} from using bot commands.", color=colours.blue))
    else:
        c.execute(f'''UPDATE users SET banned="1", ban_reason="{reason}", banned_by="{str(ctx.message.author.mention)}", banned_date="{datetime.utcnow()}", ban_duration="{timestamp}" WHERE id={user.id} ''')
        con.commit()
        await ctx.send(embed=discord.Embed(description="⚠️ Updated user ban.", color=colours.blue))
    channel = await user.create_dm()
    await channel.send(embed=discord.Embed(description=f"""You've been banned from using bot by {ctx.message.author.mention}.
Reason: `{reason}`
Until: `{time}`""",color=colours.blue))
    con.commit()

@c_chck()
@bot.command()
@cooldown(1,_cooldown, BucketType.user)
async def banned(ctx):
    l_badwords = []
    for row in c.execute(f"SELECT id FROM users where banned='1'"): l_badwords.append(row[0])
    con.commit()
    _channel = await ctx.message.author.create_dm()
    message = ""
    for item in l_badwords:
        message = f"{message}, <@{item}>"
    await _channel.send(embed=discord.Embed(title="Banned list", description=f"{message[2:]}.", color=colours.blue))

@c_chck()
@c_achck()
@bot.command()
@cooldown(1,_cooldown, BucketType.user)
async def unban(ctx, *, user):
    user = await commands.UserConverter().convert(ctx, user)
    data = c.execute(f'SELECT * FROM users WHERE id={user.id}')
    con.commit()
    x = data.fetchone()
    if x == "None" or x == None:
        await ctx.send(embed=discord.Embed(description=f"⚠️ User is not banned.", color=colours.blue))
    else:
        c.execute(f'''UPDATE users SET banned="0" WHERE id={user.id} ''')
        con.commit()
        await ctx.send(embed=discord.Embed(description=f"⚠️ Unbanned user.", color=colours.blue))
    channel = await user.create_dm()
    await channel.send(embed=discord.Embed(description=f"""You've been unbanned from bot by {ctx.message.author.mention}.""",color=colours.blue))
    con.commit()

@c_chck()
@c_achck()
@bot.command()
@cooldown(1,_cooldown, BucketType.user)
async def op(ctx, *, user):
    user = await commands.UserConverter().convert(ctx, user)
    data = c.execute(f'SELECT * FROM users WHERE id={user.id}')
    con.commit()
    x = data.fetchone()
    if x == "None" or x == None:
        c.execute(f'''INSERT INTO users VALUES ("{int(user.id)}", "{str(user)}", "1", "0", "Null", "Null", "Null", "Null")''')
        con.commit()
        await ctx.send(embed=discord.Embed(description=f"⚠️ Added User to bot admins.", color=colours.blue))
    else:
        c.execute(f'''UPDATE users SET admin="1" WHERE id={user.id} ''')
        con.commit()
        await ctx.send(embed=discord.Embed(description=f"⚠️ Added user to bot admins.", color=colours.blue))
    con.commit()
@c_chck()
@bot.command()
@cooldown(1,_cooldown, BucketType.user)
async def ops(ctx):
    l_badwords = []
    for row in c.execute(f"SELECT id FROM users where admin='1'"): l_badwords.append(row[0])
    con.commit()
    _channel = await ctx.message.author.create_dm()
    message = ""
    for item in l_badwords:
        message = f"{message}, <@{item}>"
    await _channel.send(embed=discord.Embed(title="Ops list", description=f"{message[2:]}.", color=colours.blue))
@c_chck()
@c_achck()
@bot.command()
@cooldown(1,_cooldown, BucketType.user)
async def deop(ctx, *, user):
    user = await commands.UserConverter().convert(ctx, user)
    data = c.execute(f'SELECT * FROM users WHERE id={user.id}')
    con.commit()
    x = data.fetchone()
    if x == "None" or x == None:
        await ctx.send(embed=discord.Embed(description=f"⚠️ User is not op.", color=colours.blue))
    else:
        c.execute(f'''UPDATE users SET admin="0" WHERE id={user.id} ''')
        con.commit()
        await ctx.send(embed=discord.Embed(description=f"⚠️ Deoped user.", color=colours.blue))
    con.commit()
@c_chck()
@c_achck()
@bot.command()
@cooldown(1,_cooldown, BucketType.user)
async def badword(ctx, option, *, word=None):
    try: word = word.replace("\\", "\\\\").replace("\"", "\\\""); word = word.lower()
    except: pass
    if option.lower()=="list" and word==None:
        l_badwords = []
        for row in c.execute(f"SELECT word FROM badwords"): l_badwords.append(row[0])
        con.commit()
        _channel = await ctx.message.author.create_dm()
        message = ""
        for item in l_badwords:
            message = f"{message}, `{item}`"
        await _channel.send(embed=discord.Embed(title="Badwords list", description=f"{message[2:]}.", color=colours.blue))
    if option.lower()=="remove":
        data = c.execute(f'SELECT * FROM badwords WHERE word="{word}"')
        con.commit()
        x = data.fetchone()
        if x == None:
            await ctx.send(embed=discord.Embed(description="⚠️ Badword not exists.", color=colours.blue))
            return
        c.execute(f"""DELETE FROM badwords WHERE word="{word}" """)
        con.commit()
        await ctx.send(embed=discord.Embed(description=f"⚠️ Removed `{word}` from badwords.", color=colours.blue))
    elif option.lower()=="add":
        data = c.execute(f'SELECT * FROM badwords WHERE word="{word}"')
        con.commit()
        x = data.fetchone()
        if x != None:
            await ctx.send(embed=discord.Embed(description="⚠️ Badword already exists.", color=colours.blue))
            return
        c.execute(f"""INSERT INTO badwords VALUES ("{word}", "{str(ctx.message.author)}")""")
        con.commit()
        await ctx.send(embed=discord.Embed(description=f"⚠️ Added `{word}` to badwords.", color=colours.blue))
    else:
        support.cmd_help("badword", _prefix, len(bot.commands))
@c_chck()
@c_achck()
@bot.command()
@cooldown(1,_cooldown, BucketType.user)
async def channel(ctx, option, *, channel):
    channel = channel.replace("<#", "").replace(">", "")
    channel = bot.get_channel(int(channel))
    if option.lower()=="remove":
        data = c.execute(f'SELECT * FROM banned_channels WHERE id="{channel.id}"')
        con.commit()
        x = data.fetchone()
        if x == None:
            await ctx.send(embed=discord.Embed(description="⚠️ Channel not exists in database.", color=colours.blue), delete_after=10)
            return
        c.execute(f"""DELETE FROM banned_channels WHERE id="{channel.id}" """)
        con.commit()
        await ctx.send(embed=discord.Embed(description=f"⚠️ Removed `{channel}` from banned channels.", color=colours.blue))
    elif option.lower()=="add":
        data = c.execute(f'SELECT * FROM banned_channels WHERE id="{channel.id}"')
        con.commit()
        x = data.fetchone()
        if x != None:
            await ctx.send(embed=discord.Embed(description="⚠️ Channel already exists in database.", color=colours.blue), delete_after=10)
            return
        c.execute(f"""INSERT INTO banned_channels VALUES ("{channel.id}", "{channel}")""")
        con.commit()
        await ctx.send(embed=discord.Embed(description=f"⚠️ Added `{channel}` to banned channels.", color=colours.blue))
    else:
        support.cmd_help("channel", _prefix, len(bot.commands))
@c_chck()
@c_achck()
@bot.command()
@cooldown(1,_cooldown, BucketType.user)
async def cmd(ctx, option, *,command):
    if command.lower() not in bot.all_commands:
        await ctx.send(embed=discord.Embed(description=f"⚠️ Command `{command}` does not exist.", color=colours.blue), delete_after=10)
        return
    if option.lower() == "disable":
        data = c.execute(f'SELECT * FROM disabled_cmds WHERE command="{command}"')
        con.commit()
        x = data.fetchone()
        if x != None:
            await ctx.send(embed=discord.Embed(description="⚠️ Command is already disabled.", color=colours.blue), delete_after=10)
            return
        c.execute(f"""INSERT INTO disabled_cmds VALUES ("{command}") """)
        con.commit()
        await ctx.send(embed=discord.Embed(description=f"⚠️ Added `{command}` to disabled commands.", color=colours.blue))
    elif option.lower()=="enable":
        data = c.execute(f'SELECT * FROM disabled_cmds WHERE command="{command}"')
        con.commit()
        x = data.fetchone()
        if x == None:
            await ctx.send(embed=discord.Embed(description="⚠️ Command is not disabled.", color=colours.blue), delete_after=10)
            return
        c.execute(f"""DELETE FROM disabled_cmds WHERE command="{command}" """)
        con.commit()
        await ctx.send(embed=discord.Embed(description=f"⚠️ Removed `{command}` from disabled commands.", color=colours.blue))
    else:
        support.cmd_help("cmd", _prefix, len(bot.commands))
@c_chck()
@cooldown(1, _cooldown, BucketType.user)
@bot.command()
@cooldown(1,_cooldown, BucketType.user)
async def Tweet(ctx, *, Text):
    if len(ctx.message.attachments) == 0: tweet = api.update_status(status=Text)
    else:
        image_types = ["png", "jpeg", "gif", "jpg"]
        for attachment in ctx.message.attachments:
            for image in image_types:
                image = str(image)
                if attachment.filename.lower().endswith(image):
                    _attachment = f"attachment.{image}"
                    await attachment.save(f"tmp/{_attachment}")
                    tweet = api.update_with_media(f"tmp/{_attachment}", Text)
                    try: os.remove(f"tmp/{attachment}")
                    except: pass
    embed=discord.Embed(title="Tweeted", color=0x0091ff)
    embed.add_field(name="Text", value=f"{Text}", inline=False)
    embed.add_field(name="Link", value=f"https://twitter.com/i/web/status/{tweet.id_str}", inline=True)
    embed.set_footer(text=f"""Requester: {ctx.message.author} • Today at: {datetime.utcnow().strftime("%X")} UTC""")
    await ctx.send(embed=embed)
@c_chck()
@bot.command()
@cooldown(1,_cooldown, BucketType.user)
async def nick(ctx, *, name):
    await ctx.message.guild.me.edit(nick=name)
    await ctx.send(embed=discord.Embed(description="Done", color=colours.blue), delete_after=10)
@c_chck()
@bot.command()
@cooldown(1,_cooldown, BucketType.user)
async def iq(ctx, *,user: discord.User=None):
        iq_size = random.uniform(0.00, 200.00)
        if user == None: user = ctx.message.author
        if user.id==846298981797724161:
            iq_size = 200.00
        colour_hex = '%02x%02x%02x' % ( int((iq_size/2)*2.55), int((iq_size/2)*2.51), int((iq_size/2)*1.91) ); colour = int(colour_hex, 16)
        embed=discord.Embed(description=f"{user} IQ is {iq_size:.2f}.", color=colour)
        embed.set_footer(text=f"""Requester: {ctx.message.author} • Today at: {datetime.utcnow().strftime("%X")} UTC""")
        await ctx.send(embed=embed)
@c_chck()
@bot.command()
@cooldown(1,_cooldown, BucketType.user)
async def data(ctx, user="self"):
    channel = await ctx.message.author.create_dm()
    now=datetime.now()
    if user.lower()!="all":
        if user == "self": user=ctx.message.author
        else: user = await commands.UserConverter().convert(ctx, user)
        if user!=ctx.message.author and not admin_check_by_id(ctx.message.author.id): await ctx.send(embed=discord.Embed(description=config.get("no-perms"), color=colours.yellow), delete_after=10); print(f"{Back.LIGHTYELLOW_EX}{Fore.BLACK}[NO PERMS]{Style.RESET_ALL} {ctx.message.author} {Fore.LIGHTBLUE_EX}channel: {Fore.LIGHTGREEN_EX}{ctx.message.channel}{Style.RESET_ALL} {Fore.LIGHTBLUE_EX}guild: {Fore.LIGHTGREEN_EX}{ctx.message.guild}{Style.RESET_ALL}");return False
        data = c.execute(f'SELECT * FROM users WHERE id={user.id}')
        user_data = list(data.fetchone())
        try: time=datetime.fromtimestamp(int(round(float(user_data[7]))))
        except: time="Null"
        await channel.send(embed=discord.Embed(description=f"""
User id: `{user_data[0]}`
User Name: `{user_data[1]}`
Admin: `{user_data[2]}`
Banned: `{user_data[3]}`
Ban Reason: `{user_data[4]}`
Banned by: {user_data[5]}
Ban date: `{user_data[6]}`
Time to unban: `{time}`
""", color=colours.blue).set_footer(text=f"""Requester: {ctx.message.author} • Today at: {datetime.utcnow().strftime("%X")} UTC"""))
    elif user.lower()=="all" and admin_check_by_id(ctx.message.author.id):
        data = c.execute(f'SELECT * FROM users')
        user_data = list(data.fetchall())
        file = open(f"{path}/data/temp/data_all.txt", "w+")
        file.write("(UserID, Username, Admin, Banned, Ban Reason, Banned By, Banned Time)")
        for item in user_data:
            file.write("\n"+str(f"{item}".encode('utf8')))
        file.close()
        await channel.send(file=discord.File(f"{path}/data/temp/data_all.txt"))
@c_chck()
@bot.command()
@cooldown(1,_cooldown, BucketType.user)
async def dm(ctx, user, *,message):
    user = await commands.UserConverter().convert(ctx, user)
    channel = await user.create_dm()
    await channel.send(message)
    await ctx.send(embed=discord.Embed(description="Done", color=colours.blue), delete_after=10)
@c_chck()
@c_achck()
@bot.command()
@cooldown(1,_cooldown, BucketType.user)
async def logs(ctx):
    channel = await ctx.message.author.create_dm()
    await channel.send(file=discord.File(f"{path}/logs/{log_location}.log"))
@c_chck()
@bot.command()
@cooldown(1,_cooldown, BucketType.user)
async def quote(ctx):
    await ctx.send(embed=discord.Embed(description=f"{random.choice(quotes.prequel)}", color=colours.blue))
@c_chck()
@bot.command()
@cooldown(1,_cooldown, BucketType.user)
async def hello(ctx, there):
    if str(there).lower() == "there":
        await ctx.send("https://media.giphy.com/media/8JTFsZmnTR1Rs1JFVP/giphy.gif")
    else:
        await ctx.send(embed=discord.Embed(description=config.get("command-not-found"), color=colours.blue), delete_after=10)
@c_chck()
@bot.command()
@cooldown(1,_cooldown, BucketType.user)
async def current_prefix(ctx):
    channel = await ctx.message.author.create_dm()
    await channel.send(embed=discord.Embed(description=f"Current prefix is: `{_prefix}`", color=colours.blue))
@c_chck()
@bot.command()
@cooldown(1,_cooldown, BucketType.user)
async def gay(ctx, user=None):
    async with ctx.typing():
        image_types = ["png", "jpeg", "jpg"]
        if len(ctx.message.attachments) != 0:
            for attachment in ctx.message.attachments:
                if any(attachment.filename.lower().endswith(image) for image in image_types):
                    await attachment.save(f"{path}/data/temp/image.png")
        else:
            try: user = await commands.UserConverter().convert(ctx, user)
            except: user = ctx.message.author
            await user.avatar_url.save(f"{path}/data/temp/image.png")
        embed=discord.Embed(description="🏳️‍🌈", color=colours.blue)
        embed.set_image(url="attachment://result.png")
        await ctx.send(file=discord.File(processing.gay(f"{path}/data/temp/image.png")), embed=embed)
@c_chck()
@bot.command()
@cooldown(1,_cooldown, BucketType.user)
async def resize(ctx, y, x):
    async with ctx.typing():
        if int(y) > 6000 or int(x) > 6000 or int(x) <= 0 or int(y) <=0:
            raise ValueError("X or Y value is invalid. Max: 6000 Min: 1.")
        image_types = ["png", "jpeg", "jpg"]
        for attachment in ctx.message.attachments:
            if any(attachment.filename.lower().endswith(image) for image in image_types):
                await attachment.save(f"{path}/data/temp/image.png")
        embed=discord.Embed(description=f"Resized to: {y}x{x}", color=colours.blue)
        embed.set_image(url="attachment://result.png")
        await ctx.send(file=discord.File(processing.resize(f"{path}/data/temp/image.png", int(y), int(x))), embed=embed)
@c_chck()
@bot.command()
@cooldown(1,_cooldown, BucketType.user)
async def flashbacks(ctx, user=None):
    async with ctx.typing():
        image_types = ["png", "jpeg", "jpg"]
        if len(ctx.message.attachments) != 0:
            for attachment in ctx.message.attachments:
                if any(attachment.filename.lower().endswith(image) for image in image_types):
                    await attachment.save(f"{path}/data/temp/image.png")
        else:
            try: user = await commands.UserConverter().convert(ctx, user)
            except: user = ctx.message.author
            await user.avatar_url.save(f"{path}/data/temp/image.png")
        embed=discord.Embed(description="Flashbacks", color=colours.blue)
        embed.set_image(url="attachment://result.png")
        await ctx.send(file=discord.File(processing.war(f"{path}/data/temp/image.png")), embed=embed)
@c_chck()
@bot.command()
@cooldown(1,_cooldown, BucketType.user)
async def tts(ctx, *, text):
    text = text.replace("-l", "--language")
    text = text.split("--language")
    text.append("en")
    async with ctx.typing():
        await ctx.send(file=discord.File(processing.tts(f"{text[0]}", f"{text[1]}".replace(" ", ""))), content="Text To Speech")
@c_chck()
@c_achck()
@bot.command()
@cooldown(1,_cooldown, BucketType.user)
async def prefix(ctx, __prefix):
    global _prefix
    _prefix=__prefix
    bot.command_prefix=commands.when_mentioned_or(__prefix)
    await ctx.send(embed=discord.Embed(description="Done", color=colours.blue), delete_after=10)
@c_chck()
@c_achck()
@bot.command()
@cooldown(1,_cooldown, BucketType.user)
async def react(ctx):
    global b_react
    if b_react == True:
        b_react=False
    else:
        b_react=True
    await ctx.send(embed=discord.Embed(description="Done", color=colours.blue), delete_after=10)
@c_chck()
@bot.command()
@cooldown(1,_cooldown, BucketType.user)
async def mc_server(ctx, *, server):
    with urllib.request.urlopen(f'https://eu.mc-api.net/v3/server/ping/{server}') as response:
        data = json.loads(response.read())
        try: await ctx.send(embed=discord.Embed(description=f"""
Server: `{server}`
Description: `{data["description"]}`
Online: `{data["online"]}`
Version: `{data["version"]["name"]}`
Max Players: `{data["players"]["max"]}`
Players Online: `{data["players"]["online"]}`
""",color=colours.blue))
        except: await ctx.send(embed=discord.Embed(description=f"""Server not found.""", color=colours.blue), delete_after=10)

@c_chck()
@bot.command()
@cooldown(1,_cooldown, BucketType.user)
async def blacklisted(ctx, *, server):
    with urllib.request.urlopen(f'https://eu.mc-api.net/v3/server/blacklisted/{server}') as response:
        data = json.loads(response.read())
        await ctx.send(embed=discord.Embed(description=f"""
Server: `{data["query"]}`
Blacklisted: `{data["blacklisted"]}`
""",color=colours.blue))
@c_chck()
@bot.command()
@cooldown(1,_cooldown, BucketType.user)
async def info(ctx):
    await ctx.send(embed=discord.Embed(description=f"""
Info

Author: <@!846298981797724161> 
Github: https://github.com/m2rsho
`Currently not open source`

Commands: {len(bot.commands)}
Startup Date: {startup_time} UTC
""", color=colours.blue))
# Start
def init():
    print(f"""
┌───────────────────┐
│{Back.BLUE}{Fore.LIGHTGREEN_EX } Welcome!          {Style.RESET_ALL}│
│{Back.BLUE}{Fore.WHITE         } Version 1.0.6     {Style.RESET_ALL}│
│{Back.BLUE}{Fore.YELLOW        }                   {Style.RESET_ALL}│
│{Back.BLUE}{Fore.YELLOW        } Let's cum!        {Style.RESET_ALL}│
└───────────────────┘{Style.RESET_ALL}
Logs:
""")
    loop = asyncio.get_event_loop()
    loop.create_task(bot.start(config.get("bot-token"), bot=config.get("bot-application-account")))
    loop.run_forever()
init()
