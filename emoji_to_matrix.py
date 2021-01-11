"""
Turns a message into a matrix
0-8 = normal numbers
9 = unknown
10 = bomb

example:
⬛ 🇦 🇧 🇨 🇩 🇪 🇫 🇬
1⃣ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜
2⃣ ⬜ <:bombs3:505716226354446338> <:bombs1:505716219714732047> <:bombs1:505716219714732047> ⬜ ⬜ ⬜
3⃣ ⬜ <:bombs2:505716222373920779> <:bombs0:505716180540194841> <:bombs1:505716219714732047> ⬜ ⬜ ⬜
4⃣ ⬜ <:bombs2:505716222373920779> <:bombs0:505716180540194841> <:bombs2:505716222373920779> ⬜ ⬜ ⬜
5⃣ ⬜ <:bombs1:505716219714732047> <:bombs1:505716219714732047> <:bombs3:505716226354446338> ⬜ ⬜ ⬜
6⃣ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ ⬜
"""
header_message = "**Minesweeper:**\nSend the coordinate of where you want to dig (e.g. c4) to reveal how many bombs are surrounding that tile.\nDon't dig up any bombs! You can flag bombs by adding a capital F after your coordinate (e.g. c4F)\n"
rematch_message = "🔄 Rematch"
game_header = "⬛ 🇦 🇧 🇨 🇩 🇪 🇫 🇬"

def emoji_to_matrix(message):
    content = message.content
    # checks to make sure the game header is in the message and it's not the rematch message
    if not game_header in content or rematch_message in content:
        return None

    # removes text from message if necessary
    if header_message in content:
        content = content.replace(header_message, "")

    # removes extraneous emojis
    content = content.replace(game_header, "")
    for character in ["1⃣ ", "2⃣ ", "3⃣ ", "4⃣ ", "5⃣ ", "6⃣ "]:
        content = content.replace(character, "")

    #creates a matrix by line
    result = []
    for i in content.strip().splitlines():
        line = []
        for j in i.strip().split(" "):
            line.append(emoji_to_number(j))

        result.append(line)

    # returns the result
    return result

def emoji_to_number(emoji):
    if emoji == "⬜":
        return 9
    elif emoji == "🚩":
        return 9
    elif ":bombs" in emoji:
        return int(emoji[emoji.index(":bombs")+6:emoji.index(":bombs")+7])