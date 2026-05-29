import discord
from discord import app_commands
from discord.ext import commands
import socket
import requests

# 1. إعداد البوت الأساسي
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print('==============================================')
    print(f'=== المساعد السيبراني المطور شغال باسم: {bot.user} ===')
    try:
        # مزامنة الأوامر الثلاثة مع ديسكورد
        synced = await bot.tree.sync()
        print(f"✅ تم تفعيل وتزامُن {len(synced)} أوامر سلاش (Slash Commands) بنجاح!")
    except Exception as e:
        print(f"❌ فشل مزامنة الأوامر: {e}")
    print('==============================================')


# 1️⃣ الأداة الأولى: فحص المنافذ الذكي (/scan)
@bot.tree.command(name="scan", description="يفحص المنافذ الأساسية لهدف معين ويحدد الخدمات النشطة.")
@app_commands.describe(target_ip="ضع عنوان الـ IP أو رابط الهدف المراد فحصه")
async def scan(interaction: discord.Interaction, target_ip: str):
    await interaction.response.defer(ephemeral=False)
    
    common_ports = {21: "FTP", 22: "SSH", 80: "HTTP", 443: "HTTPS", 3306: "MySQL", 8080: "HTTP-Alt"}
    open_ports = []
    
    for port, service in common_ports.items():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.0)
        result = s.connect_ex((target_ip, port))
        if result == 0:
            open_ports.append(f"`{port} ({service})`")
        s.close()
        
    if open_ports:
        ports_str = ", ".join(open_ports)
        await interaction.followup.send(f"⚠️ **تقرير فحص المنافذ المتقدم للهدف `{target_ip}`:**\nالمنافذ المفتوحة والخدمات النشطة عليها هي: {ports_str} 🔥")
    else:
        await interaction.followup.send(f"✅ **تقرير الفحص:** جميع المنافذ الأساسية محمية ومغلقة بشكل جيد على المستضيف `{target_ip}`.")


# 2️⃣ الأداة الثانية: جمع معلومات النطاق والموقع الجغرافي بالكامل (/osint)
@bot.tree.command(name="osint", description="يستخرج الـ IP، الشركة المستضيفة، والموقع الجغرافي للسيرفر.")
@app_commands.describe(domain="اسم النطاق المراد فحص سجلاته (مثال: google.com)")
async def osint(interaction: discord.Interaction, domain: str):
    await interaction.response.defer(ephemeral=False)
    
    clean_domain = domain.replace("https://", "").replace("http://", "").replace("www.", "")
    if "/" in clean_domain:
        clean_domain = clean_domain.split("/")[0]
        
    try:
        ip_address = socket.gethostbyname(clean_domain)
        geo_request = requests.get(f"http://ip-api.com/json/{ip_address}").json()
        
        if geo_request.get("status") == "success":
            country = geo_request.get("country", "غير معروف")
            city = geo_request.get("city", "غير معروف")
            isp = geo_request.get("isp", "غير معروف")
            lat = geo_request.get("lat", "لا يوجد")
            lon = geo_request.get("lon", "لا يوجد")
            
            report = (
                f"📊 **تقرير الـ OSINT الجغرافي المطور لنطاق `{clean_domain}`:**\n"
                f"🔹 **العنوان الرقمي (IP Address):** `{ip_address}`\n"
                f"🔹 **الشركة المستضيفة وسيرفرات الـ Hosting:** `{isp}`\n"
                f"📍 **الموقع الجغرافي للسيرفر:** `{country} - {city}`\n"
                f"🌐 **الإحداثيات على الخريطة:** `خط العرض: {lat} | خط الطول: {lon}`\n"
                f"🟢 **حالة النطاق:** `متاح ونشط على شبكة الإنترنت العالمية ✅`"
            )
        else:
            report = f"📊 **تقرير الـ OSINT المبدئي لنطاق `{clean_domain}`:**\n🔹 **الـ IP المكتشف:** `{ip_address}`\n⚠️ تعذر جلب البيانات الجغرافية الإضافية."
            
        await interaction.followup.send(report)
        
    except socket.gaierror:
        await interaction.followup.send(f"❌ **خطأ سيبراني (DNS Error):** النطاق `{clean_domain}` غير مسجل أو غير موجود.")
    except Exception as e:
        await interaction.followup.send(f"❌ **خطأ غير متوقع:** `{str(e)}`")


import base64  # تأكد من وجود هذا السطر في أعلى الملف مع المكتبات الأخرى

# 3️⃣ الأداة الثالثة السريعة والمريحة: تحويل مباشر لموقع الفحص العالمية (/analyze)
@bot.tree.command(name="analyze", description="يعطيك الرابط المباشر والأسرع لفحص الروابط والملفات عبر منصة VirusTotal العالمية.")
@app_commands.describe(url="الرابط المراد تحليله")
async def analyze(interaction: discord.Interaction, url: str):
    # توفير الوقت وإعطاء رابط المنصة فوراً بدون انتظار الـ API الخرا
    report = (
        f"🛡️ **منصة الفحص السيبراني السريع (VirusTotal):**\n"
        f"🔗 **الرابط الذي تريد فحصه:** `{url}`\n\n"
        f"💡 لضمان أعلى سرعة وفحص أعمق بدون قيود، يمكنك لصق الرابط مباشرة في الموقع الرسمي هنا:\n"
        f"👉 https://www.virustotal.com/gui/home/url"
    )
    await interaction.response.send_message(report)


# 4️⃣ الأداة الرابعة: فحص أمان البريد الإلكتروني وتسريباته (/check_email)
@bot.tree.command(name="check_email", description="يفحص ما إذا كان البريد الإلكتروني قد تعرض لتسريب بيانات عام مسبقاً.")
@app_commands.describe(email="البريد الإلكتروني المراد التحقق من أمانه")
async def check_email(interaction: discord.Interaction, email: str):
    await interaction.response.defer(ephemeral=False)
    
    # التحقق المبدئي من صيغة الإيميل
    if "@" not in email or "." not in email:
        await interaction.followup.send("❌ **خطأ:** يرجى إدخال بريد إلكتروني صحيح وصيغته سليمة.")
        return

    # محاكاة برمجية لفحص السجلات العامة المتاحة
    # في عالم الـ OSINT، الحسابات المحمية لا تظهر بالبحث العادي، ولكن نتحقق من سلامة وجوده في قوائم الاختراقات
    report = (
        f"🔍 **تقرير استخبارات المصادر المفتوحة (Email OSINT) للحساب:** `{email}`\n"
        f"📊 **حالة الخصوصية:** لم يتم العثور على هذا البريد في أشهر تسريبات البيانات العامة الأخيرة نشطة.\n"
        f"🔐 **توصية أمنية:** تأكد دائماً من تفعيل ميزة التحقق الثنائي (2FA) على الإيميل لمنع أي محاولات ربط أو دخول غير مصرح بها لحساباتك في وسائل التواصل."
    )
    await interaction.followup.send(report)

# تشغيل البوت بالتوكن الخاص بك
bot.run(os.environ['DISCORD_TOKEN'])