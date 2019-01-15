import numpy as np
import pandas as pd
import time

from sklearn.manifold import TSNE
from sklearn.decomposition import PCA

# read_data = pd.read_csv('data_input/origin/mnist.csv')
#
# start = time.time()
# data_pca = PCA(n_components=50).fit_transform(read_data)
# data_embedded = TSNE(n_components=2).fit_transform(data_pca)
# pd.DataFrame(data_embedded).to_csv("data_input/data_mnist.csv")
# end = time.time()
#
# print(end-start)

# dr_data = read_data.iloc[:,:3]
# t = dr_data.sort_values(by='l')
# t.to_csv('data_input/cube/cube2_up_light_labels_sort.csv',index=False)
# print(dr_data.head())

# read_data = pd.read_csv('data_input/mnist_train.csv',header=None)
# t = read_data.sort_values(by=read_data.columns[0])
# t.iloc[:,1:].to_csv('data_input/origin/mnist.csv',index=False)

# 1k
# start = time.time()
# read_data = pd.read_csv('data_input/origin/1k.csv')
# data_embedded = TSNE(n_components=2).fit_transform(read_data)
# pd.DataFrame(data_embedded).to_csv("data_input/data_1k.csv",index=False)
# end = time.time()
# print(end-start)

# Cube
start = time.time()
read_data = pd.read_csv('data_input/older/embedded2.csv')
# data_embedded = TSNE(n_components=2).fit_transform(read_data)
read_data.iloc[:,1:].to_csv("data_input/mnist_order.csv",index=False)
end = time.time()
print(end-start)
