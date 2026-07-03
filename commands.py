from trainer import train_server


async def handle_command(message):
    if message.content == "!train":
        await message.channel.send("📚 Training...")

        learned = await train_server(message.guild)

        await message.channel.send(
            f"✅ Learned {learned} conversation pairs."
        )

        return True

    return False