# メイン
from . import openai
import os
import json

# JSONファイルから設定を読み込む
with open("config.json") as f:
    config = json.load(f)

# API_KEYを設定する
OPENAI_API_KEY = config["openai_api_key"]

# 各Botの設定を取得する
for bot in config["bots"]:
    MODEL = bot["model"]
    PROMPT = bot["prompt"]
    TOKEN = bot["token"]

    bot = OpenAIDiscordBot(command_prefix="$", 
                           case_insensitive=True, 
                           intents=intents, 
                           openai_api_key=openai_api_key, 
                           model=model, 
                           prompt=prompt)

    # ここでBotを起動する処理を実装する
    bot.run(TOKEN)
