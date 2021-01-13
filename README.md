# Minesweeper Sweeper
Solves GamesROB's minesweeper because I can't beat it without a robot myself
 
Are you fed up with GamesROB's minesweeper? So am I. If you have this bot it'll do everything for you. To activate and 
deactivate the bot, simply ping it. If it's not really doing anything for some reason, or you activate it while a 
minesweeper game is running, ping it and say "do something", like this:

`@Minesweeper do something`\
or whatever your bot's name is instead of "Minesweeper"

That being said, minesweeper is inherently chance based so there's some chance you'll fail.

Requires discord.py and python to run (obviously), as well as a discord bot\
To get the discord.py, check out the [discord.py github page](https://github.com/Rapptz/discord.py) \
As for your token, you can either replace the `open("token.txt", "r").read()` stuff with just a string of your 
token or drop in a new text file called "token.txt" that contains your token. You'll also have to replace `name` with \
the ID of your bot which you can get by left clicking on their name in developer mode or just by copying client ID in 
the developer portal.

This bot simulates every possible configuration of bombs to get perfectly accurate probabilities, but it's not the most 
efficient method. For better methods, check out [this paper](https://dash.harvard.edu/bitstream/handle/1/14398552/BECERRA-SENIORTHESIS-2015.pdf?sequence=1) 
which I don't understand at all so I just did an insanely time-consuming version.

If you want my bot on your server for some reason, which will basically be offline 99% of the time,
[this is the link](https://discord.com/api/oauth2/authorize?client_id=797850288543367199&permissions=0&scope=bot). But 
seriously, if you want to use this for some reason, you most likely don't want the bot I run. You should probably host 
it yourself.