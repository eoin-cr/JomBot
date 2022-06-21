import json
import discord
import re
# import string
# import matplotlib.pyplot as plt
# import numpy as np
# import pandas as pd
# import pkg_resources
# import spacy
from discord.ext import commands
# from keras.layers import Embedding
# from keras.layers import LSTM, Dense, Dropout, SpatialDropout1D
# from keras.models import Sequential
from keras_preprocessing.sequence import pad_sequences
# from keras_preprocessing.text import Tokenizer
# from symspellpy.symspellpy import SymSpell, Verbosity
# from tensorflow import keras
# from tqdm import tqdm
import tensorflow as tf
from bot import embed_func
# import string


def pond_check():
    def predicate(ctx):
        return ctx.guild.id == 829349685667430460

    return commands.check(predicate)


trans_model = tf.keras.models.load_model('models/trans')
billionaire_model = tf.keras.models.load_model('models/billionaire')


def predict_sentiment(text, i):
    tx = tokenizer_arr[i].texts_to_sequences([text])
    tx = pad_sequences(tx, maxlen=700)
    prediction = int(model_arr[i].predict(tx).round().item())
    # print("Predicted label: ", sentiment_label[1][prediction])
    return sentiment_label_arr[i][1][prediction]


class Sentiment(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        global tokenizer_arr
        tokenizer_arr = [None, None]
        global model_arr
        model_arr = [None, None]
        global sentiment_label_arr
        sentiment_label_arr = [None, None]
        global samples_arr
        samples_arr = ['Billionaire_samples.csv', 'trans_samples.csv']
        train(0, 5)
        train(1, 50)
        self.invites_disabled = False
        print("Sentiment analysis initialised")

    @commands.command(name="analyse", help="Performs sentiment analysis")
    async def analyse(self, ctx, *, text):
        # text_str = ' '.join(text).replace("'", "")
        text_str = remove_punctuation(cleanemojis(text)).replace("\n", "")
        sentiment = predict_sentiment(text_str, 0)
        # sentiment = 1
        if sentiment == 1:
            string = "anti billionaire"
        else:
            string = "pro billionaire"

        emojis = ['✅', '❌']
        embed = embed_func(ctx, "Sentiment analysis", f"Following my analysis it appears your string \"{text_str}\" "
                                                      f"has {string}"
                                                      f" sentiment")
        message = await ctx.send(embed=embed)
        for emoji in emojis:
            await message.add_reaction(emoji)

    @commands.command(name="analyse_t", alias="tranalyse", help="Performs sentiment analysis")
    async def analyse_t(self, ctx, *, text):
        # text_str = ' '.join(text).replace("'", "")
        text_str = remove_punctuation(cleanemojis(text)).replace("\n", "")
        sentiment = predict_sentiment(text_str, 1)
        # sentiment = 1
        if sentiment == 1:
            string = "does not have anti trans"
        else:
            string = "has anti trans"

        emojis = ['✅', '❌']
        embed = embed_func(ctx, "Sentiment analysis", f"Following my analysis it appears your string \"{text_str}\" "
                                                      f"{string}"
                                                      f" sentiment")
        message = await ctx.send(embed=embed)
        for emoji in emojis:
            await message.add_reaction(emoji)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.bot:
            return

        # embed = reaction.embeds[0]
        # print(embed)
        # print(reaction.message)
        # print(reaction.message.embeds)
        message = reaction.message
        # print(message)
        embed = message.embeds
        # print(embed[0].fields)
        # print(embed[0].fields[0].value)
        val = embed[0].fields[0].value
        # print(val)
        val = val.split('"')
        # print(val)
        text = val[1]
        # print(text)
        emoji = reaction.emoji

        # if emoji == "emoji 1":
        #     fixed_channel = self.bot.get_channel(ctx.channel.id)
        #     await fixed_channel.send(embed=embed)

        if emoji == '✅':
            # print(str(val[2][5:]))
            if str(val[2][5:]).startswith("anti"):
                correct_sentiment = 0
            else:
                correct_sentiment = 1
        elif emoji == '❌':
            if str(val[2][5:]).startswith("anti"):
                correct_sentiment = 1
            else:
                correct_sentiment = 0
        else:
            return

        if str(val[2]).__contains__("trans"):
            i = 1
        else:
            i = 0

        # print(f"text: {text}")
        # print(f"correct sentiment: {correct_sentiment}")

        with open(samples_arr[i]) as f:
            data = f.read()
            if text in data:
                # print("text already in file")
                return

        with open(samples_arr[i], "a") as f:
            f.write(f"{correct_sentiment}, {text}\n")

    @commands.command(name="retrain", alias="re-train", help="Retrains the "
                                                             "sentiment analysis")
    async def retrain(self, ctx):
        if ctx.author.id == 484444017489084416:
            embed = embed_func(ctx, "Retraining", "The sentiment analysis is "
                                                  "currently retraining.  This may"
                                                  " take a few minutes.")
            embed2 = embed_func(ctx, "Retrained", "The sentiment analysis "
                                                  "has finished retraining!")
            await ctx.send(embed=embed, delete_after=1)
            train(0, 5)
            train(1, 50)
            await ctx.send(embed=embed2)

    @commands.command(name="disable-introductions", alias="disable_introductions",
                      brief="Locks introductions",
                      help="Disables functionality that lets people "
                           "speak in general after messaging introductions")
    @pond_check()
    async def disable_introductions(self, ctx):
        embed = embed_func(ctx, "Locked down", "Messages sent in introductions will now"
                                                    " no longer let the user speak in general.")
        self.invites_disabled = True
        await ctx.send(embed=embed)

    @commands.command(name="enable-introductions", alias="enable_introductions",
                      brief="Unlocks introductions",
                      help="Enables functionality that lets people"
                           "speak in general after messaging introductions")
    @pond_check()
    async def enable_introductions(self, ctx):
        embed = embed_func(ctx, "Lock down lifted", "Messages sent in introductions will now"
                                                    " let the user speak in general.")
        self.invites_disabled = False
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        if (message.channel.id == 830565670805962822 and message.author.id != 820065836139675668
                and "7" in message.content and "8" in message.content and not self.invites_disabled):
            # if message.channel.id == 830565670805962822 and message.author.id != 820065836139675668:
            role1 = discord.utils.get((await message.guild.fetch_roles()), name='tadpoles')
            role2 = discord.utils.get((await message.guild.fetch_roles()), name='froglet')
            role3 = discord.utils.get((await message.guild.fetch_roles()), name='froggers')

            content = cleanemojis(message.content)
            # print(content)
            content = re.sub("(?<!\d)\d{2}(?!\d)", "", content).split("7")
            # print(content)
            # content = content.split("7")
            content = content[1].split("8")
            # print(content)
            content2 = content[1][1:].replace("\n", "")
            # print(content2)
            content = content[0][1:].replace("\n", "")
            # print(content)
            # print(content)

            if predict_sentiment(content, 0) != 1 or predict_sentiment(content2, 1) != 1:
                if predict_sentiment(content, 0) != 1 and predict_sentiment(content2, 1) != 1:
                    reason = "pro-billionaire and anti-trans"
                    output = f"{content}\" and \"{content2}"

                elif predict_sentiment(content, 0) != 1:
                    reason = "pro-billionaire"
                    output = content

                elif predict_sentiment(content2, 1) != 1:
                    reason = "anti-trans"
                    output = content2

                channel = message.guild.get_channel(829355854582906930)
                embed = embed_func(message, "Manual review",
                                   f"{message.author.name}#{message.author.discriminator}'s"
                                   f" introduction message\n"
                                   f" \"{message.content}\" \nhas been held for manual "
                                   f"review due to detected {reason} sentiment "
                                   f"from the line \"{output}\".  \nReact with ✅ to let "
                                   f"them in, otherwise, they will not be let in.")
                await message.add_reaction("🤨")
                await channel.send(embed=embed)
            else:
                # If a user has any of the 3 roles, ignore their message
                if not (role1 in message.author.roles or role2 in message.author.roles
                        or role3 in message.author.roles):
                    ch = message.guild.get_channel(829349688197120052)
                    # ch = message.guild.get_channel(829358413065486376)
                    # print(message.guild.roles)
                    await message.author.add_roles(role1)
                    # await message.author.add_roles(message.author, role)
                    embed = embed_func(message, "Welcome!", f"Welcome to the pond {message.author.mention}")
                    await ch.send(embed=embed)

                    # Sends a message mentioning the user and then deletes it after 1 second because
                    # discord embeds don't notify someone if they've been tagged.
                    await ch.send(message.author.mention, delete_after=1)

                # print("accepted")

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.bot:
            return

        message = reaction.message
        embed = message.embeds
        # print(embed)
        val = embed[0].fields[0].value
        title = embed[0].fields[0].name
        # print(val)
        # print(title)
        if title == "Manual review":
            emoji = reaction.emoji

            if emoji == '✅':
                user = ((val.split("\n"))[0].split(" ")[0])[:-2]
                # print(1)
                # print(user)
                member = message.guild.get_member_named(user)
                role1 = discord.utils.get((await message.guild.fetch_roles()), name='tadpoles')
                # role2 = discord.utils.get((await message.guild.fetch_roles()), name='froglet')
                # role3 = discord.utils.get((await message.guild.fetch_roles()), name='froggers')

                # If a user has any of the 3 roles, ignore their message
                # if not (
                # role1 in message.author.roles or role2 in message.author.roles or role3 in message.author.roles):
                ch = message.guild.get_channel(829349688197120052)
#                 ch = message.guild.get_channel(829358413065486376)
                # print(message.guild.roles)
                await member.add_roles(role1)
                # await message.author.add_roles(message.author, role)
                embed = embed_func(message, "Welcome!", f"Welcome to the pond {member.mention}")
                await ch.send(embed=embed)

                # Sends a message mentioning the user and then deletes it after 1 second because
                # discord embeds don't notify someone if they've been tagged.
                await ch.send(member.mention, delete_after=1)
            else:
                # print(2)
                return

        # print(f"text: {text}")
        # print(f"correct sentiment: {correct_sentiment}")


def setup(bot):
    bot.add_cog(Sentiment(bot))
