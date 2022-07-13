import gpt_2_simple as gpt2
# import discord
from discord.ext import commands
# import tensorflow as tf


class Sentient(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("Sentient initialised")
        self.sess = None

    @commands.command(name="complete", help="Generates text from the GPT-2 model")
    async def complete(self, ctx, *, text):
        # tf.reset_default_graph()

        if not self.sess:
            self.sess = gpt2.start_tf_sess()
        else:
            self.sess = gpt2.reset_session(self.sess)

        gpt2.load_gpt2(self.sess)

        text = gpt2.generate(self.sess, prefix=text, return_as_list=True)
        text_to_send = ""
        print(text)
        i = 0
        text = text[0].split("\n")
        while i < len(text) and i < 20:
            # for i in range(20):
            text_to_send += text[i] + "\n"
            i += 1

        print(text_to_send[:1999])
        await ctx.send(text_to_send[:1999])


def setup(bot):
    bot.add_cog(Sentient(bot))
