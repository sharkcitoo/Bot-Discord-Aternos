import discord
from discord.ext import commands
from python_aternos import Client
import os
import asyncio

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.messages = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")

@bot.command()
async def encender(ctx):
    await ctx.send("🟡 Encendiendo servidor...")

    try:
        user = os.getenv("ATERNOS_USER")
        password = os.getenv("ATERNOS_PSWD")
        servidor_index = int(os.getenv("N_SERVIDOR", 0))

        atclient = Client.from_credentials(user, password)
        server = atclient.list_servers()[servidor_index]

        if server.status == "online":
            await ctx.send("🟢 El servidor ya está encendido.")
            return

        server.start()
        await ctx.send("⏳ Servidor iniciando... puede tardar unos minutos.")

        for _ in range(20):
            await asyncio.sleep(10)
            server.fetch()
            if server.status == "online":
                await ctx.send("✅ ¡Servidor encendido!")
                return

        await ctx.send("⚠️ Tardó demasiado, puede que no se haya encendido.")
    
    except Exception as e:
        await ctx.send(f"❌ Error al encender el servidor: {e}")

# Reemplazar bot.run() por asyncio.run()
async def main():
    async with bot:
        await bot.start(os.getenv("DISCORD_TOKEN"))

asyncio.run(main())
