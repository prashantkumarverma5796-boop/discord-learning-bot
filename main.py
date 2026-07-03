import os
import discord
from dotenv import load_dotenv
from database import save_pair
from responder import respond
from commands import handle_command
from reactions import save_reaction

load_dotenv()

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.reactions = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user}")


@client.event
async def on_raw_reaction_add(payload):
    if payload.user_id == client.user.id:
        return

    channel = client.get_channel(payload.channel_id)

    if channel is None:
        channel = await client.fetch_channel(payload.channel_id)

    message = await channel.fetch_message(payload.message_id)

    save_reaction(message.content, str(payload.emoji))


@client.event
async def on_message(message):
    if message.author.bot:
        return

    if await handle_command(message):
        return

    if (
        message.content.startswith(("!", "/", ".", "?"))
        or len(message.content.strip()) < 3
    ):
        return

    if message.reference:
        try:
            original = await message.channel.fetch_message(
                message.reference.message_id
            )

            if (
                not original.author.bot
                and original.author.id != message.author.id
            ):
                save_pair(original.content, message.content)

        except Exception:
            pass

    await respond(message)


client.run(TOKEN)