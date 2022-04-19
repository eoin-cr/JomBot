from discord.ext import commands
from PIL import Image


class Images(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("Image initialised")

    @commands.command(name="trans", alias="transify", help="overlays the trans"
                                                           " flag on an image")
    async def trans(self, ctx):
        print("hello")
        # background = Image.open("resources/trans.png")
        foreground = ctx.message.attachments[0].url

        # print("Hi")
        print(foreground)
        # background.paste(foreground, (0, 0), foreground)
        # foreground.show()
        # background.show()


def setup(bot):
    bot.add_cog(Images(bot))
