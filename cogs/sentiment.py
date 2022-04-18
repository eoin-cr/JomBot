from discord.ext import commands
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, classification_report


def remove_punctuation(text):
    final = "".join(u for u in text if u not in ("?", ".", ";", ":", "!", '"'))
    return final


# class Sentiment(commands.Cog):
#     def __init__(self, bot):
#         self.bot = bot
#         print("Sentiment analysis initialised")

def analyse(input):
    df = pd.read_csv('../Billionaire_samples.csv')
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

    # random split train and test data

    index = df.index
    df['random_number'] = np.random.randn(len(index))

    train = df[df['random_number'] <= 0.8]
    test = df[df['random_number'] > 0.8]

    vectorizer = CountVectorizer(token_pattern=r'\b\w+\b')

    train_matrix = vectorizer.fit_transform(train['Text'])
    test_matrix = vectorizer.transform(test['Text'])

    lr = LogisticRegression()

    x_train = train_matrix
    x_test = test_matrix
    y_train = train['sentiment']
    y_test = test['sentiment']

    lr.fit(x_train, y_train)

    predictions = lr.predict(x_test)

    new = np.asarray(y_test)
    confusion_matrix(predictions, y_test)

    print(classification_report(predictions, y_test))

    input_arr = np.asarray(input)
    print(lr.predict(input_arr))


analyse("I love billionaires")
