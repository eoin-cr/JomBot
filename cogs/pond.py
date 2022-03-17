# pond.py
import discord
from discord.ext import commands
import random
import asyncio


class Pond(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("Pond initialised")

    @commands.command(name="hi")
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.member)
    async def hi(self, ctx):
        await ctx.send("Hi!")

    @commands.command(name="manage_messages_check")
    @commands.has_guild_permissions(manage_messages=True)
    async def manage(self, ctx):
        await ctx.send("You have manage messages perms!")

    # Code from when groovy was still a thing and would announce whenever
    # it dced from the vc
    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.author.id == 234395307759108106:
            voice_state = ctx.member.voice
            await asyncio.sleep(5)

            # If it's not in a voice channel and sends a message, delete it
            # and give out to it
            if voice_state is None:
                await ctx.send('Shut the fuck up groovy')
                return await ctx.remove

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild is not None and message.guild.id == 829349685667430460:
            # Checks if a message was sent in the introductions channel
            if message.channel.id == 830565670805962822:
                role1 = discord.utils.get((await message.guild.fetch_roles()), name='tadpoles')
                role2 = discord.utils.get((await message.guild.fetch_roles()), name='froglet')
                role3 = discord.utils.get((await message.guild.fetch_roles()), name='froggers')

                # If a user has any of the 3 roles, ignore their message
                if role1 in message.author.roles or role2 in message.author.roles or role3 in message.author.roles:
                    print("ignoring")

                # Otherwise, give them the tadpole role so they can speak
                else:
                    ch = message.guild.get_channel(829349688197120052)
                    # print(message.guild.roles)
                    await message.author.add_roles(role1)
                    # await message.author.add_roles(message.author, role)
                    return await ch.send(f"Welcome to the pond {message.author.mention}")

            if message.mention_everyone:
                return await message.channel.send("This seems important <:flosh:701774266894647338>")

            # Doesn't work as a command as it would need a prefix which is cringe
            # Checks if in right server, and if perms are correct
            if message.content.startswith("🦶") and len(
                    message.content.split(' ')) == 2 and message.author.guild_permissions.kick_members:
                # Splits message content
                cont = message.content.split(' ')

                # Removes characters from tag to get user id
                auth = int(cont[1].strip('@,<>,!'))

                # Fetches member
                memb = await message.guild.fetch_member(auth)

                # Checks if you tagged yourself
                if message.author.id == auth:
                    return await message.channel.send("You can't kick yourself I'm afraid!")

                # Otherwise, kicks them
                await memb.kick(reason="You were inactive and have been footed")
                return await message.channel.send("Goodbye goofball <:pixellice:829423250361679922>")

    @commands.command(name="Q", help="Formats Jom's questions")
    async def Q(self, ctx, *, cont):
        # Checks if I sent the message and if it's in the right server
        if ctx.message.author.id == 484444017489084416 and ctx.message.guild is not None and \
                ctx.message.guild.id == 829349685667430460:
            # Splits message at newlines
            split = cont.split('\n')

            # Formatting stuff
            for i in range(len(split)):
                if split[i].startswith("Q"):
                    split[i] = split[i].replace(".", ":", 1)
                elif '/' not in split[i]:
                    split[i] = f"- {split[i]}"

            # Sets question channel
            qs_channel = message.guild.get_channel(834198286310047784)
            #             qs_channel = ctx.message.guild.get_channel(829358413065486376)

            # Undoes the earlier newline split and sends message
            joined = '\n'.join(split)
            full_message = str(f"```yaml\n{joined} \n```")
            return await qs_channel.send(full_message)

    @commands.command(name="jomwheel", help="Spins the jomwheel")
    async def jomwheel(self, message, *arg):
        if arg[1] == 's':
            # Opens file, picks a random num, and selects that voice line
            with open("wheel_speak.txt", "r") as file:
                lines = file.readlines()
                for line in lines:
                    wheel_speak = line.split(", ")
            num = random.randint(0, 6)
            await message.channel.send("*clickclickclickclick1*")
            return await message.channel.send(wheel_speak[num])
        else:
            with open("wheel.txt", "r") as file:
                lines = file.readlines()
                for line in lines:
                    wheel = line.split(", ")
            num = random.randint(0, 6)
            await message.channel.send("*clickclickclickclick*")
            return await message.channel.send(wheel[num])

    @commands.command(name="reply", help="Replies to your message")
    async def reply(self, ctx):
        return await ctx.reply('Hello')

    # Prints a message to the terminal - handy for getting emoji ids and the like
    @commands.command()
    async def print(self, *message):
        string = ' '.join(message)
        print(string)

    #         return print(message)

    @commands.command(name="short", help="ha")
    async def short(self, ctx):
        return await ctx.send("Ha lark is short")

    @commands.command(name="introduce", help="Introduces someone")
    async def introduce(self, ctx):
        return await ctx.send("""Hey there and welcome to the server!
Be sure to answer the questions in <#830565670805962822> and then check
out <#830565732001644555> and <#830565778654887958> for more information!
Also when enabled I will delete every message containing sus, vented, etc.
So if your messages are getting removed, that might be why""")

    @commands.command(name="test", help="Sends a test embed")
    async def test(self, message):
        embed = discord.Embed(title="testing", url="https://google.com", description="test", color=discord.Color.blue())
        embed.set_author(name=message.author.display_name, url="https://bing.com", icon_url=message.author.avatar_url)
        embed.add_field(name="field 2", value="testing 2", inline=False)
        embed.set_footer(text="Test")
        embed.set_thumbnail(
            url="https://3.bp.blogspot.com/-vdcxPhqYdWM/UTSJzMfhUlI/AAAAAAAACyU/Vp5x5zqjf84/s1600/smiley-facess.jpg")
        await message.channel.send(embed=embed)
        return

    # Lists invites, used it for debugging something before
    @commands.command()
    async def ls(self, ctx, message):
        if message == "invites":
            invite_list = await ctx.guild.invites()
            for i in range(0, len(invite_list)):
                print(invite_list[i].uses)

    # Secret command that doesn't do anything at all :)
    @commands.command(name="send")
    async def send(self, ctx, *message):
        # Checks channel id
        if ctx.channel.id == 824766240589086761:
            # Gets specific channel
            general = self.bot.get_channel(829349688197120052)

            # Joins tuple into single message
            message = ' '.join(map(str, message))

            # Sends message to channel
            await general.send(message)

    @commands.command(name="alias", help="alias")
    async def alias(self, message):
        # open text file in read mode
        text_file = open("words.txt", "r")
        # read whole file to a string
        words = text_file.read()

        # Picks a random sentence length from 3 to 10 words.
        loop_num = random.randint(3, 10)
        sentence = ""
        if words is not None:
            words = words.split('\n')
            for x in range(loop_num):
                # Randomly selects a word and adds it to the sentence
                index = random.randint(0, 466452)
                sentence = sentence + words[index] + " "
            # Sends message
            await message.channel.send(sentence)
            return
        else:
            response = "Uh oh there's been a fucky wucky"
            await message.channel.send(response)
            return


def setup(bot):
    bot.add_cog(Pond(bot))
