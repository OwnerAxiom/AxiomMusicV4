from pyrogram import filters
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup

from AxiomMusic import app
from AxiomMusic.utils.stream.thumbnail import (
    toggle_thumbnail_status,
    get_thumbnail_status,
)
from AxiomMusic.utils.inline.play import (
    stream_markup,
)


@app.on_callback_query(filters.regex("^THUMBTOGGLE"))
async def thumbnail_toggle_callback(_, query: CallbackQuery):

    data = query.data.split("|")
    chat_id = int(data[1])

    new_status = toggle_thumbnail_status(chat_id)

    status_text = (
        "🖼 ᴛʜᴜᴍʙɴᴀɪ ᴇɴʙʟᴇ"
        if new_status == "on"
        else "🖼 ᴛʜᴜᴍʙɴᴀɪ ᴅɪsᴀʙʟᴇᴅ"
    )

    try:
        await query.answer(status_text, show_alert=False)

        # ✅ SAHI CODE - Sirf 2 parameters
        markup = InlineKeyboardMarkup(
            stream_markup(
                _,  # First parameter: _ (translator)
                chat_id,  # Second parameter: chat_id
            )
        )

        await query.message.edit_reply_markup(reply_markup=markup)

    except Exception:
        pass
