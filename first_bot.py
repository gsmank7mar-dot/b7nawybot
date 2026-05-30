import discord
from discord import app_commands
from discord.ext import commands
import socket
import requests
import os
from flask import Flask, render_template
from threading import Thread

# إعداد الويب
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

def run_web():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# إعداد البوت
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'=== المساعد السيبراني {bot.user} يعمل الآن ===')

# الأوامر
@bot.tree.command(name="scan", description="فحص المنافذ")
async def scan(interaction: discord.Interaction, target_ip: str):
    await interaction.response.send_message(f"جارٍ فحص `{target_ip}`...")

@bot.tree.command(name="osint", description="جمع معلومات النطاق")
async def osint(interaction: discord.Interaction, domain: str):
    await interaction.response.send_message(f"جاري جلب بيانات `{domain}`...")

# تشغيل النظامين معاً
if __name__ == "__main__":
    t = Thread(target=run_web)
    t.start()
    bot.run(os.environ['DISCORD_TOKEN'])
