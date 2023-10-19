# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# Please read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >.

from asyncio import Lock
from threading import local

class Threads(local):
    pass

locks = Threads()

locks._GCAST_LOCKED = _GCAST_LOCKED = set()
locks._GUCAST_LOCKED = _GUCAST_LOCKED = set()
locks._GBAN_LOCKED = _GBAN_LOCKED = set()
locks._UNGBAN_LOCKED = _UNGBAN_LOCKED = set()
locks._INVITED_LOCKED = _INVITED_LOCKED = set()
locks._KICKED_LOCKED = _KICKED_LOCKED = set()

locks._HELP_ACCEPT = _HELP_ACCEPT = set()
locks._HELP_LOCK = _HELP_LOCK = Lock()

locks.SETMODE_ONLINE = SETMODE_ONLINE = set()
locks.SETMODE_OFFLINE = SETMODE_OFFLINE = set()

LOCK_TYPES: dict = {
    "all": "Everything.",
    "messages": "Text, contacts, locations and venues.",
    "media": "Audio files, documents, photos, videos, video notes and voice notes.",
    "others": "Stickers, games, gifs, inline.",
    "links": "Web priview.",
    "polls": "Polling.",
    "info": "Change info.",
    "invite": "Invite users.",
    "pin": "Pinned messages.",
}

_CHARACTER_NAMES = {
    "`": "",
    "*": "",
    "_": "",
    "-": "",
    "~": "",
    "/": "",
    "|": "",
    "[": "",
    "]": "",
    "<": "",
    ">": "",
    "'": "",
    "{": "",
    "}": "",
    ")": "",
    "(": "",
    "’": "",
    "‘": "",
    "=": "",
    "#": "",
    "&": "",
    "+": "",
    "^": "",
    "%": "",
    "°": "",
    ";": "",
    ":": "",
    "?": "",
    "!": "",
    "@": "",
    "¡": "",
    "¿": "",
    "‽": "",
    "♪": "",
    "±": "",
    '″': '',
    "‚": "",
    ".": "",
    "№": "",
    "—": "",
    "–": "",
    "·": "",
}

SIZE_UNITS = [
    "B",
    "KB",
    "MB",
    "GB",
    "TB",
    "PB",
    "EB",
]

OUT_AFK = [
    "Is Alive !!",
    "Is Here !!",
    "Is Back !!",
    "Is Awake !!",
    "Is Awakening !!",
    "Is Online !!",
    "Is Active !!",
    "Is Finally Here !!",
    "Well Done !!",
    "No Longer AFK !!",
    "Is Coming !!",
    "No Longer Offline !!",
    "Back Again !!",
]
