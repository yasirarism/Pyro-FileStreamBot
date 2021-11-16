# (c) @EverythingSuckz | @AbirHasan2005

from WebStreamer.bot import StreamBot
from WebStreamer.vars import Var
from WebStreamer.utils.human_readable import humanbytes
from WebStreamer.utils.database import Database
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant
db = Database(Var.DATABASE_URL, Var.SESSION_NAME)


@StreamBot.on_message(filters.command('start') & filters.private & ~filters.edited)
async def start(b, m):
    if not await db.is_user_exist(m.from_user.id):
        await db.add_user(m.from_user.id)
        await b.send_message(
            Var.BIN_CHANNEL,
            f"#NEW_USER: \n\nPengguna Baru [{m.from_user.first_name}](tg://user?id={m.from_user.id}) Dimulai !!"
        )
    usr_cmd = m.text.split("_")[-1]
    if usr_cmd == "/start":
        await m.reply_text(
            text='🙋 Halo gaesss!!\nAku adalah Link Generator Bot.\n\nKirimkan aku sebuah file dan lihatlah sebuah keajaiban!\n\nCredit Source by @AbirHasan2005 and Translated by @YasirArisM.',
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton('YMovieZ Channel', url='https://t.me/YMovieZNew'), InlineKeyboardButton('Support Group', url='https://t.me/YMoviezChat')],
                    [InlineKeyboardButton('My Blog', url='https://www.yasir.my.id')]
                ]
            ),
            disable_web_page_preview=True
        )
    elif m.text == "/start help":
        await m.reply_text(
            text='🌟 Jika kamu merasa bot ini sangat bermanfaat, kamu bisa donasi melalui link dan nomer dibawah ini. Berapapun nilainya saya sangat berterimakasih, jika ada kendala kamu bisa chat ke @YasirArisM. Thanks you.. \n\n~ <b>Saweria :</b> https://saweria.co/yasirarism\n~ <b>Dana :</b> 088220143804',
            disable_web_page_preview=True
        )
    else:
        get_msg = await b.get_messages(chat_id=Var.BIN_CHANNEL, message_ids=int(usr_cmd))

        file_size = None
        if get_msg.video:
            file_size = f"{humanbytes(get_msg.video.file_size)}"
        elif get_msg.document:
            file_size = f"{humanbytes(get_msg.document.file_size)}"
        elif get_msg.audio:
            file_size = f"{humanbytes(get_msg.audio.file_size)}"

        file_name = None
        if get_msg.video:
            file_name = f"{get_msg.video.file_name}"
        elif get_msg.document:
            file_name = f"{get_msg.document.file_name}"
        elif get_msg.audio:
            file_name = f"{get_msg.audio.file_name}"

        stream_link = "https://yasirlink.ga/{}".format(get_msg.message_id) if Var.ON_HEROKU or Var.NO_PORT else \
            "http://{}:{}/{}".format(Var.FQDN,
                                     Var.PORT,
                                     get_msg.message_id)

        msg_text = "Yeaaayyyy! 😁\nLink kamu berhasil di generate! 🤓\n\n📂 **Nama File:** `{}`\n**Ukuran File:** `{}`\n\n📥 **Download Link:** `{}`\n\n**Catatan:** Klik tombol untuk mendownload"
        await m.reply_text(
            text=msg_text.format(file_name, file_size, stream_link),
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Download Sekarang", url=stream_link)]])
        )


@StreamBot.on_message(filters.command('help') & filters.private & ~filters.edited)
async def help_handler(bot, message):
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id)
        await bot.send_message(
            Var.BIN_CHANNEL,
            f"#NEW_USER: \n\nPengguna Baru [{message.from_user.first_name}](tg://user?id={message.from_user.id}) Memulai !!"
        )
    await message.reply_text(
        text="Kirimkan aku sebuah file dan aku akan mengubah nya menjadi direct link!\n\nAku juga mendukung Channels loh. Tambahkan aku ke channel supaya aku bekerja!",
        parse_mode="Markdown",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Support Group", url="https://t.me/YMoviezChat"), InlineKeyboardButton("YMovieZ Channel", url="https://t.me/YMovieZNew")],
                [InlineKeyboardButton("OriginalDeveloper", url="https://t.me/AbirHasan2005")]
            ]
        )
    )
