from discord.ext import commands
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, classification_report
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, SpatialDropout1D
from tensorflow.keras.layers import Embedding
import matplotlib.pyplot as plt
from bot import embed_func


def remove_punctuation(text):
    final = "".join(u for u in text if u not in ("?", ".", ";", ":", "!", '"'))
    return final


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

sentiment_label = dfNew.sentiment.factorize()
print(sentiment_label)

text = dfNew.Text.values

tokenizer = Tokenizer(num_words=100)
tokenizer.fit_on_texts(text)

encoded_docs = tokenizer.texts_to_sequences(text)

padded_sequence = pad_sequences(encoded_docs, maxlen=200)

embedding_vector_length = 32
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
                    epochs=70, batch_size=10)

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

test_sentence1 = "I love billionaires"
predict_sentiment(test_sentence1)

test_sentence2 = "I fucking hate them so goddamn much fucking hell."
predict_sentiment(test_sentence2)

predict_sentiment("I love billionaires so much")
predict_sentiment("I fucking hate billionaires")
predict_sentiment("They're awful people")
predict_sentiment("They're awful people who exploit the working class")
predict_sentiment("They're good people who provide jobs")
predict_sentiment("They're pretty dope people who are overhated")
predict_sentiment("I'm sick of socialists nowadays hating on billionares, they earned their money")
predict_sentiment("Billionaire moment")

class Sentiment(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("Sentiment analysis initialised")

    @commands.command(name="analyse", help="Performs sentiment analysis")
    async def analyse(self, ctx, *text):
        text_str = ' '.join(text)
        sentiment = predict_sentiment(text_str)
        if sentiment == 1:
            string = "anti billionaire"
        else:
            string = "pro billionaire"
        embed = embed_func(ctx, "Sentiment analysis", f"Following my analysis it appears your string has {string}"
                                                      f" sentiment")
        await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(Sentiment(bot))
