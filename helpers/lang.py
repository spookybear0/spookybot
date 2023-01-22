from typing import Dict, List
from helpers.command import Context
from helpers.models import User
from helpers.logger import logger
import json
import os

class LanguageManager:
    def __init__(self) -> None:
        self.language_pack: Dict[str, Dict[str, str]] = {}
        self.default = "en"

    def load_language_packs(self) -> None:
        logger.info("Loading language packs...")

        path = os.path.dirname(os.path.realpath(__file__)).replace("helpers", "")

        for file in os.listdir(f"{path}lang"):
            if file.endswith(".json"):
                with open(f"{path}/lang/{file}", "r") as f:
                    self.language_pack[file.replace(".json", "")] = json.load(f)

    async def get(self, ctx: Context, key: str, *args) -> str:
        user = await User.get_or_none(name=ctx.username) 

        if user is None:
            lang = self.default
        else:
            lang = user.language

        return self.language_pack[lang][key].format(*args)