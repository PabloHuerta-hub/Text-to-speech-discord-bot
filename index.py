
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import asyncio
from gtts import gTTS
import google.generativeai as genai

load_dotenv()

#implementacion de gemini AI
genai.configure(api_key=os.getenv("API_KEY"))
model = genai.GenerativeModel('gemini-pro')


#intents de discord bot
intents = discord.Intents.all()
intents.messages = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def tts(ctx, *, text):
    if ctx.voice_client is None:
        if ctx.author.voice is None or ctx.author.voice.channel is None:
            await ctx.send("¡Necesitas estar en un canal de voz para usar este comando!")
            return

        channel = ctx.author.voice.channel
        voice_channel = await channel.connect()

        print("Bot joined voice channel.")
    else:
        voice_channel = ctx.voice_client


    tts = gTTS(text=text, lang='es', slow=False)
    tts.save("tts_output.mp3")

    voice_channel.play(discord.FFmpegPCMAudio('tts_output.mp3'), after=lambda e: print('done', e))
    while voice_channel.is_playing():
         await asyncio.sleep(1)

    print("Audio playback finished.")

    if os.path.exists("tts_output.mp3"):
       os.remove('tts_output.mp3')
    else:
        print("El archivo 'tts_output.wav' no existe.")

@bot.command()
async def leave(ctx):
    if ctx.voice_client is not None:
        await ctx.voice_client.disconnect()
        await ctx.send("Bot desconectado")
    else:
        await ctx.send("Debo estar en un canal de voz para desconectarme")

@bot.command()
async def gemini(ctx,*,text):
    try:

        if ctx.channel.name == 'consultas-gemini':
            response = model.generate_content(text)
            await ctx.send(response.text)
            await asyncio.sleep(5)
        else:
            await ctx.send("Es mejor que uses otro canal para hacerme consultas")
    except Exception as e:
        print(f"Error en el comando gemini: {e}")

# usar el token que provee el servicio de developers de discord
bot.run(os.getenv("DISCORD_TOKEN"))


