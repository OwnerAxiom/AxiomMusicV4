```
╔════════════════════════════════════════════════════════════════════════╗
║                                                                        ║
║   ██╗ ██╗██╗ ██╗███╗   ███╗ ██╗   ██╗███████╗██╗ ██████╗             ║
║   ██║ ██║██║ ██║████╗ ████║ ██║   ██║██╔════╝██║██╔════╝             ║
║   ███████║██║ ██║██╔████╔██║ ██║   ██║███████╗██║██║                 ║
║   ██╔══██║██║ ██║██║╚██╔╝██║ ██║   ██║╚════██║██║██║                 ║
║   ██║  ██║╚██████╔╝██║ ╚═╝ ██║ ╚██████╔╝███████║██║╚██████╗          ║
║   ╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝  ╚═════╝ ╚══════╝╚═╝ ╚═════╝          ║
║                                                                        ║
║              🎵 Advanced Telegram Music Bot V4 🎵                      ║
║                                                                        ║
║          Powered by Pyrogram | Built with Py-Tgcalls                  ║
║                                                                        ║
╚════════════════════════════════════════════════════════════════════════╝
```

---

## 📖 **PROJECT OVERVIEW**

**AxiomMusic V4** is a powerful **Telegram Voice Chat Music Bot** designed to deliver premium music streaming with advanced features, AI integration, and seamless user experience. Stream from 10+ music platforms, enjoy intelligent playback controls, and experience lightning-fast performance!

---

## 👨‍💼 **OWNER & CREDITS**

