import os
import discord
from discord.ext import commands
from python_aternos import Client


# Configuración
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Credenciales
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
ATERNOS_USER = os.getenv("ATERNOS_USER")
ATERNOS_PSWD = os.getenv("ATERNOS_PSWD")
CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL"))

# Iniciar sesión en Aternos
aternos = Client()
aternos.login(ATERNOS_USER, ATERNOS_PSWD)
server = aternos.list_servers()[0]  # Asume que solo tienes un servidor

@bot.event
async def on_ready():
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send("✅ Bot encendido y listo para usar. Usa `!start` para encender el servidor.")

@bot.command()
async def start(ctx):
    if server.status != "online":
        server.start()
        await ctx.send("🟢 Iniciando el servidor. Espera unos minutos...")
    else:
        await ctx.send("✅ El servidor ya está encendido.")

@bot.command()
async def status(ctx):
    await ctx.send(f"📡 Estado del servidor: `{server.status}`")

bot.run(DISCORD_TOKEN)

