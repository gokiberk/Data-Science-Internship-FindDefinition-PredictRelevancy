def predict_model(classifier, test_features): 
    # predict using model
    predictions = classifier.predict(test_features) 
    return predictions

# load model.pkl using pickle
import pickle
model = "model.pkl"
with open(model, "rb") as f:
    pickle.load((lr, cv, tv), f)

# assign key_test to input csv file that is created line by line
import csv

with open("./bwq.csv", 'r') as file:
  test = csv.reader(file)

key_test = test['data']

cv_test_features = cv.transform(key_test)
tv_test_features = tv.transform(key_test)

from sklearn.linear_model import SGDClassifier, LogisticRegression

lr = LogisticRegression(penalty='l2', max_iter=100, C=1)

lr_bow_predictions = predict_model(classifier=lr, test_features=cv_test_features)

# this will print an array of 1's and 0's, displaying relevancy of sentences to SSB
print(lr_bow_predictions)
