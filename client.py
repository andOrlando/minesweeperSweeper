import discord
from emoji_to_matrix import emoji_to_matrix
from matrix_solver import MatrixSolver

'''
HOW ITS GOING TO WORK
-you start the minesweeper game
-you type fuck minesweeper
-bot looks for active minesweeper game
-bot tells you what to do, waits for you to do something, then tells you what to do next every time the thing edits it
'''


def is_rob(author):
    return author.id == 383995098754711555

class MyClient(discord.Client):

    def __init__(self, **options):
        super().__init__(**options)
        self.running = False

    async def on_ready(self):
        print("bot ready as {}".format(self.user))

    async def on_message(self, message):
        if message.content.lower() == "gamesrob's minesweeper sucks":
            message.channel.send("I totally agree so I'll just do it for you lol")
            self.running = True
        elif message.content.lower() == "nvm its not actually that bad":
            message.channel.send("well you're wrong; I'm not helping you anymore. Hmph.")
            self.running = False

    async def on_message_edit(self, _, after):
        if is_rob(after.author) and self.running:
            #pass message to emoji_to_matrix
            matrix = emoji_to_matrix(after)
            if matrix == "rematch":
                return None

            #pass the new emoji_to_matrix to minesweeper_solver
            move = MatrixSolver(matrix).get_command() if not matrix is None else None
            #send the result in the channel
            if not move is None:
                await after.channel.send(move)
            else:
                await after.channel.send("couldn't find a move")