| **Field** | **Details** |
|-----------|-----------|
| **Developer** | [@III_MAA7NAV_III](https://t.me/III_MAA7NAV_III) |
| **Support Group** | [@axlomm](https://t.me/axlomm) |
| **Update Channel** | [@axiombots](https://t.me/axiombots) |
| **Repository** | [github.com/OwnerAxiom/AxiomMusicV4](https://github.com/OwnerAxiom/AxiomMusicV4) |
| **License** | Educational Use Only |

---

## ⚡ **KEY FEATURES**

### 🎶 **MUSIC STREAMING**
- ✅ YouTube Music - 50M+ Songs
- ✅ Spotify - 70M+ Tracks
- ✅ SoundCloud - 24M+ Songs
- ✅ Apple Music - 100M+ Tracks
- ✅ Resso Music - Indian Content
- ✅ Telegram Files - Local Audio
- ✅ Direct URLs - HTTP/HTTPS Streams
- ✅ Playlists - Create & Manage

### 🎮 **PLAYBACK CONTROLS**
- ⏯️ Play/Pause - Full Control
- ⏭️ Skip Track - Jump Instantly
- 🔄 Replay - Repeat Song
- ⏱️ Seek Forward/Backward - ±25 Seconds
- 🔁 Loop Modes - Single/Playlist/Off
- 🎚️ Speed Control - 0.5x to 2x
- 📊 Progress Bar - Real-time Updates
- 🎯 Queue Jump - Jump to Any Song

### 📋 **QUEUE MANAGEMENT**
- Queue Display - See Upcoming Songs
- Add/Remove Songs - Full Control
- Shuffle Mode - Random Order
- Auto Suggestions - Smart Recommendations
- Playlist Support - Create & Share
- Save Preferences - Store Favorites

### 🎨 **USER INTERFACE**
- 🖼️ Custom Thumbnails - Album Art Display
- 🎭 Theme Support - Multiple Themes
- 💬 Multi-Language - 20+ Languages
- 📱 Mobile Optimized - Works Everywhere
- ✨ Smooth Animations - Beautiful Transitions
- 🎯 Inline Buttons - One-Tap Controls

### 👥 **ADMIN FEATURES**
- 🔐 Admin-Only Commands - Secure Access
- 🗳️ Vote Skip System - Democratic Control
- 👤 User Management - Ban/Unban Users
- 📢 Broadcast Messages - Reach All Groups
- ⚙️ Per-Group Settings - Customization
- 📊 Statistics - Track Usage
- 🔔 Notifications - Real-time Alerts

### 🤖 **AI & INTELLIGENCE**
- 🧠 OpenAI Integration - Smart Responses
- 🎵 Smart Recommendations - Mood-Based
- 📝 Lyric Search - Find Lyrics Instantly
- 🔍 Voice Search - Humming Recognition
- 📊 Predictive Analytics - Next Song Prediction
- 🌟 Auto-DJ Mode - Automated Playlists

---

## 🚀 **DEPLOYMENT & SETUP**

### **Railway (Recommended - 1 Click Deploy)**
```bash
1. Go to https://railway.app
2. Click "New Project" → "Deploy from GitHub"
3. Select: OwnerAxiom/AxiomMusicV4
4. Configure Variables (see below)
5. Deploy & Enjoy! 🎉
```

### **Heroku**
```bash
heroku create your-music-bot
heroku buildpacks:add heroku/python
heroku buildpacks:add https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest.git
heroku config:set API_ID=xxx API_HASH=xxx BOT_TOKEN=xxx
git push heroku main
```

### **Docker**
```bash
docker build -t axiommusic .
docker run -e API_ID=xxx -e BOT_TOKEN=xxx -e MONGO_DB_URI=xxx axiommusic
```

### **Local Development**
```bash
# Clone Repository
git clone https://github.com/OwnerAxiom/AxiomMusicV4
cd AxiomMusicV4

# Setup Environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install Dependencies
pip install -r requirements.txt

# Configure
cp sample.env .env
# Edit .env with your credentials

# Run
python start
```

---

## 🔑 **ENVIRONMENT VARIABLES**

### **Required Variables**
```env
# Telegram Credentials
API_ID=39930006
API_HASH=0c1afd87f1a69d0e9a8b06b779480f51
BOT_TOKEN=YOUR_BOT_TOKEN_HERE
STRING_SESSION=YOUR_STRING_SESSION_HERE

# Owner Configuration
OWNER_ID=7169279112
OWNER_USERNAME=@III_MAA7NAV_III
BOT_USERNAME=@YourBotName

# Database
MONGO_DB_URI=mongodb+srv://username:password@cluster0.mongodb.net/

# Support Links
SUPPORT_CHANNEL=https://t.me/axiombots
SUPPORT_CHAT=https://t.me/axlomm

# Music APIs
YT_API_KEY=ShrutiBotsx7llDDmWnF986ygx9seT
YOUTUBE_DATA_API_KEY=INFLEX90156228D
NEXGEN_API_KEY=your_nexgen_key
INFLIX_API_KEY=INFLEX96052828D
```

### **Optional Variables**
```env
DURATION_LIMIT=54000
SONG_DOWNLOAD_DURATION_LIMIT=54000
PLAYLIST_FETCH_LIMIT=25
AUTO_LEAVING_ASSISTANT=False
AUTO_SUGGESTION_MODE=True
COMMAND_HANDLER=! / .
```

### **Get Values From:**
- **API_ID & API_HASH**: https://my.telegram.org
- **BOT_TOKEN**: [@BotFather](https://t.me/BotFather)
- **STRING_SESSION**: [@StringSessionBot](https://t.me/StringSessionBot)
- **MONGO_DB_URI**: https://cloud.mongodb.com

---

## 🎮 **COMMANDS**

### **Music Commands**
```
/play [song/url]        Play a song
/pause                  Pause playback
/resume                 Resume playback
/skip                   Skip to next
/stop                   Stop & leave
/queue                  View queue
/now                    Current song
/seek [time]            Jump to time
/loop [mode]            Set loop mode
/shuffle                Shuffle queue
```

### **Playlist Commands**
```
/playlist create [name] Create playlist
/playlist add [song]    Add to playlist
/playlist play [name]   Play playlist
/myplaylists            View your playlists
/playlist delete [name] Delete playlist
```

### **Settings Commands**
```
/settings               Configure bot
/lang [language]        Change language
/thumbnail on/off       Toggle thumbnails
/autoplay on/off        Toggle suggestions
/prefix [symbol]        Change prefix
/theme [theme]          Change theme
```

### **User Commands**
```
/stats                  View statistics
/profile                View profile
/help                   Get help
/ping                   Check latency
/about                  About bot
/support                Support info
```

### **Admin Commands** (Voice Chat Admin Required)
```
/ban [@user]            Ban user
/unban [@user]          Unban user
/kick [@user]           Kick from chat
/broadcast [msg]        Send broadcast
/logs [lines]           View logs
/clearqueue             Clear all songs
/restart                Restart bot
```

---

## 📊 **TECH STACK**

| Component | Technology |
|:--|:--|
| **Language** | Python 3.10+ |
| **Framework** | Pyrogram / PyroTgFork |
| **Voice API** | Py-TgCalls / Ntgcalls |
| **Database** | MongoDB (Motor async) |
| **HTTP Client** | HTTPX / Requests |
| **Media** | FFmpeg / Yt-dlp |
| **Task Scheduler** | APScheduler |
| **Image Processing** | Pillow / Hachoir |
| **AI Integration** | OpenAI API |
| **Deployment** | Docker / Railway / Heroku |

---

## 📁 **PROJECT STRUCTURE**

```
AxiomMusicV4/
├── AxiomMusic/
│   ├── core/            # Bot Core
│   │   ├── bot.py      # Bot Init
│   │   ├── call.py     # Voice Chat
│   │   ├── userbot.py  # Userbot
│   │   └── git.py      # Git Integration
│   ├── plugins/         # Commands
│   │   ├── play/       # Play Commands
│   │   ├── admins/     # Admin Tools
│   │   └── bot/        # Bot Commands
│   ├── utils/          # Utilities
│   │   ├── inline/     # Buttons
│   │   ├── stream/     # Streaming
│   │   └── database/   # Database Layer
│   ├── platforms/      # Music APIs
│   │   ├── youtube.py  # YouTube
│   │   ├── spotify.py  # Spotify
│   │   └── soundcloud.py
│   └── __init__.py
├── strings/            # Multi-Language
├── config.py           # Configuration
├── requirements.txt    # Dependencies
├── Dockerfile          # Docker
├── Procfile           # Heroku
├── app.json           # Railway
└── README.md          # This File
```

---

## 🆘 **TROUBLESHOOTING**

### **Bot Not Responding**
```
✓ Check BOT_TOKEN is correct
✓ Verify API_ID & API_HASH
✓ Ensure bot has admin rights
✓ Check internet connection
✓ Verify LOGGER_ID is set
```

### **No Sound in Voice Chat**
```
✓ Install FFmpeg: apt-get install ffmpeg
✓ Verify STRING_SESSION is valid
✓ Check bot permissions
✓ Check firewall settings
✓ Restart bot: /restart
```

### **MongoDB Connection Error**
```
✓ Verify MONGO_DB_URI format
✓ Add IP to MongoDB whitelist
✓ For Railway: Use MONGO_URL
✓ Test connection locally
```

### **Songs Not Playing**
```
✓ Check YouTube/Spotify accessibility
✓ Verify API keys are valid
✓ Try different song/platform
✓ Update yt-dlp: pip install -U yt-dlp
```

---

## 🌟 **WHAT'S SPECIAL?**

✨ **Lightning Fast** - Optimized async operations  
✨ **Always Updated** - Regular feature releases  
✨ **Secure** - Encrypted & safe  
✨ **Mobile Friendly** - Works on all devices  
✨ **Powerful** - Advanced features included  
✨ **Easy to Use** - Intuitive interface  
✨ **Community Driven** - Active support  
✨ **Scalable** - Grows with your needs  
✨ **Beautiful** - Modern UI/UX  
✨ **Customizable** - Tailor to your preferences  

---

## 📞 **SUPPORT & COMMUNITY**

```
📢 Updates & News
└─ @axiombots
   https://t.me/axiombots

💬 Support & Help
└─ @axlomm
   https://t.me/axlomm
   • Get support
   • Report bugs
   • Suggest features
   • Chat with community

👤 Direct Contact
└─ @III_MAA7NAV_III
   https://t.me/III_MAA7NAV_III
   • Owner support
   • Business inquiries

💻 GitHub
└─ Issues & Pull Requests
   https://github.com/OwnerAxiom/AxiomMusicV4
```

---

## 🤝 **CONTRIBUTING**

We welcome contributions!

```bash
1. Fork the repository
2. Create feature branch: git checkout -b feature/name
3. Make your changes
4. Commit: git commit -m "Add feature"
5. Push: git push origin feature/name
6. Open Pull Request
```

---

## ⚠️ **LICENSE & LEGAL**

This code is for **educational use ONLY**.

✅ **Allowed:**
- Educational projects
- Personal use
- Learning & development
- Non-commercial apps

❌ **NOT Allowed:**
- Commercial use
- Redistribution without credit
- Removal of copyright notices
- Claiming as your own

See [LICENSE](/LICENSE) for details.

---

## 📈 **STATISTICS**

```
Repository: OwnerAxiom/AxiomMusicV4
Created: June 2026
Language: Python (99.9%)
Size: 12.6 MB
Status: ✅ Production Ready
Maintenance: Active 🔧
```

---

## 🙏 **ACKNOWLEDGMENTS**

- **Pyrogram Team** - Telegram API Library
- **Py-TgCalls Contributors** - Voice Chat Streaming
- **MongoDB** - Cloud Database
- **Shruti Bots** - Music API Services
- **All Contributors** - Helping us improve

---

```
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║        Made with 💖 by OwnerAxiom | Music Never Stops         ║
║                                                                ║
║           Join Us: @axlomm | Updates: @axiombots              ║
║                                                                ║
║                  🎵 HAPPY LISTENING! 🎵                       ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
```

**Version:** 4.0.0 | **Last Updated:** June 19, 2026 | **Status:** ✅ Live
