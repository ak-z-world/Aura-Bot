import discord
from discord import app_commands
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

GUILD_ID = 1457316487134973995


def split_message(text, limit=2000):
    return [text[i:i+limit] for i in range(0, len(text), limit)]


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

    try:
        async with httpx.AsyncClient(timeout=httpx.Timeout(20.0)) as http:
            res = await http.post(
                f"{API_URL}/api/chat",
                json={
                    "prompt": question,
                    "user_id": str(interaction.user.id)
                }
            )

        if res.status_code != 200:
            try:
                await interaction.followup.send(
                    "Aura backend returned an error."
                )
            except discord.errors.NotFound:
                pass
            return

        try:
            data = res.json()
        except Exception:
            try:
                await interaction.followup.send(
                    "Aura backend returned invalid data."
                )
            except discord.errors.NotFound:
                pass
            return

        response_text = data.get("response")
        if not response_text:
            try:
                await interaction.followup.send(
                    "Aura backend response was empty."
                )
            except discord.errors.NotFound:
                pass
            return

        try:
            await interaction.followup.send("**Aura response:**")
            for part in split_message(response_text):
                await interaction.followup.send(part)
        except discord.errors.NotFound:
            pass

    except Exception as e:
        print(f"Discord /ask error (interaction expired): {e}")
        # DO NOT respond here — interaction is gone

@client.tree.command(name="contact", description="Contact the developer of Aura")
async def contact(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Aura — AI Systems & Automation",
        description=(
            "Aura is a live AI systems and automation demo.\n\n"
            "We build and support:\n"
            "• Custom AI & social-media bots (Discord, WhatsApp, etc.)\n"
            "• AI-powered chatbots and assistants\n"
            "• Workflow & process automation\n"
            "• Backend systems and API development\n\n"
            "Open to collaborations, projects, and custom development."
        ),
        color=0x5865F2
    )

    embed.add_field(
        name="Primary Contact",
        value="• Discord DM: **@akzworld**",
        inline=False
    )

    embed.add_field(
        name="Professional",
        value="• Email: **sivaarun10@gmail.com**",
        inline=False
    )

    embed.set_footer(
        text="Live cloud demo • Custom solutions available on request"
    )

    await interaction.response.send_message(embed=embed, ephemeral=True)

@client.tree.command(name="about", description="About Aura")
async def about(interaction: discord.Interaction):
    await interaction.response.send_message(
        "Aura — AI Systems & Research Initiative\n\n"
        "Aura was founded and built by Arun Kumar.\n\n"
        "Aura is not just a Discord bot. It is a growing initiative focused on designing,"
        "building, and demonstrating intelligent AI systems, automation tools, and"
        "real-world applications using modern AI technologies.\n\n"
        "Alongside applied development, Aura has begun early-stage exploratory research"
        "into quantum-inspired concepts for language models. This research is conceptual"
        "in nature and runs entirely on classical computing infrastructure.\n\n"
        "Through Aura, we work on:\n"
        "• Custom AI & social-media bots\n"
        "• AI-driven automation systems\n"
        "• Backend & API engineering\n"
        "• Research-oriented AI experimentation\n\n"
        "This bot serves as a live demonstration of Aura’s applied engineering work.",
        ephemeral=True
    )

client.run(DISCORD_TOKEN)

