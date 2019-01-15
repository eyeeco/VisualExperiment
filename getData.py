import numpy as np
import pandas as pd

import os
from sklearn.manifold import TSNE

def getDataf(path_ori):
    item = path_ori.split("/")[-1].split(".")[0]
    path_gen = "data_input/data_"+ item +".csv"
    if not os.path.exists(path_gen):
        # 第一次调用
        read_data = pd.read_csv(path_ori)
        data_embedded = TSNE(n_components=2).fit_transform(read_data)
        pd.DataFrame(data_embedded).to_csv(path_gen,index=False)
    data_f = pd.read_csv(path_gen).values
    return data_f, item

def getData(kind=1):
    if kind ==1 :
        path_ori = "data_input/cube/cube.csv"
        data_ori = pd.read_csv(path_ori).iloc[:,:3].values
        data_l = pd.read_csv(path_ori).iloc[:,3].values
        data_f, item = getDataf(path_ori)
    elif kind ==2:
        path_ori = "data_input/origin/1k.csv"
        data_l = np.repeat(range(10),100)
        data_ori = pd.read_csv(path_ori).values
        data_f, item = getDataf(path_ori)
    elif kind == 3:
        item = 'mnist_order'
        path_gen = "data_input/data_"+ item +".csv"
        data_f = pd.read_csv(path_gen).iloc[:,:2].values
        data_ori = data_f
        data_l = pd.read_csv(path_gen).iloc[:,2].values.astype(int)
    return data_ori, data_f, data_l, item
