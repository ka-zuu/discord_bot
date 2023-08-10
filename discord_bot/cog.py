from discord.ext import commands
import requests

# コグとして用いるクラスを定義。
class Cog(commands.Cog):

    # Cogクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot

    # コマンドの作成。コマンドはcommandデコレータで必ず修飾する。
    @commands.command()
    async def ping(self, ctx):
        try:
            global_ip = requests.get('https://api.ipify.org').text
            await ctx.send(f'実行サーバのグローバルIPアドレスは {global_ip} です')
        except Exception as e:
            await ctx.send(f'エラーが発生しました: {e}')

# Bot本体側からコグを読み込む際に呼び出される関数。
def setup(bot):
    # TestCogにBotを渡してインスタンス化し、Botにコグとして登録する。
    bot.add_cog(Cog(bot))