import nltk
# nltk.download("punkt")
# nltk.download("movie_reviews")
# nltk.download("stopwords")

from nltk.corpus import movie_reviews
from nltk.corpus import stopwords
from random import shuffle
import string
from nltk import NaiveBayesClassifier
from nltk import classify
from nltk import word_tokenize
from MAIN_scrap_movies_reviews import reviews_extract
import joblib


def bag_words(words):
    global stop_words
    stop_words = stopwords.words('english')
    clean = []
    for i in words:
        if i not in stop_words and i not in string.punctuation:
            clean.append(i)
    dictionary = dict([word, True] for word in clean)
    #print(dictionary)
    return dictionary

def TrainingAndTesting():
    pos_review = []
    neg_review = []

    for fileid in movie_reviews.fileids('pos'):
        pos_review.append(movie_reviews.words(fileid))

    for fileid in movie_reviews.fileids('neg'):
        neg_review.append(movie_reviews.words(fileid))

    pos_set = []
    for word in pos_review:
        pos_set.append((bag_words(word),'pos'))

    neg_set = []
    for word in neg_review:
        neg_set.append((bag_words(word),'neg'))

    shuffle(pos_set)
    shuffle(neg_set)
    test_set = pos_set[:200]+neg_set[:200]
    train_set = pos_set[200:]+neg_set[200:]

    classifier = NaiveBayesClassifier.train(train_set)
    acc = classify.accuracy(classifier,test_set)
    print(acc)
    joblib.dump(classifier,'imdb_movies_reviews.pkl')



def predicting():
    classifier = joblib.load('imdb_movies_reviews.pkl')
    reviews_film, movie = reviews_extract()
    testing = reviews_film

    tokens = []
    for i in testing:
        tokens.append(word_tokenize(i))

    set_testing = []
    for i in tokens:
        set_testing.append(bag_words(i))

    final = []
    for i in set_testing:
        final.append(classifier.classify(i))

    n = 0
    p = 0
    for i in final:
        if i == 'neg':
            n+= 1
        else:
            p+= 1
    pos_per = (p / len(final)) * 100

    return movie,pos_per,len(final)

TrainingAndTesting()
movie,positive_per,total_reviews = predicting()
print('The film {} has got {} percent positive reviews'.format(movie, round(positive_per)))
if positive_per > 60:
    print('overall impression of movie is good  ')
else:
    print('overall impression of movie is bad ')