import gpt_2_simple as gpt2
from discord.ext import commands
import re


class Sentient(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("Sentient initialised")
        self.sess = None

    @commands.command(name="complete", help="Generates text from the GPT-2 model")
    async def complete(self, ctx, *, text):
        if not self.sess:
            self.sess = gpt2.start_tf_sess()
        else:
            self.sess = gpt2.reset_session(self.sess)

        gpt2.load_gpt2(self.sess)
        async with ctx.typing():
            # blocking async is bad but i simply do not care
            text = gpt2.generate(self.sess, prefix=text, return_as_list=True)
            print(text)
        # Remove emoji-only lines
        text = [l for l in text[0].split("\n") if not re.match(r"^:.*:$", l)][:20]
        # Remove backticks
        text = "\n".join(text).replace("`", "")[:1990]
        await ctx.send("```\n" + text + "```")


async def setup(bot):
    await bot.add_cog(Sentient(bot))
