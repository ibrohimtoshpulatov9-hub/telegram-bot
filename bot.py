import telebot
import yt_dlp
import os
import re

TOKEN = "8616732455:AAF0wf-2zSCUVr8HTvi6KwW-y1TpaiYW2tg"

bot = telebot.TeleBot(TOKEN)

def is_video_link(text):
    return bool(re.search(r'(https?://)?(www\.)?(youtube\.com|youtu\.be|instagram\.com)', text.lower()))


def find_file(prefix):
    for f in os.listdir('.'):
        if f.startswith(prefix):
            return f
    return None


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 
        "👋 Salom! Men video va musiqa yuklovchi botman!\n\n"
        "📎 YouTube yoki Instagram linki yuboring — video yuklayman\n"
        "🎵 Musiqa nomi yozing — yuklab beraman!")

@bot.message_handler(func=lambda message: True)
def download(message):
    link = message.text.strip()

    if not link:
        bot.send_message(message.chat.id, "❌ Iltimos, video yoki musiqa nomini yuboring.")
        return

    if is_video_link(link):
        bot.send_message(message.chat.id, "⏳ Video yuklanmoqda, kuting...")
        try:
            ydl_opts = {
                'format': 'best[ext=mp4]/best',
                'outtmpl': 'video_%(id)s.%(ext)s',
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([link])

            video_file = find_file('video_')

            if video_file:
                bot.send_message(message.chat.id, "📤 Yuborilmoqda...")
                with open(video_file, 'rb') as v:
                    bot.send_video(message.chat.id, v)
                os.remove(video_file)
            else:
                bot.send_message(message.chat.id, "❌ Video topilmadi.")

        except Exception as e:
            bot.send_message(message.chat.id, "❌ Xatolik yuz berdi!")

    else:
        bot.send_message(message.chat.id, f"🎵 '{link}' qidirilmoqda...")
        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': 'music_%(id)s.%(ext)s',
                'default_search': 'ytsearch1',
                'noplaylist': True,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([link])

            music_file = find_file('music_')

            if music_file:
                bot.send_message(message.chat.id, "📤 Yuborilmoqda...")
                with open(music_file, 'rb') as m:
                    bot.send_audio(message.chat.id, m)
                os.remove(music_file)
            else:
                bot.send_message(message.chat.id, "❌ Musiqa topilmadi.")

        except Exception as e:
            bot.send_message(message.chat.id, f"❌ Xatolik: {e}")

print("✅ Bot ishlamoqda...")
bot.polling()