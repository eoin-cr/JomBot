import json
import discord
import re
import string
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pkg_resources
import spacy
from discord.ext import commands
from keras.layers import Embedding
from keras.layers import LSTM, Dense, Dropout, SpatialDropout1D
from keras.models import Sequential
from keras_preprocessing.sequence import pad_sequences
from keras_preprocessing.text import Tokenizer
from symspellpy.symspellpy import SymSpell, Verbosity
from tensorflow import keras
from tqdm import tqdm
from bot import embed_func
import string


def remove_punctuation(text):
    new_string = text.translate(str.maketrans('', '', string.punctuation))

    return new_string
    #
    # final = "".join(u for u in text if u not in ("?", ".", ";", ":", "!", '"', "'", "’", ","))
    # return final


def simplify_punctuation_and_whitespace(sentence_list):
    norm_sents = []
    print("Normalizing whitespaces and punctuation")
    for sentence in tqdm(sentence_list):
        sent = remove_punctuation(sentence)
        sent = _normalize_whitespace(sent)
        norm_sents.append(sent)
    return norm_sents


def _normalize_whitespace(text):
    """
    This function normalizes whitespaces, removing duplicates.
    """
    corrected = str(text)
    corrected = re.sub(r"//t", r"\t", corrected)
    corrected = re.sub(r"( )\1+", r"\1", corrected)
    corrected = re.sub(r"(\n)\1+", r"\1", corrected)
    corrected = re.sub(r"(\r)\1+", r"\1", corrected)
    corrected = re.sub(r"(\t)\1+", r"\1", corrected)
    return corrected.strip(" ")


def normalize_contractions(sentence_list):
    contraction_list = json.loads(open('english_contractions.json', 'r').read())
    norm_sents = []
    print("Normalizing contractions")
    for sentence in tqdm(sentence_list):
        norm_sents.append(_normalize_contractions_text(sentence, contraction_list))
    return norm_sents


def _normalize_contractions_text(text, contractions):
    """
    This function normalizes english contractions.
    """
    new_token_list = []
    token_list = text.split()
    for word_pos in range(len(token_list)):
        word = token_list[word_pos]
        first_upper = False
        if word[0].isupper():
            first_upper = True
        if word.lower() in contractions:
            replacement = contractions[word.lower()]
            if first_upper:
                replacement = replacement[0].upper() + replacement[1:]
            replacement_tokens = replacement.split()
            if len(replacement_tokens) > 1:
                new_token_list.append(replacement_tokens[0])
                new_token_list.append(replacement_tokens[1])
            else:
                new_token_list.append(replacement_tokens[0])
        else:
            new_token_list.append(word)
    sentence = " ".join(new_token_list).strip(" ")
    return sentence


def spell_correction(sentence_list):
    max_edit_distance_dictionary = 3
    prefix_length = 4
    spellchecker = SymSpell(max_edit_distance_dictionary, prefix_length)
    dictionary_path = pkg_resources.resource_filename(
        "symspellpy", "frequency_dictionary_en_82_765.txt")
    bigram_path = pkg_resources.resource_filename(
        "symspellpy", "frequency_bigramdictionary_en_243_342.txt")
    spellchecker.load_dictionary(dictionary_path, term_index=0, count_index=1)
    spellchecker.load_bigram_dictionary(dictionary_path, term_index=0, count_index=2)
    norm_sents = []
    print("Spell correcting")
    for sentence in tqdm(sentence_list):
        norm_sents.append(_spell_correction_text(sentence, spellchecker))
    return norm_sents


def _spell_correction_text(text, spellchecker):
    """
    This function does very simple spell correction normalization using pyspellchecker module. It works over a tokenized sentence and only the token representations are changed.
    """
    if len(text) < 1:
        return ""
    # Spell checker config
    max_edit_distance_lookup = 2
    suggestion_verbosity = Verbosity.TOP  # TOP, CLOSEST, ALL
    # End of Spell checker config
    token_list = text.split()
    for word_pos in range(len(token_list)):
        word = token_list[word_pos]
        if word is None:
            token_list[word_pos] = ""
            continue
        if not '\n' in word and word not in string.punctuation and not is_numeric(word) and not (
                word.lower() in spellchecker.words.keys()):
            suggestions = spellchecker.lookup(word.lower(), suggestion_verbosity, max_edit_distance_lookup)
            # Checks first uppercase to conserve the case.
            upperfirst = word[0].isupper()
            # Checks for correction suggestions.
            if len(suggestions) > 0:
                correction = suggestions[0].term
                replacement = correction
            # We call our _reduce_exaggerations function if no suggestion is found. Maybe there are repeated chars.
            else:
                replacement = _reduce_exaggerations(word)
            # Takes the case back to the word.
            if upperfirst:
                replacement = replacement[0].upper() + replacement[1:]
            word = replacement
            token_list[word_pos] = word
    return " ".join(token_list).strip()


