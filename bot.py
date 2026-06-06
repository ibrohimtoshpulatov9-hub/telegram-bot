import telebot
import yt_dlp
import os

TOKEN = os.environ.get("TOKEN")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 
        "👋 Salom! Men video va musiqa yuklovchi botman!\n\n"
        "📎 YouTube yoki Instagram linki yuboring — video yuklayman\n"
        "🎵 Musiqa nomi yozing — yuklab beraman!")

@bot.message_handler(func=lambda message: True)
def download(message):
    link = message.text

    if "youtube.com" in link or "youtu.be" in link or "instagram.com" in link:
        bot.send_message(message.chat.id, "⏳ Video yuklanmoqda, kuting...")
        try:
            ydl_opts = {
                'format': 'best[ext=mp4]/best',
                'outtmpl': 'video.%(ext)s',
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([link])

            video_file = None
            for f in os.listdir('.'):
                if f.startswith('video.'):
                    video_file = f
                    break

            if video_file:
                bot.send_message(message.chat.id, "📤 Yuborilmoqda...")
                with open(video_file, 'rb') as v:
                    bot.send_video(message.chat.id, v)
                os.remove(video_file)

        except Exception as e:
            bot.send_message(message.chat.id, "❌ Xatolik yuz berdi!")

    else:
        bot.send_message(message.chat.id, f"🎵 '{link}' qidirilmoqda...")
        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': 'music.%(ext)s',
                'default_search': 'ytsearch1',
                'noplaylist': True,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([link])

            music_file = None
            for f in os.listdir('.'):
                if f.startswith('music.'):
                    music_file = f
                    break

            if music_file:
                bot.send_message(message.chat.id, "📤 Yuborilmoqda...")
                with open(music_file, 'rb') as m:
                    bot.send_audio(message.chat.id, m)
                os.remove(music_file)

        except Exception as e:
            bot.send_message(message.chat.id, f"❌ Xatolik: {e}")

print("✅ Bot ishlamoqda...")
bot.polling()