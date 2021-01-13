import discord
from emoji_to_matrix import emoji_to_matrix
from matrix_solver import MatrixSolver

async def run_main_thing(message, last_response, debug):
    # pass message to emoji_to_matrix
    matrix = emoji_to_matrix(message)
    if matrix == "rematch":
        return None

    # pass the new emoji_to_matrix to minesweeper_solver
    move = MatrixSolver(matrix).get_command() if not matrix is None else None
    # send the result in the channel
    if not move is None and last_response != move:
        await message.channel.send(move)
        return move

class MyClient(discord.Client):

    def __init__(self, debug = False, **options):
        super().__init__(**options)
        self.running = False
        self.debug = debug
        self.last_response = ""

    async def on_ready(self):
        print(f"bot ready as {self.user}")

    async def on_message(self, message):
        if message.content.lower() == "gamesrob's minesweeper sucks":
            await message.channel.send("I totally agree so I'll just do it for you lol\nJust repeat whatever tiles I say")
            self.running = True
        elif message.content.lower() == "nvm its not actually that bad":
            await message.channel.send("well you're wrong; I'm not helping you anymore. Hmph.")
            self.running = False
        elif message.content.lower() == "do something" and self.running:
            async for i in message.channel.history(limit=200):
                if message.author.id == 383995098754711555:
                    await run_main_thing(i, self.last_response, self.debug)
                    break
        elif message.author.id == 383995098754711555 and self.running:
            self.last_response = await run_main_thing(message, self.last_response, self.debug)

    async def on_message_edit(self, _, after):
        # GamesROB's ID
        if after.author.id == 383995098754711555 and self.running:
            self.last_response = await run_main_thing(after, self.last_response)




