import pandas as pd
import gensim
from gensim import corpora, models, similarities
from nltk.tokenize import word_tokenize
import jieba

df = pd.read_csv("CHAT.csv", sep=":", encoding='latin-1',
                 names=["Student", "Comment"], skipinitialspace=True, comment='"')

keyword = '''In statistics, linear regression is a linear approach to modeling the relationship between a scalar response (or dependent variable) and one or more explanatory variables (or independent variables). The case of one explanatory variable is called simple linear regression. For more than one explanatory variable, the process is called multiple linear regression.[1] This term is distinct from multivariate linear regression, where multiple correlated dependent variables are predicted, rather than a single scalar variable.[2] In linear regression, the relationships are modeled using linear predictor functions whose unknown model parameters are estimated from the data. Such models are called linear models.[3] Most commonly, the conditional mean of the response given the values of the explanatory variables (or predictors) is assumed to be an affine function of those values; less commonly, the conditional median or some other quantile is used. Like all forms of regression analysis, linear regression focuses on the conditional probability distribution of the response given the values of the predictors, rather than on the joint probability distribution of all of these variables, which is the domain of multivariate analysis. '''


def identify_tokens(row):
    # Calculating tokens
    comment = str(row['Comment']).lower()
    tokens = word_tokenize(comment)
    # takes only words (not punctuation)
    token_words = [w for w in tokens if w.isalpha()]
    return token_words


def dictionary():
    token_dictionary = gensim.corpora.Dictionary(df['words'])
    return token_dictionary


def bag_of_words(row):
    token_dictionary = dictionary()
    words = row['words']
    corpus = token_dictionary.doc2bow(words)
    return corpus


def nlp():
    df['words'] = df.apply(identify_tokens, axis=1)
    token_dictionary = dictionary()
    feature_cnt = len(token_dictionary.token2id)
    corpus = df.apply(bag_of_words, axis=1)
    corpus = list(corpus)
    tfidf = models.TfidfModel(corpus)
    kw_vector = token_dictionary.doc2bow(jieba.lcut(keyword))
    index = similarities.SparseMatrixSimilarity(
        tfidf[corpus], num_features=feature_cnt)
    df['sim'] = index[tfidf[kw_vector]]
    # for i in range(110, 130):
    #     print('keyword is similar to text%d: %.2f' % (i + 1, df.loc[i, 'sim']))

    print(df)


nlp()
