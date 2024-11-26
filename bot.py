import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import asyncio

# Cargar variables de entorno desde .env
load_dotenv()

# Variables de entorno
TOKEN = os.getenv("DISCORD_TOKEN")
TARGET_CHANNEL_ID = int(os.getenv("TARGET_CHANNEL_ID"))
TONE_PATH = "timbre.mp3"  # Ruta del sonido del timbre

# Configuración de intents
intents = discord.Intents.default()
intents.guilds = True
intents.voice_states = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")

@bot.event
async def on_voice_state_update(member, before, after):
    # Ignorar si no hay cambio de canal
    if before.channel == after.channel:
        return

    if after.channel:  # Si alguien entra a un canal de voz
        try:
            guild = member.guild
            target_channel = guild.get_channel(TARGET_CHANNEL_ID)

            if target_channel and isinstance(target_channel, discord.VoiceChannel):
                vc = await target_channel.connect()
                vc.play(discord.FFmpegPCMAudio(TONE_PATH), after=lambda e: asyncio.run_coroutine_threadsafe(vc.disconnect(), bot.loop))
        except Exception as e:
            print(f"Error al reproducir sonido: {e}")

# Iniciar el bot
if TOKEN:
    bot.run(TOKEN)
else:
    print("Token no encontrado en el archivo .env")