def _reduce_exaggerations(text):
    """
    Auxiliary function to help with exxagerated words.
    Examples:
        woooooords -> words
        yaaaaaaaaaaaaaaay -> yay
    """
    correction = str(text)
    return re.sub(r'([\w])\1+', r'\1', correction)


def lemmatize(sentence_list):
    nlp = spacy.load('en_core_web_sm')
    new_norm = []
    print("Lemmatizing Sentences")
    for sentence in tqdm(sentence_list):
        new_norm.append(_lemmatize_text(sentence, nlp).strip())
    return new_norm


def _lemmatize_text(sentence, nlp):
    sent = ""
    doc = nlp(sentence)
    for token in doc:
        if '@' in token.text:
            sent += " @MENTION"
        elif '#' in token.text:
            sent += " #HASHTAG"
        else:
            sent += " " + token.lemma_
    return sent


def is_numeric(text):
    for char in text:
        if not (char in "0123456789" or char in ",%.$"):
            return False
    return True


def normalization_pipeline(sentences):
    print("##############################")
    print("Starting Normalization Process")
    sentences = simplify_punctuation_and_whitespace(sentences)
    sentences = normalize_contractions(sentences)
    sentences = spell_correction(sentences)
    sentences = lemmatize(sentences)
    print("Normalization Process Finished")
    print("##############################")
    return sentences


def train():
    df = pd.read_csv('Billionaire_samples.csv')
    print(df.head())

    # assign reviews with score > 3 as positive sentiment
    # score < 3 negative sentiment
    # remove score = 3df = df[df['Score'] != 3]
    df['sentiment'] = df['Score'].apply(lambda rating: +1 if rating > 3 else -1)

    # split df - positive and negative sentiment:
    positive = df[df['sentiment'] == 1]
    negative = df[df['sentiment'] == -1]

    df['Text'] = normalization_pipeline(df['Text'])
    dfNew = df[['Text', 'sentiment']]
    print()
    # print(dfNew.head())

    # print(dfNew['sentiment'].value_counts())

    global sentiment_label
    sentiment_label = dfNew.sentiment.factorize()
    # print(sentiment_label)

    text = dfNew.Text.values

    global tokenizer
    tokenizer = Tokenizer(num_words=100)
    tokenizer.fit_on_texts(text)
    # tokenizer = normalization_pipeline(tokenizer)

    encoded_docs = tokenizer.texts_to_sequences(text)

    padded_sequence = pad_sequences(encoded_docs, maxlen=700)

    embedding_vector_length = 32
    global model
    model = Sequential()
    vocab_size = len(tokenizer.word_index) + 1
    model.add(Embedding(vocab_size, embedding_vector_length, input_length=700))
    model.add(SpatialDropout1D(0.25))
    model.add(LSTM(50, dropout=0.5, recurrent_dropout=0.5))
    model.add(Dropout(0.2))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    print(model.summary())

    # stops if the model starts overfitting
    my_callbacks = [
        keras.callbacks.EarlyStopping(patience=2)
    ]

    history = model.fit(padded_sequence, sentiment_label[0], validation_split=0.2,
                        epochs=15, batch_size=10, callbacks=my_callbacks)
    # epochs=5, batch_size=10)

    plt.plot(history.history['accuracy'], label='acc')
    plt.plot(history.history['val_accuracy'], label='val_acc')
    plt.legend()
    plt.show()

    # plt.savefig("Acc_plot.jpg")

    plt.plot(history.history['loss'], label='loss')
    plt.plot(history.history['val_loss'], label='val_loss')

    plt.legend()
    plt.show()

    # plt.savefig("Loss_plt.jpg")


def predict_sentiment(text):
    tx = tokenizer.texts_to_sequences([text])
    tx = pad_sequences(tx, maxlen=700)
    prediction = int(model.predict(tx).round().item())
    # print("Predicted label: ", sentiment_label[1][prediction])
    return sentiment_label[1][prediction]


