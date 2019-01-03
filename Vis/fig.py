import numpy as np
import pandas as pd

from mpl_toolkits import mplot3d
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt

read_data = pd.read_csv('data_input/labels_cube1_cube2/cube2_up_light_hsv_feature.csv',header=None)
data_order = read_data[3]!=-1
label_order = read_data[3]==-1
data_ori = np.squeeze(read_data.iloc[:,:-2].values)
labels = np.squeeze(read_data.iloc[:,-2].values)

data1 = data_ori[data_order].T
labels = labels[data_order]
data2 = data_ori[label_order].T
color = np.array(['green','black','pink','red','grey','blue'])
colors1 = color[labels]

fig = plt.figure()
ax = plt.axes(projection='3d')


zdata = data1[0]
xdata = data1[1]
ydata = data1[2]
ax.scatter3D(xdata,ydata,zdata,c=colors1,s=100)


zdata = data2[0]
xdata = data2[1]
ydata = data2[2]
ax.scatter3D(xdata,ydata,zdata,c='#D3A4FF')

plt.show()
