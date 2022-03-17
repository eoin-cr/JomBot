# JomBot

Does stuff and things.

<sup><sub>Aha oops didn't mean to wipe the entire repo rip all my commits</sub></sup>

---

Default prefix: !

Features:
* Can set role upon new user messaging a selected channel (and then welcome them
to the server)
* Music player with queue and seek functionality
* Can keep track of different user's timezones
* Can generate wordles for you to play
* Can tell you the IP of the server it's hosted on and let you know when it changes
  (useful if you're self hosting and don't have a static domain)
* Crypto trading simulator using real time prices from the cryptocompare API

---

[Discord.py documentation](https://discordpy.readthedocs.io/en/stable/)

Just a word of advice for anyone looking to build their own bot from scratch—use cogs
and proper commands as soon as possible.  Whilst stuff like `if message.content.lower()
== 'command'` is easier than actually looking at the proper way to do it, when you inevitably
have to switch to the proper way to do it, it's very annoying to have to rewrite a huge
amount of your code.

If you don't know anything about discord bots and are looking at this repo and curious as to how
it works I'll give a quick overview of the command layout and stuff.  Cogs are just different sections
of code split into different files.  For example my song.py cog just has all the music commands and
the like.  Having files laid out like this makes it much easier to debug code and find code you're
looking for.  When you go into a cog you will see
```py
class Pond(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("Pond initialised")
```
this is just initialising the Pond class, which hosts most of the commands in that cog.  This
class is later added to the bot with
```python
def setup(bot):
    bot.add_cog(Pond(bot))
```
and then we add it to the main bot.py file with `bot.load_extension("cogs.pond")`.  

Back in the
pond cog you will see functions like this
```python
 @commands.command(name="reply", help="Replies to your message")
    async def reply(self, ctx):
```
Here the way you will call this command in discord is by doing `!reply` (`!` is the default prefix).
The way you call this command is either set with the `name="..."` in the commands.command function,
or if there is no name declaration in the commands.command function, it will simply be called with
the name set in `async def ...():`.

You can also add more checks to functions.  For example:
```python
    @commands.command(name="hi")
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.member)
    @commands.has_guild_permissions(manage_messages=True)
    @pond_check()
    async def hi(self, ctx):
        await ctx.send("Hi!")
```
(pond_check is a custom check).  Here this function is called with `!hi`, and can only be called
once every 5 seconds, and the user must have manage_messages perms, and the message must be sent
in the pond.  Take a look at the docs if you want some more examples.  Also note that every function
must by `async`ed and then messages must be `await`ed. 