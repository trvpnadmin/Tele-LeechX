#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K | gautamajay52 | MaxxRider | 5MysterySD | Other Contributors 
#
# Copyright 2022 - TeamTele-LeechX
# 
# This is Part of < https://github.com/5MysterySD/Tele-LeechX >
# All Right Reserved 


import asyncio
import logging
import os
import time
from collections import defaultdict
from logging.handlers import RotatingFileHandler
from sys import exit
import urllib.request
import dotenv
import telegram.ext as tg

from pyrogram import Client

UPDATES_CHANNEL = os.environ.get("UPDATES_CHANNEL", "@FuZionX")
LOG_FILE_NAME = f"{UPDATES_CHANNEL}Logs.txt"

if os.path.exists(LOG_FILE_NAME):
    with open(LOG_FILE_NAME, "r+") as f_d:
        f_d.truncate(0)

# Logging Requirements >>>>>>>>>>>
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s [%(filename)s:%(lineno)d]",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        RotatingFileHandler(
            LOG_FILE_NAME, maxBytes=50000000, backupCount=10
        ),
        logging.StreamHandler(),
    ],
)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("PIL").setLevel(logging.WARNING)

LOGGER = logging.getLogger(__name__)

user_specific_config=dict()
__version__ = "2.5.15"
def getConfig(name: str):
    return os.environ[name]
CONFIG_FILE_URL = os.environ.get('CONFIG_FILE_URL')
try:
    if len(CONFIG_FILE_URL) == 0:
        raise TypeError
    try:
        res = requests.get(CONFIG_FILE_URL)
        if res.status_code == 200:
            with open('config.env', 'wb+') as f:
                f.write(res.content)
        else:
            LOGGER.error(f"Failed to download config.env {res.status_code}")
    except Exception as e:
        LOGGER.error(f"CONFIG_FILE_URL: {e}")
except:
    pass

try:
    HEROKU_API_KEY = getConfig('HEROKU_API_KEY')
    HEROKU_APP_NAME = getConfig('HEROKU_APP_NAME')
    if len(HEROKU_API_KEY) == 0 or len(HEROKU_APP_NAME) == 0:
        raise KeyError
except:
    HEROKU_APP_NAME = None
    HEROKU_API_KEY = None

dotenv.load_dotenv("config.env")

# Compulsory Variables >>>>>>>>
for imp in ["TG_BOT_TOKEN", "APP_ID", "API_HASH", "OWNER_ID", "AUTH_CHANNEL"]:
    try:
        value = os.environ[imp]
        if not value:
            raise KeyError
    except KeyError:
        LOGGER.critical(f"Oh...{imp} is missing from config.env ... fill that")
        exit()

# The Telegram API things >>>>>>>>>>>
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "5139162631:AAHGWHHbnbu7k5jOjXW-axcNuJcSRpBktr4")
APP_ID = os.environ.get("APP_ID", "6878048")
API_HASH = os.environ.get("API_HASH", "3833ae3a7415af46df46a83a3ba2c432")
OWNER_ID = int(os.environ.get("OWNER_ID", "1242011540"))

# Authorised Chat Functions >>>>>>>>>>>
AUTH_CHANNEL = [int(x) for x in os.environ.get("AUTH_CHANNEL", "-1001270496331 -1001508663868").split()]
SUDO_USERS = [int(sudos) if (' ' not in os.environ.get('SUDO_USERS', '')) else int(sudos) for sudos in os.environ.get('SUDO_USERS', '').split()]
AUTH_CHANNEL.append(OWNER_ID)
AUTH_CHANNEL += SUDO_USERS
# Download Directory >>>>>>>>>>>
DOWNLOAD_LOCATION = "./Downloads"

# Telegram maximum file upload size
MAX_FILE_SIZE = 50000000
TG_MAX_FILE_SIZE = 2097152000
TG_PRM_FILE_SIZE = 4194304000
FREE_USER_MAX_FILE_SIZE = 50000000

# chunk size that should be used with requests
CHUNK_SIZE = int(os.environ.get("CHUNK_SIZE", "128"))
DEF_THUMB_NAIL_VID_S = os.environ.get("DEF_THUMB_NAIL_VID_S", "https://telegra.ph/file/3a7f09b89943b51cdba38.jpg")
MAX_MESSAGE_LENGTH = 4096

# Timeout for Subprocess >>>>>>>>
PROCESS_MAX_TIMEOUT = 3600

