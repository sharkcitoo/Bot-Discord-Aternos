import discord
from discord.ext import commands
from python_aternos import Client
import os
import asyncio

# Intents necesarios para que el bot pueda leer mensajes y responder
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.messages = True

# Crear el bot
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")

@bot.command()
async def encender(ctx):
    await ctx.send("🟡 Encendiendo servidor...")

    try:
        # Leer variables de entorno
        user = os.getenv("ATERNOS_USER")
        password = os.getenv("ATERNOS_PSWD")
        servidor_index = int(os.getenv("N_SERVIDOR", 0))  # Por defecto 0

        # Conectarse a Aternos
        atclient = Client.from_credentials(user, password)
        server = atclient.list_servers()[servidor_index]

        if server.status == "online":
            await ctx.send("🟢 El servidor ya está encendido.")
            return

        server.start()
        await ctx.send("⏳ Servidor iniciando... puede tardar unos minutos.")

        # Esperar hasta que el servidor esté encendido
        for _ in range(20):  # Intenta durante 2-3 minutos
            await asyncio.sleep(10)
            server.fetch()
            if server.status == "online":
                await ctx.send("✅ ¡Servidor encendido!")
                return

        await ctx.send("⚠️ Tardó demasiado, puede que no se haya encendido.")
    
    except Exception as e:
        await ctx.send(f"❌ Error al encender el servidor: {e}")

# Iniciar el bot con el token
bot.run(os.getenv("DISCORD_TOKEN"))
