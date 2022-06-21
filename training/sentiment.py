import json
import re
import string
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pkg_resources
import spacy
from keras.layers import Embedding
from keras.layers import LSTM, Dense, Dropout, SpatialDropout1D
from keras.models import Sequential
from keras_preprocessing.sequence import pad_sequences
from keras_preprocessing.text import Tokenizer
from symspellpy.symspellpy import SymSpell, Verbosity
from tensorflow import keras
from tqdm import tqdm


def cleanemojis(string):
    return re.sub(r"<a?:([a-zA-Z0-9_-]{1,32}):[0-9]{17,21}>", "", string)


# quick note about the two tokenizer arrays: as I want to train the code on two different
# sample sets to calculate different things, but don't want to duplicate any code, I've
# simply created an array which stores the models, tokens, etc.  The 0th value of the
# arrays refers to the billionaire sample set, the 1st value refers to the trans sample
# set


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
    This function does very simple spell correction normalization using pyspellchecker module.
    It works over a tokenized sentence and only the token representations are changed.
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


def train(i, batch):
    df = pd.read_csv(samples_arr[i])
    print(df.head())

    # assign reviews with score > 3 as positive sentiment
    # score < 3 negative sentiment
    # remove score = 3df = df[df['Score'] != 3]
    df['sentiment'] = df['Score'].apply(lambda rating: +1 if rating == 1 else -1)

    # split df - positive and negative sentiment:
    # positive = df[df['sentiment'] == 1]
    # negative = df[df['sentiment'] == -1]

    df['Text'] = normalization_pipeline(df['Text'])
    dfNew = df[['Text', 'sentiment']]
    print()
    # print(dfNew.head())

    # print(dfNew['sentiment'].value_counts())

    # global sentiment_label_arr
    sentiment_label = dfNew.sentiment.factorize()
    # print(sentiment_label)

    text = dfNew.Text.values

    # global tokenizer_arr
    tokenizer = Tokenizer(num_words=100)
    tokenizer.fit_on_texts(text)
    # tokenizer = normalization_pipeline(tokenizer)

    encoded_docs = tokenizer.texts_to_sequences(text)

    padded_sequence = pad_sequences(encoded_docs, maxlen=700)

    embedding_vector_length = 32
    # global model_arr
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
                        epochs=15, batch_size=batch, callbacks=my_callbacks)

    model.save('models/' + samples_arr[i][:-11])

    # epochs = 50, batch_size = 50)
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
    tokenizer_arr[i] = tokenizer
    model_arr[i] = model
    sentiment_label_arr[i] = sentiment_label


# def predict_sentiment(text, i):
#     tx = tokenizer_arr[i].texts_to_sequences([text])
#     tx = pad_sequences(tx, maxlen=700)
#     prediction = int(model_arr[i].predict(tx).round().item())
#     # print("Predicted label: ", sentiment_label[1][prediction])
#     return sentiment_label_arr[i][1][prediction]
#

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
