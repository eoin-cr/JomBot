from discord.ext import commands
from google.cloud import translate_v2 as translate
import six
import bot as main

# makes a request to the google translate API, and returns the translated
# text.
def translate_text(target, text):
    """Translates text into the target language.

    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """

    translate_client = translate.Client()

    if isinstance(text, six.binary_type):
        text = text.decode("utf-8")

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(text, target_language=target)

    # print(u"Text: {}".format(result["input"]))
    # print(u"Translation: {}".format(result["translatedText"]))
    return result["translatedText"]
    # print(u"Detected source language: {}".format(result["detectedSourceLanguage"]))


class Translate(commands.Cog):
    def __init__(self, bot):
        print("Translate initialised")
        # self.translator = Translator()

    @commands.command(name="translate", help="Translate the message that "
                                             "you're replying to into English")
    async def translate(self, ctx):
        reply_message = ctx.message.reference.resolved.content
        # calls the google translate function
        translated = translate_text('en', reply_message)
        embed = main.embed_func(ctx, "Translate", f"The translated text means: {translated}")
        await ctx.message.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Translate(bot))
