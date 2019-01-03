import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
from sklearn.decomposition import TruncatedSVD
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

from mxnet import gluon
import sys
sys.path.append('..')
import utils


def DRvisual(mnist=0, data_input='embedded'):
    # 1 准备数据，将mxnet的数据集转换成需要的格式
    if mnist == 0:
        # 1.1 MNIST手写体数据集的准备
        mnist_train = gluon.data.vision.MNIST(train=True, transform=None)
        mnist_test = gluon.data.vision.MNIST(train=False, transform=None)
        data = mnist_train[:][0].asnumpy().reshape(60000,784)
        label = mnist_train[:][1]
    elif mnist == 1:
        # 1.2 FAshionMNIST 数据集的准备
        mnist_train = gluon.data.vision.FashionMNIST(train=True, transform=None)
        mnist_test = gluon.data.vision.FashionMNIST(train=False, transform=None)
        data = mnist_train[:][0].asnumpy().reshape(60000,784)
        label = mnist_train[:][1]

    # 2 降维可视化 经pca降维后将数据降到2维可视化
    # 2.1 降维过程
    # pca预降维
    pca = PCA(n_components=50)
    data_pca = pca.fit_transform(data)
    # svd预降维
    svd = TruncatedSVD(n_components=50)
    data_svd = svd.fit_transform(data)
    # t-SNE 降维
    data_embedded = TSNE(n_components=2).fit_transform(data_pca)
    # 2.2 储存降维后的数据供可视化接口使用
    res = np.column_stack((data_embedded,label))
    pd.DataFrame(res).to_csv('data_input/'+data_input+'.csv')