# Internal Requirements >>>>>>>>>>>
SP_LIT_ALGO_RITH_M = os.environ.get("SP_LIT_ALGO_RITH_M", "hjs")
ARIA_TWO_STARTED_PORT = int(os.environ.get("ARIA_TWO_STARTED_PORT", "6800"))
EDIT_SLEEP_TIME_OUT = int(os.environ.get("EDIT_SLEEP_TIME_OUT", "10"))
MAX_TIME_TO_WAIT_FOR_TORRENTS_TO_START = int(os.environ.get("MAX_TIME_TO_WAIT_FOR_TORRENTS_TO_START", 600))
MAX_TG_SPLIT_FILE_SIZE = int(os.environ.get("MAX_TG_SPLIT_FILE_SIZE", "2097152000"))

# Vars for the Display Progress >>>>>>>>
FINISHED_PROGRESS_STR = os.environ.get("FINISHED_PROGRESS_STR", "■")
UN_FINISHED_PROGRESS_STR = os.environ.get("UN_FINISHED_PROGRESS_STR", "□")

# Add Offensive API >>>>>>>>
TG_OFFENSIVE_API = os.environ.get("TG_OFFENSIVE_API", None)
CUSTOM_FILE_NAME = os.environ.get("CUSTOM_FILE_NAME", "")

#Bot Command [Leech]  >>>>>>>>>>>
LEECH_COMMAND = os.environ.get("LEECH_COMMAND", "leech")
LEECH_UNZIP_COMMAND = os.environ.get("LEECH_UNZIP_COMMAND", "extract")
LEECH_ZIP_COMMAND = os.environ.get("LEECH_ZIP_COMMAND", "archive")
GLEECH_COMMAND = os.environ.get("GLEECH_COMMAND", "gleech")
GLEECH_UNZIP_COMMAND = os.environ.get("GLEECH_UNZIP_COMMAND", "gleechunzip")
GLEECH_ZIP_COMMAND = os.environ.get("GLEECH_ZIP_COMMAND", "gleechzip")

#Bot Command [yt-dlp] >>>>>>>>>>>
YTDL_COMMAND = os.environ.get("YTDL_COMMAND", "ytdl")
GYTDL_COMMAND = os.environ.get("GYTDL_COMMAND", "gytdl")
PYTDL_COMMAND = os.environ.get("PYTDL_COMMAND", "pytdl")
GPYTDL_COMMAND = os.environ.get("GPYTDL_COMMAND", "gpytdl")

#Bot Command [RClone]  >>>>>>>>>>>
RCLONE_CONFIG = os.environ.get("RCLONE_CONFIG", "")
DESTINATION_FOLDER = os.environ.get("DESTINATION_FOLDER", "FuZionXBot")
INDEX_LINK = os.environ.get("INDEX_LINK", "https://covid.demonn.workers.dev/0:/FuZionXBot https://infyplexultra.mysterydemon.workers.dev/0:/FuZionXBot")
GET_SIZE_G = os.environ.get("GET_SIZE_G", "getsize")
CLONE_COMMAND_G = os.environ.get("CLONE_COMMAND_G", "gclone")
TELEGRAM_LEECH_COMMAND = os.environ.get("TELEGRAM_LEECH_COMMAND", "tleech")
TELEGRAM_LEECH_UNZIP_COMMAND = os.environ.get("TELEGRAM_LEECH_UNZIP_COMMAND", "tleechunzip")

#Bot Command [Miscs]  >>>>>>>>>>>
CANCEL_COMMAND_G = os.environ.get("CANCEL_COMMAND_G", "cancel")
STATUS_COMMAND = os.environ.get("STATUS_COMMAND", "status")
SAVE_THUMBNAIL = os.environ.get("SAVE_THUMBNAIL", "savethumb")
CLEAR_THUMBNAIL = os.environ.get("CLEAR_THUMBNAIL", "clearthumb")
UPLOAD_AS_DOC = os.environ.get("UPLOAD_AS_DOC", "False")
LOG_COMMAND = os.environ.get("LOG_COMMAND", "log")

