import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import pyttsx3
import asyncio
from gtts import gTTS

load_dotenv()

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


bot.run(os.getenv('DISCORD_TOKEN'))
