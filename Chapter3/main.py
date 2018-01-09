from sklearn.datasets import fetch_mldata
import matplotlib
import matplotlib.pyplot as plt

import numpy as np
import scipy

#Get MNIST handwritten digits
mnist = fetch_mldata('MNIST original')
#print(mnist)

X, y = mnist["data"], mnist["target"]
#print(X.shape)  # (70000, 784)
#print(y.shape)  # (70000,)

some_digit = X[36000]
some_digit_image = some_digit.reshape(28,28)
plt.imshow(some_digit_image, cmap=matplotlib.cm.binary, interpolation="nearest")
plt.axis("off")
plt.show()