#Bot Command [Custom Bot Cmd Name]  >>>>>>>>>>>
SET_BOT_COMMANDS = os.environ.get("SET_BOT_COMMANDS", True)
UPLOAD_COMMAND = os.environ.get("UPLOAD_COMMAND", "upload")
RENEWME_COMMAND = os.environ.get("RENEWME_COMMAND", "renewme")
RENAME_COMMAND = os.environ.get("RENAME_COMMAND", "rename")
TOGGLE_VID = os.environ.get("TOGGLE_VID", "togglevid")
TOGGLE_DOC = os.environ.get("TOGGLE_DOC", "toggledoc")
RCLONE_COMMAND = os.environ.get("RCLONE_COMMAND", "rclone")
HELP_COMMAND = os.environ.get("HELP_COMMAND", "help")
SPEEDTEST = os.environ.get("SPEEDTEST", "speedtest")
TSEARCH_COMMAND = os.environ.get("TSEARCH_COMMAND", "tshelp")
MEDIAINFO_CMD = os.environ.get("MEDIAINFO_CMD", "mediainfo")
CAP_STYLE = os.environ.get("CAP_STYLE", "code")
BOT_NO = os.environ.get("BOT_NO", "")

#Bot Command [Token Utils]  >>>>>>>>>>>
UPTOBOX_TOKEN = os.environ.get("UPTOBOX_TOKEN", "")
EMAIL = os.environ.get("EMAIL", "mysterysd.sd@gmail.com")
PWSSD = os.environ.get("PWSSD", "S#D#97531")
GDRIVE_FOLDER_ID = os.environ.get("GDRIVE_FOLDER_ID", "0AN3LeVWuYvwEUk9PVA")
CRYPT = os.environ.get("CRYPT", "S3htTzl3aDdHUWdJWDhLZVV2MlpSVGlkZ0RVYU0xc29oQlNKSENGakRaOD0%3D")
#PHPSESSID = os.environ.get("PHPSESSID", "dslvec02r5mo3co40vsq6154eh")
HUB_CRYPT = os.environ.get("HUB_CRYPT", "dVAwSkpDU0FWVnNYV3hSZU40RkhrRU53RzVmdjVBbFd3RThPeFllMmhSND0%3D")
DRIVEFIRE_CRYPT = os.environ.get("DRIVEFIRE_CRYPT", "dVAwSkpDU0FWVnNYV3hSZU40RkhrRU53RzVmdjVBbFd3RThPeFllMmhSND0%3D")
KATDRIVE_CRYPT = os.environ.get("KATDRIVE_CRYPT", "WlFKUldtYWJzNmJlWkEvajRscmVrSjhJRm8yNXdDZklqYXpxd1AxQ0Zwcz0%3D; __gads=ID=d116cbcd46cd789b:T=1653563306:S=ALNI_Mb-QZgpbYcINdk3rhsqxydUNpVLeQ")
KOLOP_CRYPT = os.environ.get("KOLOP_CRYPT", "WlFKUldtYWJzNmJlWkEvajRscmVrSjhJRm8yNXdDZklqYXpxd1AxQ0Zwcz0%3D")
DRIVEBUZZ_CRYPT = os.environ.get("DRIVEBUZZ_CRYPT", "dVAwSkpDU0FWVnNYV3hSZU40RkhrRU53RzVmdjVBbFd3RThPeFllMmhSND0%3D")
GADRIVE_CRYPT = os.environ.get("GADRIVE_CRYPT", "dVAwSkpDU0FWVnNYV3hSZU40RkhrRU53RzVmdjVBbFd3RThPeFllMmhSND0%3D")
STRING_SESSION = os.environ.get("STRING_SESSION", "")

