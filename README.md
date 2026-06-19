```
    ╔════════════════════════════════════════════════════════════════════════╗
    ║                                                                        ║
    ║             ███╗   ███╗  ██╗   ██╗ ███████╗ ██╗ ██████╗                ║
    ║             ████╗ ████║  ██║   ██║ ██╔════╝ ██║ ██╔═══╝                ║
    ║             ██╔████╔██║  ██║   ██║ ███████╗ ██║ ██║                    ║
    ║             ██║╚██╝ ██║  ██║   ██║ ╚════██║ ██║ ██║                    ║
    ║             ██║     ██║  ╚██████╔╝ ███████║ ██║ ╚██████╗               ║
    ║             ╚═╝     ╚═╝   ╚═════╝  ╚══════╝ ╚═╝  ╚═════╝               ║
    ║                                                                        ║
    ║               🎵 Telegram Voice Chat Music Bot V4 🎵                  ║
    ║                                                                        ║
    ║              Powered by Pyrogram | Built with Py-Tgcalls               ║
    ║                                                                        ║
    ╚════════════════════════════════════════════════════════════════════════╝
```

---

## 📖 **ABOUT**

**AxiomMusic V4** is a feature-rich **Telegram Voice Chat Music Bot** for playing music in groups and channels. Stream from multiple platforms, manage queues, and enjoy smooth playback with beautiful UI.

---

## 👨‍💼 **OWNER & CONTACT**

