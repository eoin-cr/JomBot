# IP.py
from discord.ext import commands, tasks
import requests


# import subprocess


class WOTD(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("Word of the day initialised")
        self.old_ip = ""

    # Creates a task loop that runs every 60 seconds to check if the IP
    # has changed
    @tasks.loop(hours=24)
    async def send_wotd(self, message):
        merriam_request = requests.post("https://www.merriam-webster.com/word-of-the-day").text
        idx_start = merriam_request.find("<h1>")
        idx_end = merriam_request.find("</h1>")
        word = merriam_request[idx_start + 4:idx_end]
        word_type = None

        if "<span class=\"main-attr\">verb</span>" in merriam_request:
            word_type = "verb"

        if word_type == "verb":
            def_start = merriam_request.find(f"<em>{word}</em>")
        else:
            def_start = merriam_request.find(f"<em>{word.capitalize()}</em>")
        # print(merriam_request[def_start:])
        def_end = merriam_request.find("</p>", def_start)
        definition = merriam_request[def_start + 10 + len(word):def_end]
        # print(f"definition: {definition}")

        await message.channel.send(f'Hello everyone!\nToday\'s word of the day is: {word}.\n{word.capitalize()}'
                                   f' {definition}')

    # Command to display IP
    @commands.command(name='word_of_the_day_start', aliases=['wotd_start', 'start_wotd', 'wotd-start',
                                                             'start-wotd'], hidden=True)
    async def start_word_of_the_day(self, message):
        await message.channel.send("Word of the day has started!")

        # Only tries start the loop if it's not already running to prevent
        # issues
        if not self.send_wotd.is_running():
            self.send_wotd.start(message)

    @commands.command(name='word_of_the_day_stop', aliases=['wotd_stop', 'stop_wotd', 'wotd-stop',
                                                                'stop-wotd'], hidden=True)
    async def stop_word_of_the_day(self, message):
        if self.send_wotd.is_running():
            self.send_wotd.cancel()
            return await message.channel.send('Word of the day stopped.')
        else:
            return await message.channel.send('Word of the day is not running.')


def setup(bot):
    bot.add_cog(WOTD(bot))
