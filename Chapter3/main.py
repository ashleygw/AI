from sklearn.datasets import fetch_mldata
import matplotlib
import matplotlib.pyplot as plt
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import cross_val_score, cross_val_predict
import numpy as np
import scipy
from sklearn.base import BaseEstimator
from sklearn.metrics import confusion_matrix

# Get MNIST handwritten digits
mnist = fetch_mldata('MNIST original')
#print(mnist)

X, y = mnist["data"], mnist["target"]
#print(X.shape)  # (70000, 784)
#print(y.shape)  # (70000,)

# Visualize the training and test data
some_digit = X[36000]
# some_digit_image = some_digit.reshape(28,28)
# plt.imshow(some_digit_image, cmap=matplotlib.cm.binary, interpolation="nearest")
# plt.axis("off")
# plt.show()

# Split and shuffle training and testing data
X_train, X_test, y_train, y_test = X[:60000], X[60000:], y[:60000], y[60000:]
shuffle_index = np.random.permutation(60000)
X_train, y_train = X_train[shuffle_index], y_train[shuffle_index]

# Training Binary Classifier
y_train_5 = (y_train == 5)  # True when data == 5
y_test_5 = (y_test == 5)

""" 
Using Stochastic Gradient Descent classifier- 
Good for large datasets and online learning
"""

sgd_clf = SGDClassifier(random_state=42)
sgd_clf.fit(X_train, y_train_5)
sgd_clf.predict([some_digit])

# Implementing Cross validation for the binary model
# cvs = cross_val_score(sgd_clf, X_train, y_train_5, cv=3, scoring="accuracy")
# print(cvs)  # [0.9506  0.93525 0.9524 ] Roughly 95% accuracy on guessing is 5 or not

# Checking base value - Every image classified as "not-5"
class Never5Classifier(BaseEstimator):
    def fit(self, X, y=None):
        pass
    def predict(self, X):
        return np.zeros((len(X), 1), dtype=bool)


# Over 90% accuracy for guessing not 5 always
# never_5_clf = Never5Classifier()
# print(cross_val_score(never_5_clf, X_train, y_train_5, cv=3, scoring="accuracy"))  # [0.9127  0.90745 0.9088 ]

"""
Confusion matrices are better to evaluate classifier performances
Confusing 5's with 3's -> Look in third row fifth column of matrix
"""
y_train_pred = cross_val_predict(sgd_clf, X_train, y_train_5, cv=3)
print(confusion_matrix(y_train_5, y_train_pred))
"""
[[52070  2509] -> Non-5 images. 52070 correctly classified as not 5. 2506 incorrectly classified as 5
 [  838  4583]] -> False negatives (actually 5), True positives (prediction is correct)
"""

# Precision and Recall
from sklearn.metrics import precision_score, recall_score
print(precision_score(y_train_5, y_train_pred))  # 0.8061044805321855 Precision (Correct percentage)
print(recall_score(y_train_5, y_train_pred))  # 0.7600073787124146 Recall (Only detects 76 percentage of 5's)



