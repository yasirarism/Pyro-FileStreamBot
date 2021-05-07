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
        if Var.UPDATES_CHANNEL is not None:
            try:
                user = await b.get_chat_member(Var.UPDATES_CHANNEL, m.chat.id)
                if user.status == "kicked":
                    await b.send_message(
                        chat_id=m.chat.id,
                        text="Maaf, kamu dibanned dari bot ini. Hubungi saya di [Support Group](https://t.me/YMoviezChat).",
                        parse_mode="markdown",
                        disable_web_page_preview=True
                    )
                    return
            except UserNotParticipant:
                await b.send_message(
                    chat_id=m.chat.id,
                    text="**Silahkan gabung channel saya melalui button dibawah ini!**\n\nHanya yang sudah gabung channel saya yang bisa menggunakan bot ini",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("🔔 Gabung Channel", url=f"https://t.me/{Var.UPDATES_CHANNEL}")
                            ]
                        ]
                    ),
                    parse_mode="markdown"
                )
                return
            except Exception:
                await b.send_message(
                    chat_id=m.chat.id,
                    text="Seperti nya ada yang salah. Hubungi saya di [Support Group](https://t.me/YMovieZChat).",
                    parse_mode="markdown",
                    disable_web_page_preview=True)
                return
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
    else:
        if Var.UPDATES_CHANNEL is not None:
            try:
                user = await b.get_chat_member(Var.UPDATES_CHANNEL, m.chat.id)
                if user.status == "kicked":
                    await b.send_message(
                        chat_id=m.chat.id,
                        text="Maaf, kamu sudah dibanned dari bot ini. Hubungi saya di [Support Group](https://t.me/YMoviezChat).",
                        parse_mode="markdown",
                        disable_web_page_preview=True
                    )
                    return
            except UserNotParticipant:
                await b.send_message(
                    chat_id=m.chat.id,
                    text="**Untuk menggunakan bot ini silahkan gabung channel saya melalui button dibawah ini!**\n\nHanya subscriber channel yang bisa menggunakan bot ini!",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("🔔 Gabung Channel", url=f"https://t.me/{Var.UPDATES_CHANNEL}")
                            ],
                            [
                                InlineKeyboardButton("🔄 Refresh / Coba Lagi",
                                                     url=f"https://t.me/YasirRoBot?start=YasirPedia_{usr_cmd}")
                            ]
                        ]
                    ),
                    parse_mode="markdown"
                )
                return
            except Exception:
                await b.send_message(
                    chat_id=m.chat.id,
                    text="Seperti nya ada yang salah. Hubungi saya di [Support Group](https://t.me/YMoviezChat).",
                    parse_mode="markdown",
                    disable_web_page_preview=True)
                return

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

        stream_link = "https://{}/{}".format(Var.FQDN, get_msg.message_id) if Var.ON_HEROKU or Var.NO_PORT else \
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
    if Var.UPDATES_CHANNEL is not None:
        try:
            user = await bot.get_chat_member(Var.UPDATES_CHANNEL, message.chat.id)
            if user.status == "kicked":
                await bot.send_message(
                    chat_id=message.chat.id,
                    text="Maaf, kamu sudah dibanned dari bot ini. Hubungi saya di [Support Group](https://t.me/YMoviezChat).",
                    parse_mode="markdown",
                    disable_web_page_preview=True
                )
                return
        except UserNotParticipant:
            await bot.send_message(
                chat_id=message.chat.id,
                text="**Silahkan gabung channel saya untuk menggunakan bot ini!**\n\nHanya subscriber channel yang bisa menggunakan bot ini!",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("🔔 Gabung Channel", url=f"https://t.me/{Var.UPDATES_CHANNEL}")
                        ]
                    ]
                ),
                parse_mode="markdown"
            )
            return
        except Exception:
            await bot.send_message(
                chat_id=message.chat.id,
                text="Something went Wrong. Contact my [Support Group](https://t.me/linux_repo).",
                parse_mode="markdown",
                disable_web_page_preview=True)
            return
    await message.reply_text(
        text="Kirimkan aku sebuah file dan aku akan mengubah nya menjadi direct link!\n\nAku juga mendukung Channels loh. Tambahkan aku ke channel supaya aku bekerja!",
        parse_mode="Markdown",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Support Group", url="https://t.me/YMoviezChat"), InlineKeyboardButton("YMovieZ Channel", url="https://t.me/YMovieZNew")],
                [InlineKeyboardButton("Developer", url="https://t.me/AbirHasan2005")]
            ]
        )
    )
