from discord import Embed
def replace_all(text, dic):
    for i, j in dic.items():
        text = text.replace(i, j)
    return text
def cmd_help(cmd, prefix, commands_l):
    thestuff = {
    "tell" and "sudo": "say", 
    "mc_alt" and "mcalt": "alt",
    "r" and "meter": "rate",
    "dick" and "penis" and "cock": "pp",
    "cf": "coinflip",
    "video" and "youtube": "yt",
    "ascii": "ascii",
    "font": "font",
    "hex": "hex",
    "math" and "cal" and "calculate": "calc",
    "ban": "ban",
    "unban": "unban",
    "op": "op",
    "deop": "deop",
    "badword": "badword"
    }
    r_cmd = replace_all(cmd, thestuff)

    commands = {
"Template": Embed(title=f"{prefix}{cmd} • Help", description=f"""Description""", color=0x2e66ff),

"list": Embed(title="Command List.", description=f"""
`{prefix}help <Command>         => Help about command.        `
`{prefix}help admin             => Admin commands help.       `
`{prefix}info                   => Info.                      `

`{prefix}say <Text>             => Says anything.             `
`{prefix}edited <Text>          => Sends message and edits it.`
`{prefix}alt                    => Gives you free alt.        `
`{prefix}rate <Thing>           => Rates things.              `
`{prefix}pp <User>              => Measures pp.               `
`{prefix}iq <User>              => Measures iq.               `
`{prefix}coinflip               => CoinFlip.                  `
`{prefix}yt <Stuff>             => Searches youtube.          `
`{prefix}ascii <Text>           => Text to ascii art.         `
`{prefix}font <PyFigletFont>    => Changes ascii font.        `
`{prefix}hex <Hex>              => Previews hex colour.       `
`{prefix}calc <Stuff>           => Calculates thing.          `
`{prefix}tweet <Stuff>          => Tweets stuff.              `
`{prefix}nick <Stuff>           => Changes bot nickname.      `
`{prefix}banned                 => List of banned people.     `
`{prefix}ops                    => List of bot admins.        `
`{prefix}dm <Stuff>             => Dms any user.              `
`{prefix}quote                  => Random prequel quote.      `
`{prefix}current_prefix         => Shows current prefix.      `
`{prefix}gay                    => Overlays pride flag.       `
`{prefix}flashbacks             => Overlays Helicopters.      `
`{prefix}resize                 => Resizes attachment.        `
`{prefix}tts                    => Text to Speech.            `
Commands: {commands_l}.
""", color=0xfff94d),

"admin": Embed(title=f"Admin Commands.", description=f"""
Admin Commands:
`{prefix}ban <User>             => Bans user from using bot.  `
`{prefix}unban <User>           => Unbans user.               `
`{prefix}op <User>              => Gives user op.             `
`{prefix}deop <User>            => Deops user.                `
`{prefix}badword <Options>      => Manages badwords.          `
`{prefix}channel <Options>      => Manages channel bans.      `
`{prefix}cmd <Options>          => Manages commands.          `
`{prefix}data <Options>         => Shows user data.           `
`{prefix}logs                   => Shows Logs.                `
`{prefix}prefix                 => Changes bot prefix.        `
`{prefix}react                  => Reacts to every command.   `""", color=0xfff94d),

"say": Embed(title=f"{prefix}{cmd} • Help", description=f"""
Says anything using bot account.

Usage:
    `{prefix}{cmd} <Text>`
Example:
    `{prefix}{cmd} i like cum`

Aliases: `say`, `sudo`, `tell`.""", color=0x2e66ff),

"alt": Embed(title=f"{prefix}{cmd} • Help", description=f"""
Gives you random minecraft alt.

Usage:
    `{prefix}{cmd}`

Aliases: `alt`, `mcalt`, `mc_alt`.""", color=0x2e66ff),

"rate": Embed(title=f"{prefix}{cmd} • Help", description=f"""
Rates anything

Usage:
    `{prefix}{cmd} <Optional: @Mention or @$Thing> <Something Else>`
Example:
    `{prefix}{cmd} @mariyt gay`
    `{prefix}{cmd} "@$Your Mom" Gay`
    `{prefix}{cmd} gay`

Aliases: `rate`, `r`, `meter`.""", color=0x2e66ff),

"pp": Embed(title=f"{prefix}{cmd} • Help", description=f"""
Measures pp

Usage:
    `{prefix}{cmd} <Optional: @Mention>`
Example:
    `{prefix}{cmd} @mariyt`
    `{prefix}{cmd}`

Aliases: `pp`, `dick`, `penis`, `cock`.""", color=0x2e66ff),

"coinflip": Embed(title=f"{prefix}{cmd} • Help", description=f"""
Coinflip

Usage:
    `{prefix}{cmd}`

Aliases: `cf`, `coinflip`.""", color=0x2e66ff),

"yt": Embed(title=f"{prefix}{cmd} • Help", description=f"""
Searches YouTube and finds video

Usage:
    `{prefix}{cmd} <Search Stuff>`

Aliases: `yt`, `video`, `youtube`.""", color=0x2e66ff),

"ascii": Embed(title=f"{prefix}{cmd} • Help", description=f"""
Text to Ascii text

Usage:
    `{prefix}{cmd} <Text>`

Aliases: `ascii`.""", color=0x2e66ff),

"font": Embed(title=f"{prefix}{cmd} • Help", description=f"""
Changes Ascii Font
Font List: http://www.figlet.org/fontdb.cgi

Usage:
    `{prefix}{cmd} <Font>`
Example:
    `{prefix}{cmd} usaflag`

Aliases: `font`.""", color=0x2e66ff),

"hex": Embed(title=f"{prefix}{cmd} • Help", description=f"""
Previews hex colour

Usage:
    `{prefix}{cmd} <Colour if none outputs random colour>`
Example:
    `{prefix}{cmd} #b00b5`
    `{prefix}{cmd}`

Aliases: `hex`.""", color=0x2e66ff),

"calc": Embed(title=f"{prefix}{cmd} • Help", description=f"""
Calculates Things.

Usage:
    `{prefix}{cmd} <Some Stuff>`
Example:
    `{prefix}{cmd} 2+2`

Aliases: `calc`, `cal`, `math`, `calculate`.""", color=0x2e66ff),

"ban": Embed(title=f"{prefix}{cmd} • Help", description=f"""
Bans user from using bot

Usage:
    `{prefix}{cmd} <User>`
Example:
    `{prefix}{cmd} @Your Mom`

Requires: `Admin Permissions`.
Aliases: `ban`.""", color=0x2e66ff),

"unban": Embed(title=f"{prefix}{cmd} • Help", description=f"""
Unbans user from using bot

Usage:
    `{prefix}{cmd} <User>`
Example:
    `{prefix}{cmd} @Your Mom`

Requires: `Admin Permissions`.
Aliases: `unban`.""", color=0x2e66ff),

"op": Embed(title=f"{prefix}{cmd} • Help", description=f"""
Adds user to bot admins.

Usage:
    `{prefix}{cmd} <User>`
Example:
    `{prefix}{cmd} @Your Mom`

Requires: `Admin Permissions`.
Aliases: `op`.""", color=0x2e66ff),

"deop": Embed(title=f"{prefix}{cmd} • Help", description=f"""
Removes user from bot admins.

Usage:
    `{prefix}{cmd} <User>`
Example:
    `{prefix}{cmd} @Your Mom`

Requires: `Admin Permissions`.
Aliases: `deop`.""", color=0x2e66ff),

"badword": Embed(title=f"{prefix}{cmd} • Help", description=f"""
List of words that bot removes/reacts with angry face.
Or cancels command.

Usage:
    `{prefix}{cmd} <Add/Remove> <word>`
Example:
    `{prefix}{cmd} Add I hate cum`
    `{prefix}{cmd} remove I love cum`

Requires: `Admin Permissions`.
Aliases: `badword`.""", color=0x2e66ff),

"channel": Embed(title=f"{prefix}{cmd} • Help", description=f"""
Removes/Adds channel to banned channels. (Bot does not work there)

Usage:
    `{prefix}{cmd} <Add/Remove> <channel>`
Example:
    `{prefix}{cmd} Add #general`
    `{prefix}{cmd} remove #memes`

Requires: `Admin Permissions`.
Aliases: `channel`.""", color=0x2e66ff),

"edited": Embed(title=f"{prefix}{cmd} • Help", description=f"""
Edits message after some time.

Usage:
    `{prefix}{cmd} "<Text Before Edit>" "<Text After Edit>" <Time>`
Example:
    `{prefix}{cmd} "Fuck me in the ass" "fuck me in the ass daddy uwu" 10`

Aliases: `edited`.""", color=0x2e66ff),

"banned": Embed(title=f"{prefix}{cmd} • Help", description=f"""
List of banned people.

Usage:
    `{prefix}{cmd}`

Aliases: `banned`.""", color=0x2e66ff),

"ops": Embed(title=f"{prefix}{cmd} • Help", description=f"""
List of bot admins.

Usage:
    `{prefix}{cmd}`

Aliases: `ops`.""", color=0x2e66ff),

"cmd": Embed(title=f"{prefix}{cmd} • Help", description=f"""
Enables/Disables commands

Usage:
    `{prefix}{cmd} <disable/enable> <command>`
Example:
    `{prefix}{cmd} disable help`

Requires: `Admin Permissions`.
Aliases: `cmd`.""", color=0x2e66ff),

"nick": Embed(title=f"{prefix}{cmd} • Help", description=f"""
Changes Bot Nickname.

Usage:
    `{prefix}{cmd} <nick>`
Example:
    `{prefix}{cmd} Stupid Retard`

Aliases: `nick`.""", color=0x2e66ff),

"data": Embed(title=f"{prefix}{cmd} • Help", description=f"""
Shows user data.

Usage:
    `{prefix}{cmd} <user>`
Example:
    `{prefix}{cmd} @mariyt`
    `{prefix}{cmd} all`

Requires: `Admin Permissions` **FOR other users**.
Aliases: `data`.""", color=0x2e66ff),

"dm": Embed(title=f"{prefix}{cmd} • Help", description=f"""
Dms any user.

Usage:
    `{prefix}{cmd} <user> <stuff>`
Example:
    `{prefix}{cmd} @mariyt cum`

Aliases: `dm`.""", color=0x2e66ff),

"logs": Embed(title=f"{prefix}{cmd} • Help", description=f"""
Shows commands logs.

Usage:
    `{prefix}{cmd}`

Requires: `Admin Permissions`.
Aliases: `logs`.""", color=0x2e66ff),

"quote": Embed(title=f"{prefix}{cmd} • Help", description=f"""
Random prequel quote lol.

Usage:
    `{prefix}{cmd}`

Aliases: `quote`.""", color=0x2e66ff),

"current_prefix": Embed(title=f"{prefix}{cmd} • Help", description=f"""
Shows current prefix

Usage:
    `{prefix}{cmd}`

Aliases: `current_prefix`.""", color=0x2e66ff),

"gay": Embed(title=f"{prefix}{cmd} • Help", description=f"""
Overlays pride flag.
May be used with attachments or user avatar.

Usage:
    `{prefix}{cmd} <user or none if with attachment>`
Example:
    `{prefix}{cmd} @mariyt`

Aliases: `gay`.""", color=0x2e66ff),

"flashbacks": Embed(title=f"{prefix}{cmd} • Help", description=f"""
Overlays helicopters.
May be used with attachments or user avatar.

Usage:
    `{prefix}{cmd} <user or none if with attachment>`
Example:
    `{prefix}{cmd} @mariyt`

Aliases: `flashbacks`.""", color=0x2e66ff),

"flashbacks": Embed(title=f"{prefix}{cmd} • Help", description=f"""
Overlays helicopters.
May be used with attachments or user avatar.

Usage:
    `{prefix}{cmd} <user or none if with attachment>`
Example:
    `{prefix}{cmd} @mariyt`

Aliases: `flashbacks`.""", color=0x2e66ff),

"resize": Embed(title=f"{prefix}{cmd} • Help", description=f"""
Resizes attachment.

Usage:
    `{prefix}{cmd} <x> <y>`
Example:
    `{prefix}{cmd} 69 420`

Aliases: `resize`.""", color=0x2e66ff),

"tts": Embed(title=f"{prefix}{cmd} • Help", description=f"""
Text to speech

Usage:
    `{prefix}{cmd} <Text> <OPTIONAL: -l or --language to change language>`
Example:
    `{prefix}{cmd} Cum`
    `{prefix}{cmd} Jebać Bydgoszcz -l pl`

Aliases: `tts`.""", color=0x2e66ff),

"prefix": Embed(title=f"{prefix}{cmd} • Help", description=f"""
Changes bot prefix.

Usage:
    `{prefix}{cmd} <prefix>`
Example:
    `{prefix}{cmd} cum`

Requires: `Admin Permissions`.
Aliases: `prefix`.""", color=0x2e66ff),

"react": Embed(title=f"{prefix}{cmd} • Help", description=f"""
Reacts to every command with: ✅.
Toggle

Usage:
    `{prefix}{cmd}`

Requires: `Admin Permissions`.
Aliases: `react`.""", color=0x2e66ff),
}
    return commands.get(r_cmd.lower(), Embed(title=f"Command '`{cmd}`' not found.", color=0xfff94d))