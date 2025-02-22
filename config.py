import os
import time
from pyrogram import Client, filters

API_ID = 25698862  # Apna API ID dalein
API_HASH = "7d7739b44f5f8c825d48cc6787889dbc"  # Apna API Hash dalein
BOT_TOKEN = "8058670363:AAFjE5WxGuf7AY0EXOODPmqsJJ8fom3U0ZQ"  # Apna Bot Token dalein

bot = Client("video_renamer_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

thumbnail_dict = {}

# Bot Start Command
@bot.on_message(filters.private & filters.command("start"))
async def start_command(client, message):
    await message.reply_text("👋 Welcome! Ab aap bot use kar sakte hain.\n\nSend a thumbnail first!")

# Receive Thumbnail
@bot.on_message(filters.private & filters.photo)
async def thumbnail_handler(client, message):
    user_id = message.chat.id

    thumbnail_path = f"thumbnail_{user_id}.jpg"
    await message.download(file_name=thumbnail_path)
    thumbnail_dict[user_id] = thumbnail_path

    await message.reply_text("✅ Thumbnail saved! Now send me the video.")

# Receive Video
@bot.on_message(filters.private & filters.video)
async def video_handler(client, message):
    user_id = message.chat.id

    if user_id not in thumbnail_dict:
        await message.reply_text("❌ Please send a thumbnail first.")
        return

    thumbnail_path = thumbnail_dict.pop(user_id)

    if not os.path.exists(thumbnail_path):
        await message.reply_text("❌ Error: Thumbnail not found!")
        return

    video_path = await bot.download_media(message.video.file_id)
    
    if not os.path.exists(video_path):
        await message.reply_text("❌ Error: Video download failed!")
        return

    await message.reply_text("✅ Processing your video... Please wait!")

    try:
        await bot.send_video(
            user_id,
            video=video_path,
            thumb=thumbnail_path,
            caption="🎬 Here is your video with new thumbnail!"
        )
        await message.reply_text("✅ Video sent successfully!")

        # Clean up the files
        os.remove(video_path)
        os.remove(thumbnail_path)

    except Exception as e:
        await message.reply_text(f"❌ Error sending video: {str(e)}")

print("Bot is running...")
bot.run()