| **Field** | **Info** |
|-----------|---------|
| **Developer** | [@III_MAA7NAV_III](https://t.me/III_MAA7NAV_III) |
| **Support Group** | [@axlomm](https://t.me/axlomm) |
| **Update Channel** | [@axiombots](https://t.me/axiombots) |
| **Repository** | [github.com/OwnerAxiom/AxiomMusicV4](https://github.com/OwnerAxiom/AxiomMusicV4) |

---

## ⚡ **FEATURES**

### 🎶 **Music Streaming**
- YouTube Music
- Spotify
- SoundCloud
- Apple Music
- Resso
- Telegram Files
- Direct URLs

### 🎮 **Playback Control**
- Play / Pause / Resume
- Skip to Next Track
- Replay Current Song
- Shuffle Queue
- Loop Modes (Single / Playlist / Off)

### 📋 **Queue Management**
- View Upcoming Songs
- Add/Remove from Queue
- Clear All Songs
- Auto Suggestions

### 🎨 **User Interface**
- Album Thumbnails
- Multi-Language Support (20+ Languages)
- Inline Control Buttons
- Settings Panel
- Language Selection

### 👥 **Admin Features**
- Ban/Unban Users
- Vote Skip System
- Broadcast Messages
- View Statistics
- User Management
- Group Settings

### ⚙️ **Settings**
- Toggle Thumbnails (On/Off)
- Change Language
- Autoplay with Mood Selection
- Customize Command Prefix

---

## 🚀 **QUICK SETUP**

### **Railway (Recommended)**
```bash
1. Go to https://railway.app
2. New Project → Deploy from GitHub
3. Select: OwnerAxiom/AxiomMusicV4
4. Add Variables (Below)
5. Deploy! 🎉
```

### **Heroku**
```bash
heroku create your-app
heroku buildpacks:add heroku/python
heroku config:set API_ID=xxx BOT_TOKEN=xxx
git push heroku main
```

### **Docker**
```bash
docker build -t axiommusic .
docker run -e API_ID=xxx -e BOT_TOKEN=xxx axiommusic
```

### **Local**
```bash
git clone https://github.com/OwnerAxiom/AxiomMusicV4
cd AxiomMusicV4
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp sample.env .env  # Edit with your credentials
python start
```

---

## 🔑 **ENVIRONMENT VARIABLES**

```env
# Telegram
API_ID=your_api_id
API_HASH=your_api_hash
BOT_TOKEN=your_bot_token
STRING_SESSION=your_string_session

# Owner
OWNER_ID=7169279112
OWNER_USERNAME=@III_MAA7NAV_III
BOT_USERNAME=@YourBotName

# Database
MONGO_DB_URI=mongodb+srv://username:password@cluster0.mongodb.net/

# Support
SUPPORT_CHANNEL=https://t.me/axiombots
SUPPORT_CHAT=https://t.me/axlomm

# APIs
YT_API_KEY=your_key
YOUTUBE_DATA_API_KEY=your_key
INFLIX_API_KEY=your_key
NEXGEN_API_KEY=your_key
```

**Get from:**
- **API_ID & API_HASH**: https://my.telegram.org
- **BOT_TOKEN**: [@BotFather](https://t.me/BotFather)
- **STRING_SESSION**: [@StringSessionBot](https://t.me/StringSessionBot)
- **MONGO_DB_URI**: https://cloud.mongodb.com

---

## 🎮 **COMMANDS**

### **Music Commands**
```
/play [song/url]        Play a song
/pause                  Pause music
/resume                 Resume playing
/skip                   Skip to next
/stop                   Stop & leave chat
/queue                  View queue
/shuffle                Shuffle queue
/now                    Current song info
```

### **Settings**
```
/settings               Configure bot
/lang [language]        Change language
/thumbnail on/off       Toggle thumbnails
/autoplay               Toggle autoplay with mood
/prefix [symbol]        Change command prefix
```

### **Admin** (Voice Chat Admin Only)
```
/ban [@user]            Ban user
/unban [@user]          Unban user
/clearqueue             Clear all songs
/broadcast [msg]        Send broadcast
/stats                  View statistics
```

### **General**
```
/start                  Start bot
/help                   Get help
/ping                   Check speed
/about                  About bot
```

---

## 📊 **TECH STACK**

- **Language**: Python 3.10+
- **Framework**: Pyrogram
- **Voice**: Py-TgCalls / Ntgcalls
- **Database**: MongoDB
- **Media**: FFmpeg, Yt-dlp
- **Deployment**: Docker, Railway, Heroku

---

## 📁 **PROJECT STRUCTURE**

```
AxiomMusicV4/
├── AxiomMusic/
│   ├── core/              # Bot Core
│   │   ├── bot.py        # Bot Init
│   │   ├── call.py       # Voice Chat
│   │   ├── userbot.py    # Userbot
│   │   └── git.py        # Git
│   ├── plugins/           # Commands
│   │   ├── play/         # Play Commands
│   │   ├── admins/       # Admin Tools
│   │   ├── bot/          # Bot Commands
│   │   ├── tools/        # Autoplay, Settings
│   │   └── extra/        # Extra Features
│   ├── utils/             # Utilities
│   │   ├── inline/       # Buttons
│   │   ├── stream/       # Streaming
│   │   ├── database/     # Database
│   │   └── decorators/   # Decorators
│   ├── platforms/         # Music APIs
│   │   ├── youtube.py
│   │   ├── spotify.py
│   │   └── soundcloud.py
│   └── __init__.py
├── strings/               # Languages (20+)
├── config.py              # Config
├── requirements.txt       # Dependencies
├── Dockerfile
├── Procfile
└── README.md
```

---

## 🆘 **TROUBLESHOOTING**

### **Bot not responding?**
```
✓ Check BOT_TOKEN is correct
✓ Verify API_ID & API_HASH
✓ Ensure bot is admin in group
✓ Check internet connection
```

### **No sound?**
```
✓ Install FFmpeg: apt-get install ffmpeg
✓ Check STRING_SESSION is valid
✓ Verify bot permissions
✓ Check firewall
```

### **MongoDB error?**
```
✓ Verify MONGO_DB_URI
✓ Add IP to whitelist
✓ For Railway: use MONGO_URL
```

---

## 📞 **SUPPORT**

```
📢 Updates: @axiombots
💬 Support: @axlomm
👤 Owner: @III_MAA7NAV_III
🐙 GitHub: github.com/OwnerAxiom/AxiomMusicV4
```

---

## 🤝 **CONTRIBUTING**

```bash
1. Fork repository
2. Create feature branch: git checkout -b feature/name
3. Make changes
4. Commit: git commit -m "Add feature"
5. Push: git push origin feature/name
6. Open Pull Request
```

---

## ⚠️ **LICENSE**

Educational use only. Retain credit in all copies. Commercial use prohibited.

See [LICENSE](/LICENSE) for details.

---

```
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║        Made with 💖 by OwnerAxiom | Keep Music Playing        ║
║                                                                ║
║              Join Us: @axlomm | Updates: @axiombots            ║
║                                                                ║
║                  🎵 ENJOY THE MUSIC! 🎵                       ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
```

**Version:** 4.0.0 | **Status:** ✅ Production Ready | **Updated:** June 19, 2026
