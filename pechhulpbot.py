import os
import discord
from discord import app_commands
from discord.ext import commands

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Your Discord ID encoded in HEX format (Replace this string with your real Hex ID)
OWNER_HEX_ID = "a17a27284c00083"  

def verify_owner_id() -> int:
    """Decodes the Hex string back to integer ID. 
    If modified or broken, it returns None to stop the bot."""
    try:
        # Convert hex string back to integer ID
        return int(OWNER_HEX_ID, 16)
    except Exception:
        return None

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    try:
        synced = await bot.tree.sync()
        print(f"Successfully synced {len(synced)} command(s) globally!")
    except Exception as e:
        print(e)

def get_job_title(num: int) -> str:
    """Determines the job title based on the input number range."""
    if num == 0:
        return "Pechhulp Coordinator"
    elif 1 <= num <= 3:
        return "Directeur"
    elif 4 <= num <= 9:
        return "Chef Werkplaats"
    elif 10 <= num <= 23:
        return "Technisch Specialist"
    elif 24 <= num <= 34:
        return "Autotechnicus"
    elif 35 <= num <= 54:
        return "Hoofd Monteur"
    elif 55 <= num <= 74:
        return "Ervaren Monteur"
    elif 75 <= num <= 94:
        return "Monteur"
    elif 95 <= num <= 134:
        return "Beginnend Monteur"
    elif 135 <= num <= 185:
        return "Stagiair"
    else:
        return "Onbekend Nummer"
#HUZ4dd7PnCyuhbLHS+M9kojfRS0sM58egfCLKrAwVe2YuXGC74vr9Y7Vjc30q2QJFmgkbR6HPPoO1Ci7bRAkpvT/IT0IwGTV2Qlq5H7nsASrEBc+kduEvBNwFWHGf2p8FLVQctXWaQittcf7MpLUZV/OL6pTcrMzI/8IqVraN6Q=
@bot.tree.command(name="binds", description="Generate radio and action binds for a user.")
@app_commands.describe(nummer="The ID number (e.g., 00, 6, 15)", naam="The player name (e.g., Frederik.K)")
async def binds(interaction: discord.Interaction, nummer: int, naam: str):
    # 1. Read and decode the Hex ID
    owner_id = verify_owner_id()
    
    # 2. Hard Stop: If the hex code was removed, broken, or unreadable, the command dies silently
    if not owner_id:
        return

    # Instructs Discord to expect hidden responses
    await interaction.response.defer(ephemeral=True)
    
    # Format the number (e.g., 6 becomes "06", 0 becomes "00")
    formatted_num = f"{nummer:02d}"
    title = get_job_title(nummer)
    
    # Message 1: The active binds
    bind_output = f"""```text
bind keyboard "1" "nameinradio [A-{formatted_num}] {naam} (S1)";
bind keyboard "2" "nameinradio [A-{formatted_num}] {naam} (S2)";
bind keyboard "3" "nameinradio [A-{formatted_num}] {naam} (S3)";
bind keyboard "4" "nameinradio [A-{formatted_num}] {naam} (S4)";
bind keyboard "5" "nameinradio [A-{formatted_num}] {naam} (HB)";

bind keyboard "6" "me [A-{formatted_num}] {naam} | {title}";
bind keyboard "6" "e whistle";
```"""

    # Message 2: The unbind cleanup utility
    unbind_output = f"""```text
unbind keyboard 1;unbind keyboard 2;unbind keyboard 3;unbind keyboard 4;unbind keyboard 5;unbind keyboard 6
```"""

    # Delivers both blocks cleanly
    await interaction.followup.send(bind_output, ephemeral=True)
    await interaction.followup.send(unbind_output, ephemeral=True)

# Safely fetch the token from the environment variables

# Run your bot
bot.run('my_token')
