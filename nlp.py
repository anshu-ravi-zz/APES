import pandas as pd
from nltk.tokenize import word_tokenize
import gensim
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords


df = pd.read_csv("CHAT.csv",
                 sep=":",
                 encoding='latin-1',
                 names=["Student", "Comment"],
                 skipinitialspace=True,
                 comment='"')


def identify_tokens(row):
    # Calculating tokens
    comment = str(row['Comment'])
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
    # print(words)
    corpus = token_dictionary.doc2bow(words)
    print(corpus)
    return corpus


def run():
    df['words'] = df.apply(identify_tokens, axis=1)
    df['stemmed_words'] = df.apply(stem_list, axis=1)
    df.apply(bag_of_words, axis=1)


run()
