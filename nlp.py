import pandas as pd
from nltk.tokenize import word_tokenize
import gensim
from nltk.stem import PorterStemmer
import numpy as np


df = pd.read_csv("CHAT.csv", sep=":", encoding='latin-1',
                 names=["Student", "Comment"], skipinitialspace=True, comment='"')


def identify_tokens(row):
    # Calculating tokens
    comment = str(row['Comment']).lower()
    tokens = word_tokenize(comment)
    # takes only words (not punctuation)
    token_words = [w for w in tokens if w.isalpha()]
    return token_words


def stem_list(row):
    # Words are being stemmed
    stemming = PorterStemmer()
    my_list = row['words']
    stemmed_list = [stemming.stem(word) for word in my_list]
    return stemmed_list


def dictionary():
    token_dictionary = gensim.corpora.Dictionary(df['words'])
    return token_dictionary


def bag_of_words(row):
    token_dictionary = dictionary()
    words = row['words']
    corpus = token_dictionary.doc2bow(words)
    return corpus


def tfidf(row):
    token_dictionary = dictionary()
    corpus = row['corpus']
    print(corpus)
    # tfidf = gensim.models.TfidfModel(corpus)
    # print(tfidf)
    # for doc in tfidf[corpus]:
    #     print([[token_dictionary[id], np.around(freq, decimals=2)]
    #            for id, freq in doc])


def run():
    df['words'] = df.apply(identify_tokens, axis=1)
    df['stemmed_words'] = df.apply(stem_list, axis=1)
    df['corpus'] = df.apply(bag_of_words, axis=1)
    print(df.head(20))
    df['tfidf'] = df.apply(tfidf, axis=1)


run()
