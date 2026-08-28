# Copyright (c) 2026 Themattmen & Ingetypt. All rights reserved.
# Zie LICENSE bestand voor de volledige licentvoorwaarden.
# https://github.com/Themattmen/dc-bot-Frederik.K/blob/main/LICENSE

import os
import discord
from discord import app_commands
from discord.ext import commands

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Your Discord ID encoded in HEX format
OWNER_HEX_ID = "a17a27284c00083"  


def verify_owner_id() -> int | None:
    """Decodes the Hex string back to integer ID.
    If modified or broken, it returns None to stop execution."""
    try:
        return int(OWNER_HEX_ID, 16)
    except Exception:
        return None


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    try:
        synced = await bot.tree.sync()
        print(f"Successfully synced {len(synced)} command(s) globally!")
    except Exception as e:
        print(e)


def get_job_title(nummer_input: str) -> str:
    """Determines the job title based on the input number range or specific text."""
    clean_str = str(nummer_input).strip().upper()

    if clean_str == "EE":
        return "Extra Eenheid"

    if clean_str.isdigit():
        num = int(clean_str)
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

    return "Onbekend Nummer"


@bot.tree.command(
    name="binds", description="Generate radio and action binds for a user."
)
@app_commands.describe(
    nummer="The ID number or code (e.g., 00, 6, 15, EE)",
    naam="The player name (e.g., Frederik.K)",
)
async def binds(interaction: discord.Interaction, nummer: str, naam: str):
    # 1. Verification Step: Verify owner ID exists and matches command invoker
    owner_id = verify_owner_id()
    if not owner_id or interaction.user.id != owner_id:
        return

    # Defer response for ephemeral delivery
    await interaction.response.defer(ephemeral=True)

    # 2. Format identifier (e.g., "6" -> "06", "EE" -> "EE")
    raw_input = str(nummer).strip().upper()
    if raw_input.isdigit():
        formatted_num = f"{int(raw_input):02d}"
    else:
        formatted_num = raw_input

    title = get_job_title(raw_input)

    # Message 1: Active binds output
    bind_output = f"""```text
bind keyboard "1" "nameinradio [A-{formatted_num}] {naam} (S1)";
bind keyboard "2" "nameinradio [A-{formatted_num}] {naam} (S2)";
bind keyboard "3" "nameinradio [A-{formatted_num}] {naam} (S3)";
bind keyboard "4" "nameinradio [A-{formatted_num}] {naam} (S4)";
bind keyboard "5" "nameinradio [A-{formatted_num}] {naam} (HB)";

bind keyboard "6" "me [A-{formatted_num}] {naam} | {title}";
bind keyboard "7" "e whistle";
```"""

    # Message 2: Cleanup utility output
    unbind_output = """```text
unbind keyboard 1;unbind keyboard 2;unbind keyboard 3;unbind keyboard 4;unbind keyboard 5;unbind keyboard 6;unbind keyboard 7
```"""

    # Deliver standard messages
    await interaction.followup.send(bind_output, ephemeral=True)
    await interaction.followup.send(unbind_output, ephemeral=True)

    # Extra check: Stuur de aanvullende binds ALLEEN als de functie Stagiair is
    if title == "Stagiair":
        stagiair_binds_output = """```text
// 1. Unbinds
unbind keyboard f4;
unbind keyboard f5;
unbind keyboard delete;
unbind keyboard n;

// 2. Binds
bind keyboard "f4" "+tablet_open";
bind keyboard "f5" "objectmenu";
bind keyboard "delete" "mechanicForceClose";
bind keyboard "n" "mechanicKoppel";
```"""
        await interaction.followup.send(stagiair_binds_output, ephemeral=True)

# Run your bot
bot.run('my_token')
