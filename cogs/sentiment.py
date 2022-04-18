from discord.ext import commands
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from keras_preprocessing.text import Tokenizer
from keras_preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout, SpatialDropout1D
from keras.layers import Embedding

from bot import embed_func


def remove_punctuation(text):
    final = "".join(u for u in text if u not in ("?", ".", ";", ":", "!", '"'))
    return final


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

    df['Text'] = df['Text'].apply(remove_punctuation)
    dfNew = df[['Text', 'sentiment']]
    print()
    print(dfNew.head())

    # print(dfNew['sentiment'].value_counts())

    global sentiment_label
    sentiment_label = dfNew.sentiment.factorize()
    print(sentiment_label)

    text = dfNew.Text.values

    global tokenizer
    tokenizer = Tokenizer(num_words=100)
    tokenizer.fit_on_texts(text)

    encoded_docs = tokenizer.texts_to_sequences(text)

    padded_sequence = pad_sequences(encoded_docs, maxlen=200)

    embedding_vector_length = 32
    global model
    model = Sequential()
    vocab_size = len(tokenizer.word_index) + 1
    model.add(Embedding(vocab_size, embedding_vector_length, input_length=200))
    model.add(SpatialDropout1D(0.25))
    model.add(LSTM(50, dropout=0.5, recurrent_dropout=0.5))
    model.add(Dropout(0.2))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    print(model.summary())

    history = model.fit(padded_sequence, sentiment_label[0], validation_split=0.2,
                        epochs=50, batch_size=10)
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
    tx = pad_sequences(tx, maxlen=200)
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
    async def analyse(self, ctx, *text):
        text_str = ' '.join(text).replace("'", "")
        text_str = remove_punctuation(text_str)
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


def setup(bot):
    bot.add_cog(Sentiment(bot))
