import os
import re

from telethon import TelegramClient, events

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION_NAME = os.getenv("SESSION_NAME", "boss_session")
DESTINATION = os.getenv("DESTINATION")

client = TelegramClient(
    SESSION_NAME,
    API_ID,
    API_HASH,
    sequential_updates=False
)

SOURCE_CHANNELS = [
    "@gauwv819",
    "@bossrummy"
]

# Sirf 500-cashcode-xxxxx pakdega
CODE_REGEX = re.compile(
    r"\b500-cashcode-\d+\b",
    re.IGNORECASE
)


def extract_code(text: str):
    if not text:
        return None

    # Mono formatting remove
    text = text.replace("`", "")

    match = CODE_REGEX.search(text)

    if match:
        return match.group(0)

    return None


@client.on(events.NewMessage(chats=SOURCE_CHANNELS))
async def handle_message(event):
    try:
        text = event.raw_text or ""

        code = extract_code(text)

        if not code:
            return

        message = (
            f"`{code}`\n"
            f"`{code}`\n"
            f"`{code}`\n"
            f"`{code}`"
        )

        await client.send_message(
            DESTINATION,
            message,
            parse_mode="md"
        )

        print(f"FORWARDED: {code}")

    except Exception as e:
        print(f"ERROR: {e}")


async def main():
    me = await client.get_me()
    print(f"Logged in as: {me.first_name}")
    print("Ultra Fast Forwarder Started...")
    await client.run_until_disconnected()


with client:
    client.loop.run_until_complete(main())