# test_sentence1 = "I love billionaires"
# predict_sentiment(test_sentence1)
#
# test_sentence2 = "I fucking hate them so goddamn much fucking hell."
# predict_sentiment(test_sentence2)
#
# predict_sentiment("I love billionaires so much")
# predict_sentiment("I fucking hate billionaires")
# predict_sentiment("They're awful people")
# predict_sentiment("They're awful people who exploit the working class")
# predict_sentiment("They're good people who provide jobs")
# predict_sentiment("They're pretty dope people who are overhated")
# predict_sentiment("I'm sick of socialists nowadays hating on billionares, they earned their money")
# predict_sentiment("Billionaire moment")


class Sentiment(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        train()
        print("Sentiment analysis initialised")

    @commands.command(name="analyse", help="Performs sentiment analysis")
    async def analyse(self, ctx, *, text):
        # text_str = ' '.join(text).replace("'", "")
        text_str = remove_punctuation(text).replace("\n", "")
        sentiment = predict_sentiment(text_str)
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
                correct_sentiment = 5
            else:
                correct_sentiment = 1
        elif emoji == '❌':
            if str(val[2][5:]).startswith("anti"):
                correct_sentiment = 1
            else:
                correct_sentiment = 5
        else:
            return

        # print(f"text: {text}")
        # print(f"correct sentiment: {correct_sentiment}")

        with open('Billionaire_samples.csv') as f:
            data = f.read()
            if text in data:
                # print("text already in file")
                return

        with open('Billionaire_samples.csv', "a") as f:
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
            train()
            await ctx.send(embed=embed2)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == 830565670805962822 and message.author.id != 820065836139675668:
            role1 = discord.utils.get((await message.guild.fetch_roles()), name='tadpoles')
            role2 = discord.utils.get((await message.guild.fetch_roles()), name='froglet')
            role3 = discord.utils.get((await message.guild.fetch_roles()), name='froggers')

            # If a user has any of the 3 roles, ignore their message
            if not(role1 in message.author.roles or role2 in message.author.roles or role3 in message.author.roles):
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

        if (message.channel.id == 829358413065486376 or message.channel.id == 829355854582906930
                and "7" in message.content and "8" in message.content):
            content = message.content
            # print(content)
            content = re.sub("(?<!\d)\d{2}(?!\d)", "", content).split("7")
            # print(content)
            # content = content.split("7")
            content = content[1].split("8")
            content = content[0][1:].replace("\n", "")
            print(content)

            if predict_sentiment(content) != 1:
                channel = message.guild.get_channel(829358413065486376)
                embed = embed_func(message, "Manual review",
                                        f"{message.author.name}#{message.author.discriminator}'s"
                                        f" introduction message\n"
                                        f" \"{message.content}\" \nhas been held for manual "
                                        f"review due to detected pro billionaire sentiment "
                                        f"from the line \"{content}\".  \nReact with ✅ to let "
                                        f"them in, otherwise, they will not be let in.")
                await message.add_reaction("🤨")
                await channel.send(embed=embed)
            else:
                print("accepted")


    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.bot:
            return

        message = reaction.message
        embed = message.embeds
        print(embed)
        val = embed[0].fields[0].value
        title = embed[0].fields[0].name
        print(val)
        print(title)
        if title == "Manual review":
            emoji = reaction.emoji

            if emoji == '✅':
                user = ((val.split("\n"))[0].split(" ")[0])[:-2]
                print(1)
                print(user)
                member = message.guild.get_member_named(user)
                role1 = discord.utils.get((await message.guild.fetch_roles()), name='tadpoles')
                # role2 = discord.utils.get((await message.guild.fetch_roles()), name='froglet')
                # role3 = discord.utils.get((await message.guild.fetch_roles()), name='froggers')

                # If a user has any of the 3 roles, ignore their message
                # if not (
                #         role1 in message.author.roles or role2 in message.author.roles or role3 in message.author.roles):
                # ch = message.guild.get_channel(829349688197120052)
                ch = message.guild.get_channel(829358413065486376)
                # print(message.guild.roles)
                await member.add_roles(role1)
                # await message.author.add_roles(message.author, role)
                embed = embed_func(message, "Welcome!", f"Welcome to the pond {member.mention}")
                await ch.send(embed=embed)

                # Sends a message mentioning the user and then deletes it after 1 second because
                # discord embeds don't notify someone if they've been tagged.
                await ch.send(member.mention, delete_after=1)
            else:
                print(2)
                return

        # print(f"text: {text}")
        # print(f"correct sentiment: {correct_sentiment}")


def setup(bot):
    bot.add_cog(Sentiment(bot))
