# -----------------------------------------------
# 🔸 AxiomMusic Project
# 🔹 Developed & Maintained by: Axiom Bots (https://t.me/axiombots)
# 📅 Copyright © 2026 – All Rights Reserved
#
# 📖 License:
# This source code is open for educational and non-commercial use ONLY.
# You are required to retain this credit in all copies or substantial portions of this file.
# Commercial use, redistribution, or removal of this notice is strictly prohibited
# without prior written permission from the author.
#
# ❤️ Made with dedication and love by AxiomBots
# -----------------------------------------------

import asyncio
import importlib
import os
import threading
import time
import requests
from flask import Flask
from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall

import config
from AxiomMusic import LOGGER, app, userbot
from AxiomMusic.core.call import Axiomm
from AxiomMusic.core.mongo import verify_mongo_connection
from AxiomMusic.misc import sudo
from AxiomMusic.plugins import ALL_MODULES
from AxiomMusic.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS

# ─────────────────────────────────────────────
# Flask Health Server
# ─────────────────────────────────────────────

_flask = Flask(__name__)

@_flask.route("/")
def home():
    return "AxiomMusic is Running ❤️", 200

@_flask.route("/health")
def health():
    return "OK", 200

def run_flask():
    port = int(os.getenv("PORT", 8000))
    _flask.run(
        host="0.0.0.0",
        port=port,
        use_reloader=False,
    )

# ─────────────────────────────────────────────
# Auto Keep Alive
# ─────────────────────────────────────────────

def keep_alive():
    port = os.getenv("PORT", "8000")
    url = os.getenv(
        "RENDER_EXTERNAL_URL",
        f"http://127.0.0.1:{port}"
    )
    while True:
        try:
            requests.get(url, timeout=10)
            LOGGER(__name__).info(f"Keep Alive Ping → {url}")
        except Exception as e:
            LOGGER(__name__).warning(f"Keep Alive Error: {e}")
        time.sleep(300)

# ─────────────────────────────────────────────
# Main Startup
# ─────────────────────────────────────────────

async def init():
    # Start Flask
    threading.Thread(
        target=run_flask,
        daemon=True
    ).start()
    LOGGER(__name__).info("Flask Health Server Started")

    # Start Auto Ping
    threading.Thread(
        target=keep_alive,
        daemon=True
    ).start()
    LOGGER(__name__).info("Keep Alive Thread Started")

    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER(__name__).error("Assistant client variables not defined, exiting...")
        exit()
        
    await verify_mongo_connection()
    await sudo()
    
    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except:
        pass
        
    await app.start()
    
    for all_module in ALL_MODULES:
        importlib.import_module("AxiomMusic.plugins" + all_module)
        
    LOGGER("AxiomMusic.plugins").info("sᴜᴄᴄᴇssғᴜʟʟʏ ɪᴍᴘᴏʀᴛᴇᴅ ᴀʟʟ ᴍᴏᴅᴜʟᴇs...")
    
    await userbot.start()
    await Axiomm.start()
    
    try:
        await Axiomm.stream_call("https://te.legra.ph/file/39b302c93da5c457a87e3.mp4")
    except NoActiveGroupCall:
        LOGGER("AxiomMusic").error(
            "ʙsᴅᴋ ᴠᴄ ᴛᴏ ᴏɴ ᴋᴀʀʟᴇ  ʟᴏɢ ɢʀᴏᴜᴘ\ᴄʜᴀɴɴᴇʟ ᴋɪ.\n\n ᴏɴ ᴋᴀʀᴋᴇ ᴀᴀ ᴛᴀʙ ᴛᴀᴋ ʙᴏᴛ ʙᴀɴᴅ ᴋᴀʀ ʀʜᴀ ʜᴏᴏɴ..."
        )
        exit()
    except:
        pass
        
    await Axiomm.decorators()
    
    LOGGER("AxiomMusic").info(
        "ᴍᴜsɪᴄ ʙᴏᴛ sᴛᴀʀᴛᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ, ɴᴏᴡ ɢɪʙ ʏᴏᴜʀ ɢɪʀʟғʀɪᴇɴᴅ ᴄʜᴜᴛ ɪɴ @Axiombots"
    )
    
    await idle()
    
    await app.stop()
    await userbot.stop()
    
    LOGGER("AxiomMusic").info("ᴍᴀᴀ ᴄʜᴜᴅᴀ ᴍᴀɪɴ ʙᴏᴛ ʙᴀɴᴅ ᴋᴀʀ ʀʜᴀ Mᴜsɪᴄ Bᴏᴛ...")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init())
