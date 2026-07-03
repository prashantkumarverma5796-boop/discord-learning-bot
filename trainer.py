from database import save_pair


async def train_channel(channel):
    learned = 0
    previous = None

    async for msg in channel.history(limit=None, oldest_first=True):
        if msg.author.bot:
            continue

        if previous and previous.author != msg.author:
            save_pair(previous.content, msg.content)
            learned += 1

        previous = msg

    return learned


async def train_server(guild):
    total = 0

    for channel in guild.text_channels:
        try:
            total += await train_channel(channel)
        except Exception:
            pass

    return total