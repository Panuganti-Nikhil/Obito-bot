# Ash Bot

Ash Bot is a comprehensive, multi-purpose Discord bot built with `discord.py`. Originally starting as an administrative and utility bot, it has rapidly expanded into a fully featured moderation, music, economy, and anime interaction system.

With over 400+ dynamically compiled commands, Ash Bot aims to be the single bot you need to control, entertain, and manage your Discord servers.

---

## 🌟 Key Features

* **Advanced Music System**
  * Stream high-quality audio directly from YouTube and other platforms via `yt-dlp`.
  * Interactive control panel (`!musicpanel`) for easy Play/Pause, Skip, and Stop functionality without typing commands.
  * Robust queueing, volume control, and session management.

* **Extensive Anime Interactions**
  * Over 100+ unique anime-style reaction commands (e.g., `!hug`, `!slap`, `!pat`, `!cuddle`).
  * Integrates seamlessly with the `nekos.best` API to fetch context-aware GIFs and embeds for user interactions.

* **Economy & Currency**
  * Built-in economy system featuring daily rewards, balances, gambling, and user-to-user transfers.
  * Server leaderboards to track the richest users.

* **Advanced Administration & Moderation**
  * Total server control: load/unload cogs dynamically, run shell commands, execute raw Python blocks (Owner Only).
  * Mass DMing, webhook manipulation, thread bombing, and channel cloning capabilities.
  * Automated raid prevention and server analyzer metrics.

* **Dynamic Cog Compilation (`builder.py`)**
  * Unlike standard bots, Ash Bot uses a custom build step. Individual feature cogs are written cleanly in `old_cmds_folder/` and then dynamically bundled into a master `cmds.py` file using `builder.py`. This ensures fast loading and centralized command structures.

---

## 🛠️ Prerequisites

Before you install and run Ash Bot, ensure you have the following installed on your system:

* **Python 3.8+**
* **FFmpeg** (Required for music playback)
  * *Ubuntu/Debian:* `sudo apt-get install ffmpeg`
  * *Windows:* Download from the [FFmpeg official site](https://ffmpeg.org/download.html) and add it to your System PATH.
  * *MacOS:* `brew install ffmpeg`

---

## 🚀 Installation & Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/ash-bot.git
   cd ash-bot
   ```

2. **Install Python Dependencies**
   Install all required libraries using `pip`:
   ```bash
   pip install -r requirements.txt
   ```
   *(Note: Ensure `discord.py`, `yt-dlp`, `PyNaCl`, `aiohttp`, `python-dotenv`, and `pyfiglet` are installed).*

3. **Configure Environment Variables**
   Create a `.env` file in the root directory of the project and add your bot's credentials:
   ```env
   DISCORD_BOT_TOKEN=your_bot_token_here
   OWNER_ID=your_discord_user_id_here
   ```

---

## 🏗️ Building and Adding Commands

Because of Ash Bot's unique architecture, you **do not** directly edit `cmds.py`.

1. To add a new feature, create or edit a Python cog file inside the `old_cmds_folder/`.
2. Once your changes are saved, run the builder script:
   ```bash
   python3 builder.py
   ```
3. This will parse all files in `old_cmds_folder/` and `extented_features.txt` and regenerate the master `cmds.py` file.
4. Don't forget to update the `commands_list.txt` to keep the documentation accurate!

---

## ▶️ Running the Bot

Once everything is installed and built, you can start the bot by running:

```bash
python3 main.py
```

The bot will print a log confirming it has logged in, loaded its cogs, and validated Opus/Voice support.

---

## 📚 Command Documentation

For a full list of the 400+ commands available, please refer to the [`commands_list.txt`](commands_list.txt) file included in this repository.

---

## ⚖️ Disclaimer

Certain administrative commands (e.g., mass-DM, webhook spamming, exploit testing) are designed for authorized server testing, moderation, and specific owner-only use cases. Use them responsibly and ensure you comply with Discord's Terms of Service.
