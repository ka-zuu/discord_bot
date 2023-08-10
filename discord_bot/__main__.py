# メイン
import asyncio
from . import openai
import os
import json

# JSONファイルから設定を読み込む
with open("config.json") as f:
    config = json.load(f)

# API_KEYを設定する
OPENAI_API_KEY = config["openai_api_key"]


# Botを起動する非同期関数
async def run_bot(bot_conf):
    MODEL = bot_conf["model"]
    PROMPT = bot_conf["prompt"]
    TOKEN = bot_conf["token"]

    bot = openai.OpenAIDiscordBot(
        openai_api_key=OPENAI_API_KEY, model=MODEL, prompt=PROMPT
    )

    # ここでBotを起動する処理を実装する
    await bot.start(TOKEN)


# 各Botの設定を取得し、非同期で実行する
loop = asyncio.get_event_loop()
tasks = [run_bot(bot_conf) for bot_conf in config["bots"]]
loop.run_until_complete(asyncio.gather(*tasks))
