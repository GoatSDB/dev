import os
import discord
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
POE_API_KEY = os.getenv("POE_API_KEY")
POE_API_URL = os.getenv("POE_API_URL")
SYSTEM_PROMPT = os.getenv("AI_PERSONALITY")

# Discord client setup
intents = discord.Intents.default()
intents.messages = True
client = discord.Client(intents=intents)

def get_ai_response(user_prompt):
    """
    Send prompt to Poe API with a fixed system prompt (personality)
    """
    headers = {
        "Authorization": f"Bearer {POE_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "GPT-4o",  # Poe-supported model
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},  # Fixed personality
            {"role": "user", "content": user_prompt}       # User message
        ]
    }

    try:
        response = requests.post(
            f"{POE_API_URL}/chat/completions",
            json=data,
            headers=headers,
            timeout=30
        )
        if response.status_code == 200:
            result = response.json()
            ai_reply = result.get("choices")[0].get("message").get("content")
            return ai_reply
        else:
            return f"Error: API returned status code {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"

@client.event
async def on_ready():
    print(f"{client.user} has connected to Discord!")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("!ai"):
        prompt = message.content[len("!ai "):].strip()
        if not prompt:
            await message.channel.send("Please provide a message after !ai")
            return

        reply = get_ai_response(prompt)
        await message.channel.send(reply)

# Run Discord bot
client.run(DISCORD_TOKEN)