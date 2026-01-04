import discord
from discord import app_commands
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

GUILD_ID = 1457316487134973995

class AuraClient(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        guild = discord.Object(id=GUILD_ID)
        self.tree.copy_global_to(guild=guild)
        await self.tree.sync(guild=guild)
        print("Slash commands synced to guild")

client = AuraClient()

@client.event
async def on_ready():
    print(f"Aura Bot ready as {client.user}")

@client.tree.command(name="ask", description="Ask Aura a question")
@app_commands.describe(question="Your question for Aura")
async def ask(interaction: discord.Interaction, question: str):
    await interaction.response.defer(thinking=True)

    async with httpx.AsyncClient(timeout=httpx.Timeout(90.0)) as http:
        res = await http.post(
            f"{API_URL}/api/chat",
            json={
                "prompt": question,
                "user_id": str(interaction.user.id)
            }
        )

    await interaction.followup.send(res.json()["response"])

client.run(DISCORD_TOKEN)
