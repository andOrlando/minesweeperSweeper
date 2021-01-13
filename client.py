import discord
from emoji_to_matrix import emoji_to_matrix
from matrix_solver import MatrixSolver

async def run_main_thing(message, last_response, debug):
    # pass message to emoji_to_matrix
    matrix = emoji_to_matrix(message)
    if matrix == "rematch": return None

    # pass the new emoji_to_matrix to minesweeper_solver
    move = MatrixSolver(matrix, debug=debug).get_command()
    # send the result in the channel
    if not move is None and last_response != move:
        await message.channel.send(move)
        return move

class MyClient(discord.Client):

    def __init__(self, name, debug = False, **options):
        super().__init__(**options)
        self.running = False
        self.debug = debug
        self.name = f"<@!{name}>"
        self.last_response = ""

    async def on_ready(self):
        print(f"bot ready as {self.user}")

    async def on_message(self, message):
        # when pinged activates or deactivates
        if message.content.lower() == self.name:
            await message.channel.send(f"bot {'activated' if not self.running else 'de-activated'}")
            self.running = not self.running

        # if pinged and it says "do something" check through channel history to do something
        elif message.content.lower() == f"{self.name} do something" and self.running:
            async for i in message.channel.history(limit=200):
                if i.author.id == 383995098754711555:
                    await run_main_thing(i, self.last_response, self.debug)
                    break

        # if it's activated and GamesROB does something, runs the main thing
        elif message.author.id == 383995098754711555 and self.running:
            self.last_response = await run_main_thing(message, self.last_response, self.debug)

    # if GamesROB edits a message it runs the main thing
    async def on_message_edit(self, _, after):
        # checks that it's GamesROB and it's running
        if after.author.id == 383995098754711555 and self.running:
            self.last_response = await run_main_thing(after, self.last_response, self.debug)




