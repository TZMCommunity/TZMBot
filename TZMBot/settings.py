# -*- coding: utf-8 -*-

"""Settings for TZMBot."""
import os
from typing import List, Tuple

# The base dir is the root of the TZMBot application.
BASE_DIR: str = os.path.dirname(os.path.realpath(__file__))
# Database URL is a step above, in the media folder that can be managed separately.
DATABASE_URL: str = f"sqlite://{os.path.join(BASE_DIR, '..', 'media', 'db.sqlite')}"

# Logging setup for the app loggers.
LOGGING = {
    "version": 1,
    "formatters": {"default": {"format": "%(asctime)s - %(levelname)s - %(message)s"}},
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "default",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "DEBUG",
            "filename": os.path.join(BASE_DIR, "..", "debug.log"),
            "maxBytes": 1024 * 1024,
            "backupCount": 3,
            "formatter": "default",
        },
    },
    "loggers": {"__main__": {"level": "DEBUG", "handlers": ["console", "file"]}},
}

# A token associated with the discord bot.
TOKEN: str = os.environ.get("DISCORD_TOKEN", "")
# Developer member ids in a tuple that control if they can call the development commands.
DEV_IDS: Tuple[int] = (int(os.environ.get("DISCORD_DEV_ID", 0)),)
# If bot has any errors, output them in specific channels.
ERROR_CHANNEL_ID: int = int(os.environ.get("DISCORD_ERROR_CHANNEL", 0))
SAR_CHANNEL_ID = int(os.environ.get("DISCORD_SAR_CHANNEL", 0))
WELCOME_CHANNEL_ID = int(os.environ.get("DISCORD_WELCOME_CHANNEL", 0))

SAR_CONFIG = {
    649716342483845141: {
        "categories": {
            "Continents": {
                "1\u20e3": 568088763670986812,
                "2\u20e3": 568088828242427906,
                "3\u20e3": 568088763670986812,
                "4\u20e3": 623501823076073503,
            },
            "Areas": {
                "🔴": 568088763670986812,
                "🔵": 568088828242427906,
            },
            "Other": {
                "\u2764": 568088828242427906,
                "📚": 568088763670986812
            }
        }
    }
}

# A list of extensions to be loaded on bot init.
INIT_EXTENSIONS: List[str] = [
    "cogs.activity",
    "cogs.biography",
    "cogs.devtools",
    "cogs.error_handling",
    "cogs.loading",
    "cogs.sar",
]

EMBED_COLOURS: List[int] = [0x3FA84A, 0x26662C, 0x55E663, 0x5AF269, 0x4BCC58]