#Bot Command [IMDB]  >>>>>>>>>>>
CUSTOM_CAPTION = os.environ.get("CUSTOM_CAPTION", "")
MAX_LIST_ELM = os.environ.get("MAX_LIST_ELM", None)
DEF_IMDB_TEMPLATE = os.environ.get("IMDB_TEMPLATE", """<i><b>⚡𝐓𝐢𝐭𝐥𝐞: </b> {title}
<b>⚡𝐈𝐌𝐃𝐁 𝐑𝐚𝐭𝐢𝐧𝐠 :</b> <code>{rating} </code>
<b>⚡𝐐𝐮𝐚𝐥𝐢𝐭𝐲:  </b>
<b>⚡𝐑𝐞𝐥𝐞𝐚𝐬𝐞 𝐃𝐚𝐭𝐞: </b> {release_date}
<b>⚡𝐆𝐞𝐧𝐫𝐞: </b>{genres}
<b>⚡️𝐈𝐌𝐃𝐁: </b>{url}
<b>⚡𝐋𝐚𝐧𝐠𝐮𝐚𝐠𝐞:  </b>{languages}
<b>⚡𝐂𝐨𝐮𝐧𝐭𝐫𝐲: </b> {countries}
<b>⚡𝐒𝐮𝐛𝐭𝐢𝐭𝐥𝐞𝐬: </b>

<b>⚡𝐒𝐭𝐨𝐫𝐲 𝐋𝐢𝐧𝐞: </b><code>{plot}</code>

⚡️𝐉𝐨𝐢𝐧 𝐍𝐨𝐰 :  @FuZionX </i>

⚡️✅ 𝑪𝒍𝒊𝒄𝒌 𝑫𝒐𝒘𝒏 𝒂𝒏𝒅 𝑺𝒕𝒂𝒓𝒕 𝒕𝒉𝒆 𝑩𝒐𝒕 𝒕𝒐 𝑮𝒆𝒕 𝒕𝒉𝒆 𝑭𝒊𝒍𝒆 ✅ !! ⬇️ ⬇️""")

#Bot Command [Bot PM & Log Channel]  >>>>>>>>>>>
LEECH_LOG = os.environ.get("LEECH_LOG", "-1001569981856")
EX_LEECH_LOG = os.environ.get("EX_LEECH_LOG", "")
EXCEP_CHATS = os.environ.get("EXCEP_CHATS", "")
BOT_PM = os.environ.get("BOT_PM", "True")
SERVER_HOST = os.environ.get("SERVER_HOST", "Heroku")

# 4 GB Upload Utils >>>>>>>>>>>
PRM_USERS = os.environ.get("PRM_USERS", "1242011540 503170505")
PRM_LOG = os.environ.get("PRM_LOG", "-1001620169370")

# Bot Theme [ UI & Customization ] >>>>>>>>
BOT_THEME = os.environ.get("BOT_THEME", "fx-optimised")

BOT_START_TIME = time.time()

gDict = defaultdict(lambda: [])
user_settings = defaultdict(lambda: {})
gid_dict = defaultdict(lambda: [])
_lock = asyncio.Lock()

# Rclone Config Via Raw Gist URL & BackUp >>>>>>>>
try:                                                                      
    RCLONE_CONF_URL = os.environ.get('RCLONE_CONF_URL', "")              
    if len(RCLONE_CONF_URL) == 0:                                        
        RCLONE_CONF_URL = None                                           
    else:                                                                
        urllib.request.urlretrieve(RCLONE_CONF_URL, '/app/rclone.conf')  
except KeyError:                                                       
    RCLONE_CONF_URL = None                                              

if RCLONE_CONFIG:
    LOGGER.warning("[ATTENTION] Found RCLONE_CONFIG Var, Better Put your rclone.conf in Root Directory of Your Forked Repo")
if not os.path.exists("rclone.conf"):
    LOGGER.warning("No rclone.conf found in root directory")
if not os.path.exists("rclone_bak.conf"):  # Remake and BackUp rclone.conf file
    with open("rclone_bak.conf", "w+", newline="\n", encoding="utf-8") as fole:
        with open("rclone.conf", "r") as f:
            fole.write(f.read())
    LOGGER.info("[SUCCESS] rclone.conf BackUped to rclone_bak.conf!")


# Pyrogram Client Intialization >>>>>>>>>>>
app = Client("LeechBot", bot_token=TG_BOT_TOKEN, api_id=APP_ID, api_hash=API_HASH, workers=343)
isUserPremium = False
if len(STRING_SESSION) > 10:
    userBot = Client("Tele-UserBot", api_id=APP_ID, api_hash=API_HASH, session_string=STRING_SESSION)
    if userBot:
        userBot.start()
        if (userBot.get_me()).is_premium:
            isUserPremium = True
            LOGGER.info("[SUCCESS] Initiated UserBot : Premium Mode") #Logging is Needed Very Much
        else:
            isUserPremium = False
            LOGGER.info("[SUCCESS] Initiated UserBot : Non-Premium Mode. Add Premium Account StringSession to Use 4GB Upload. ")
    else: LOGGER.warning("[FAILED] Userbot Not Started. ReCheck Your STRING_SESSION, and Other Vars")
else: LOGGER.info("ReGenerate Your STRING_SESSION Var.")


updater = tg.Updater(token=TG_BOT_TOKEN)
bot = updater.bot
dispatcher = updater.dispatcher
