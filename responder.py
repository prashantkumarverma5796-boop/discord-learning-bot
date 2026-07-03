import random
from semantic import find_best_reply
from reactions import get_reaction
from config import REPLY_CHANCE, PERSONALITY


async def respond(message):
    # React using learned emoji
    emoji = get_reaction(message.content)

    if emoji:
        try:
            # Unicode emoji
            await message.add_reaction(emoji)

        except Exception:
            # Custom server emoji
            try:
                if ":" in emoji:
                    emoji_name = emoji.split(":")[1]

                    for e in message.guild.emojis:
                        if e.name == emoji_name:
                            await message.add_reaction(e)
                            break
            except Exception:
                pass

    # Random text reply
    if random.randint(1, 100) > REPLY_CHANCE:
        return

    reply = find_best_reply(message.content)

    if not reply:
        return

    if reply.lower() == message.content.lower():
        return

    if PERSONALITY == "funny":
        reply += random.choice([" 😂", " 😭", " 💀", "", " lol", " fr"])

    elif PERSONALITY == "wholesome":
        reply += random.choice([" ❤️", " 😊", " ✨", " 🙌", ""])

    elif PERSONALITY == "sarcastic":
        reply += random.choice([" 🙄", " sure...", " obviously", " 💀", ""])

    await message.channel.send(reply)