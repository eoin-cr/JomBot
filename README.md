# JomBot

Does stuff and things.

<sup><sub>Aha oops didn't mean to wipe the entire repo rip all my
commits</sub></sup>

---

# Features:

- Can set role upon new user messaging a selected channel (and then welcome them
  to the server)
- Music player with queue and seek functionality
- Can keep track of different user's timezones
- Can generate wordles for you to play
- Can tell you the IP of the server it's hosted on and let you know when it
  changes (useful if you're self hosting and don't have a static domain)
- Crypto trading simulator using real time prices from the cryptocompare API
- Added implementation of MEE6 level system

Default prefix: `!`

---

# Added in this commit:

Added machine learning algorithm to determine the difference between one type
of image and all other images (sorry alex).  Made a python file for training
the model, and then a separate one to be used in the bot.  This means the
model does not have to be re-trained every single time the bot starts, which
is very time consuming, for very little benefit.  I plan to save all the other
models in a similar fashion in the future.

---

# Self-hosting JomBot

[Article on creating a bot token](https://www.writebots.com/discord-bot-token/)

Once you have your token, download the JomBot repo and unzip it. Create a file
called just `.env` with the layout

```
# .env
DISCORD_TOKEN=INSERT YOUR DISCORD TOKEN HERE
```

and put the file in the same directory as the bot.py file.

Now you have to download all the libraries required. To do that run the command

```python
pip install -r requirements.txt
```

Then for the sentiment analyser normalisation function you'll need to run

```python
python -m spacy download en_core_web_sm
```

And then install ffmpeg on whatever version of linux you're using. For Ubuntu
the command is
```python
sudo apt install ffmpeg
```

Then to run the bot you'll want to simply run `python3 bot.py` and it should be
working. Note that the bot will only be running for as long as your terminal is
open, so I'd recommend using tmux to create terminal instances so it will be
running as long as your computer is on. I believe there are also some free cloud
hosting options you could use to host the bot instead of leaving your computer
on all the time.

NOTE: Whilst most of the functionality should work out of the box, there are
several commands that will only run on certain servers. Change the id the
command looks for in code to the id of your server/channel.

### Running the translate feature

The translate feature uses Google's translate API. You can see the prices for
that [here](https://cloud.google.com/translate/pricing?hl=en_US). It's free for
under 500k chars translated per month. If you are self-hosting, create an
account and then take a look at the 
[documentation](https://cloud.google.com/translate/docs/basic/translating-text).
In my experience, getting the translate feature running via Pycharm's run
option is far more annoying than just doing it through the terminal. I'd
recommend just getting the JSON key and then placing 
`export GOOGLE_APPLICATION_CREDENTIALS="[/place/in/system/key.json]` in your
bash/zshrc. Then the program should work fine.

---

# NOTE:

The contents in the sample sets are NOT my own opinions.  These sample sets
have been scraped from various places, and may contain content that some users
find offensive. A sample set will be created to try and automatically prevent
transphobia on a server, so that sample set will contain transphobic things,
which are absolutely not my own opinions, and I strongly condemn transphobia
of any sort.

---

# Building your own bot

[Discord.py documentation](https://discordpy.readthedocs.io/en/stable/)

Just a word of advice for anyone looking to build their own bot from scratch—use
cogs and proper commands as soon as possible. Whilst stuff like
`if message.content.lower() == 'command'` is easier than actually looking at the
proper way to do it, when you inevitably have to switch to the proper way to do
it, it's very annoying to have to rewrite a huge amount of your code.

If you don't know anything about discord bots and are looking at this repo and
curious as to how it works I'll give a quick overview of the command layout and
stuff. Cogs are just different sections of code split into different files. For
example my song.py cog just has all the music commands and the like. Having
files laid out like this makes it much easier to debug code and find code you're
looking for. When you go into a cog you will see

```py
class Pond(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("Pond initialised")
```

this is just initialising the Pond class, which hosts most of the commands in
that cog. This class is later added to the bot with

```python
def setup(bot):
    bot.add_cog(Pond(bot))
```

and then we add it to the main bot.py file with
`bot.load_extension("cogs.pond")`.

Back in the pond cog you will see functions like this

```python
 @commands.command(name="reply", help="Replies to your message")
    async def reply(self, ctx):
```

Here the way you will call this command in discord is by doing `!reply` (`!` is
the default prefix). The way you call this command is either set with the
`name="..."` in the commands.command function, or if there is no name
declaration in the commands.command function, it will simply be called with the
name set in `async def ...():`.

You can also add more checks to functions. For example:

```python
    @commands.command(name="hi")
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.member)
    @commands.has_guild_permissions(manage_messages=True)
    @pond_check()
    async def hi(self, ctx):
        await ctx.send("Hi!")
```

(pond_check is a custom check). Here this function is called with `!hi`, and can
only be called once every 5 seconds, and the user must have manage_messages
perms, and the message must be sent in the pond. Take a look at the docs if you
want some more examples. Also note that every function must by `async`ed and
then messages must be `await`ed.

---

# Commands list

All required values will be in square brackets, any optional values will be in
round brackets. Any commands that will not run if you invite the bot to your
server will be indicated with an asterisks in front of the prefix.

### Control

This cog will be responsible for controlling some of the functionality of the
bot on different servers. At the moment it just controls the custom prefix
stuff.

```python
!set-prefix/set_prefix [prefix]
```

- Sets a custom prefix for JomBot on your server

```python
!prefix
```

- Displays the currently set prefix for JomBot on your server

```python
!del-prefix
```

- Deletes your custom prefix and reverts it back to the default—`!`

---

### Crypto

The crypto cog was built after someone who was interested in crypto asked for a
crypto simulator they could use to practice. This cog uses real time current and
historic data from the cryptocompare API. JomBot will store your coins in a
personal wallet.

```
!price [coin]
```

- Displays information about the price of a certain coin

```
!chelp
```

- Displays a little help embed

```
!cbuy [coin] [amount/all]
```

- Buys a certain amount of a coin with USD

```
!csell [coin] [amount/all]
```

- Sells a certain amount of a coin for USD

```
!wallet (user)
```

- Displays the wallet of a user, if left blank will display your own wallet

---

### HH

This cog was custom built for a certain server. It tracks the amount of messages
each user sends and gives a regular role if a user sends more than a certain
amount of messages each week. By default this is disabled, however, you can
enable it if you have manage server perms.

```python
!enable-regular/enable-weekly-messages/enable-weekly/enable_regular/enable_weekly_messages/enable_weekly/enable_weekly_message_counter [regular role name] (messages required for regular role (default is 125))
```

- Tracks the messages for the last 7 days. If a user exceeds the amount of
  messages required to get the regular role it will be given to them. If a user
  with the role does not meet the amount of messages required, the role will be
  removed. Requires manage server perms to enable

```python
!disable-regular/disable-weekly-messages/disable-weekly/disable_regular/disable_weekly_messages/disable_weekly/disable_weekly_message_counter
```

- Disables the message tracker. Requires manage server perms to disable

```python
!vibe-check/vibe_check [@user]
```

- Prints how good the vibes of a user are

### IP

This cog provides an easy way to get the IP of the device you are hosting the
bot on. This can be helpful if you are self-hosting on a server has a dynamic
IP, which is on a different network than you are currently on. Obviously this
command will only work for me, but if you are self hosting the bot you'll be
able to change which users are able to call the command.

```python
*!send_ip
```

- sends the current IP of the server hosting the bot

---

### Netsoc

Although this cog was originally just custom build for UCD Netsoc's Discord
server, I have expanded the functionality so it can be used on every server
(after being enabled by a user with manage server perms). This project was built
using the
[MEE6](https://github.com/Mee6/Mee6-documentation/blob/master/docs/levels_xp.md)
level
up/[XP](https://www.reddit.com/r/discordapp/comments/60z1eg/mee6_bot_levelling_system/)
system. The functionality is disabled by default.

```python
!enable-level/enable-levelling/enable-levels/enable_level/enable_levelling/enable_levels (level up message channel)
```

- Command which enables the level up system. The level up channel is the channel
  in which the bot will post messages informing users they have levelled up. If
  no channel is given, JomBot will use the channel the command to enable the bot
  was sent in. Requires manage guild perms

```python
!disable-level/disable-levelling/disable-levels/disable_level/disable_levelling/disable_levels
```

- This command disables the level up system. Requires manage guild perms

---

### Pond

This cog is custom build for a different server. However, quite a few of the
commands will run universally.

```python
!manage_messages_check
```

- Check which will tell you if you have manage message perms on a server

```python
*🦶 [user]
```

- Kicks a user

```python
*!jomwheel spin (s)
```

- Imitates a user by printing a message from a list of messages

```python
!reply
```

- Replies to your message. Good way of just checking if the bot is working.

```python
*!introduce
```

- Prints an introduction message to welcome someone who joined and give them a
  little information about the server

```python
!test
```

- Sends a test embed

```python
*!alias
```

- Sends a random list of words to imitate a user

```python
*!disable_introductions/disable-introductions
```

- On the server this was created for, a user cannot speak unless they send a
  message in an introductory channel first. Upon sending a message there a
  speaking role is automatically granted. This command turns off the function
  which automatically grants a speaking role upon sending a message in the
  introduction channel to prevent raids and the like

```python
*!enable_introductions/enable-introductions
```

- Enables the functionality that automatically grants speaking perms upon
  messaging the intro channel

---

### Sentiment

This cog was created after some people requested a system to automatically
filter people based on political beliefs—specifically their opinions towards
billionaires.  NOTE: The opinions in `Billionaire_samples.csv` are not my own,
they are just a wide range of different opinions gathered from people and
manually sorted by pro/anti-billionaire sentiment.

```python
!analyse [sentence]
```

- Analyses a sentence and determines whether it has a pro or anti billionaire
  sentiment


### Song

This cog is a youtube music player.

```python
!join/j
```

- Joins the voice channel you are currently in

```python
!leave/dc
```

- Leaves the voice channel you are currently in

```python
!play/p [title/youtube url]
```

- Adds a song to the queue

```python
!pause
```

- Pauses the song

```python
!resume
```

- Resumes the song

```python
!queue/q
```

- Displays the queue

```python
!raw_queue
```

- Displays the raw queue (only useful for debugging)

```python
!skip
```

- Skips the currently playing song

```python
!seek [time in seconds]
```

- Seeks to a certain part of the currently playing song

```python
!current
```

- Displays the name of the currently playing song

```python
!remove/r/rm/del/delete [number in queue]
```

- Removes a song from the queue

```python
!move/m/mv [old position in queue] [new position in queue]
```

- Moves a song in the queue

---

### Time

Cog which keeps track of people's timezones. The option display certain
countries timezones will not be accurate for everyone, as for example the
`!time US` command is just for `UTC-8`, because that's the only one needed on my
server. However, the option to set certain user's timezones should always be
accurate (apart from when the user goes into daylight savings time. The server
I'm hosting it on is at UTC+0 and is not affected by DST). Remember, if you are
self hosting, you will have to change the time the server thinks you're at, as
the code assumes you're hosting from UTC+0

```python
!time [us/america/uk/england/ireland/serbia/canada]
```

- Displays some times in certain timezones in certain countries

```python
!time [user]
```

- Displays the time it currently is for a certain user

```python
!set-time (user) [UTC+/-X]
```

- Sets the timezone of a user or yourself.

---

### Translate

This utilises the Google translate API in order to detect what language a
message was sent in, and then convert it to English. If you've invited
JomBot to your server rather than self-hosting, please don't go overboard
with the amount of characters translated, as otherwise I will be charged and
simply disable this functionality globally.

```python
!translate
```

- This command is different from most others, as rather than translating
the text after the command, instead, it translates the text in the
*message you are replying to*.  If you do not reply to a message this command
will not work.

---

### Wordle

Wordle is a word game where you have to guess a certain 5 letter word. If a
letter is not in the answer it will show up grey, if it is in the answer but in
a different position it will show up yellow, and if it is in the answer in the
correct position it will show up green. You can play the original game
[here](https://www.nytimes.com/games/wordle/index.html). You can also play
wordles with JomBot.

```python
!wordle start
```

- Starts a wordle game (NOTE: Only one person can play at a time to avoid
  confusion)

```python
!wordle [guess]
```

- Guesses a word

```python
!extend
```

- There is a time limit imposed so a user doesn't start a game and never finish
  it, blocking it for everyone else. However, if you are halfway through a game
  and still thinking when the bot tells you your time is running low, you can
  simply do this command to extend your time

```python
!quit
```

- Quits your current wordle game
