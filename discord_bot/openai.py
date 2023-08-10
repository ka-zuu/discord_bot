# OpenAIとやり取りするDiscord Botクラス

from discord.ext import commands
import discord
import openai
import os
import requests

# クラスを作成
class OpenAIDiscordBot(commands.Bot):
    def __init__(self, openai_api_key, model, prompt):
        self.openai_api_key = openai_api_key
        self.model = model
        self.prompt = prompt

        # OpenAIのAPIキーを設定
        openai.api_key = self.openai_api_key

        # Discord Botの設定
        intents = discord.Intents.default()
        intents.typing = False  # typingを受け取らないように
        intents.message_content = True

        super().__init__(
            command_prefix="$",  # $コマンド名　でコマンドを実行できるようになる
            case_insensitive=True,  # コマンドの大文字小文字を区別しない
            intents=intents,  # 権限を設定
    )

    # ログインしたらターミナルにログイン通知が表示される
    async def on_ready(self):
        print(f"We have logged in as {self.user}")

    # Botにメンションをした場合、OpenAIに問い合わせる
    async def on_message(self, message):
        if message.author == self.user:
            return

        if self.user in message.mentions:
            # typingを表示
            async with message.channel.typing():
                # 会話履歴を初期化
                conversations = [{"role": "system", "content": self.prompt}]
                # メッセージを会話履歴に追加
                conversations.insert(1, {"role": "user", "content": message.content})

                # メッセージが返信か再帰的に確認し、返信元のメッセージをすべて会話履歴に追加
                while message.reference:
                    message = await message.channel.fetch_message(message.reference.message_id)
                    # 返信がBotの場合はrole:assistant、ユーザーの場合はrole:userとして会話履歴に追加
                    if message.author == self.user:
                        conversations.insert(1, {"role": "assistant", "content": message.content})
                    else:
                        conversations.insert(1, {"role": "user", "content": message.content})

                # OpenAIに問い合わせ
                response = openai.ChatCompletion.create(
                    model=self.model,
                    messages=conversations,
                    max_tokens=2048,
                    temperature=0.8,
                )

            await message.reply(response.choices[0]["message"]["content"])

        await self.process_commands(message)