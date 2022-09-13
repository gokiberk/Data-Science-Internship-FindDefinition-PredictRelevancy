import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


from sklearn import metrics
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.base import clone
from sklearn.preprocessing import label_binarize
from scipy import interp
from sklearn.metrics import roc_curve, auc 
import argparse
import pickle

# Initiate the parser
parser = argparse.ArgumentParser()

# Add long and short argument
parser.add_argument("--out", "-o", help="set output model name .pkl")
parser.add_argument("--csv", "-c", help="set input csv directory")

# Read arguments from the command line
args = parser.parse_args()

if args.out:
    print("Output model name set to: %s" % args.out)
if args.csv:
    print("CSV input directory set to: %s" % args.csv)

def train_predict_model(classifier, train_features, train_labels, test_features):
    # build model    
    classifier.fit(train_features, train_labels)
    # predict using model
    predictions = classifier.predict(test_features) 
    return predictions 

def train_model(clf, train_features, train_labels):
    # build model    
    clf.fit(train_features, train_labels)


#df = pd.read_csv("docs/ssb-clean.csv", sep=';')
df = pd.read_csv( args.csv, sep=';')

df['phrase_len'] = [len(t) for t in df.Key]
df.head(4)

from nltk.corpus import stopwords
import nltk
import re
stop = stopwords.words("turkish")
df['Key'] = df['Key'].apply(lambda x: " ".join([x for x in x.split() if x not in stop]))
stop = stopwords.words("english")
df['Key'] = df['Key'].apply(lambda x: " ".join([x for x in x.split() if x not in stop]))
df['Key'] = df['Key'].apply(lambda x: " ".join([re.sub('[^A-Za-zĞÜŞİÖÇöçşğüı]+',' ', x) for x in nltk.word_tokenize(x)]))
df['Key'] = df['Key'].apply(lambda x: re.sub('bir|olarak|olan', ' ', x))


neg_phrases = df[df.Value == 0]
neg_words = []
for t in neg_phrases.Key:
    neg_words.append(t)
neg_words[:4]

neg_text = pd.Series(neg_words).str.cat(sep=' ')
neg_text[:150]

from sklearn.feature_extraction.text import CountVectorizer
cvector = CountVectorizer(min_df = 0.0, max_df = 1.0, ngram_range=(1,2))
cvector.fit(df.Key)

len(cvector.get_feature_names_out())

key = np.array(df['Key'])
value = np.array(df['Value'])
# build train and test datasets
"""
from sklearn.model_selection import train_test_split    
key_train, key_test, value_train, value_test = train_test_split(key, value, test_size=0.2, random_state=4)
"""
key_train = key
value_train = value

# to test real input, comment out above train_test_split
# assign key_test to your own input of csv to check relativity of sentences in overall
#text = pd.read_csv("docs/savunmaF.csv", delimiter = ';')
#key_test = text['data']

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

## Build Bag-Of-Words on train keys
cv = CountVectorizer(max_features=10000)
cv_train_features = cv.fit_transform(key_train)

# build TFIDF features on train values
tv = TfidfVectorizer(min_df=0.0, max_df=1.0, ngram_range=(1,2), sublinear_tf=True)
tv_train_features = tv.fit_transform(key_train)

# transform test reviews into features
cv_test_features = cv.transform(key_test)
tv_test_features = tv.transform(key_test)

from sklearn.linear_model import SGDClassifier, LogisticRegression

lr = LogisticRegression(penalty='l2', max_iter=100, C=1)
#sgd = SGDClassifier(loss='hinge', n_iter_no_change=100)

train_model(clf=lr, train_features=cv_train_features, train_labels=value_train)

with open(args.out,'wb') as f:
    pickle.dump((lr, cv, tv),f)
