import numpy as np
import pandas as pd

import os

def getData(kind=1):
    if kind ==1 :
        path_ori = "data_input/cube/cube.csv"
        data_ori = pd.read_csv(path_ori).iloc[:,:3].values
        data_l = pd.read_csv(path_ori).iloc[:,3].values
    elif kind ==2:
        path_ori = "data_input/origin/1k.csv"
        data_l = np.repeat(range(10),100)
        data_ori = pd.read_csv(path_ori).values
    elif kind  == 3:
        path_ori = "data_input/origin/mnist.csv"
        data_f = pd.read_csv(path_ori).values
        data_l = np.repeat(range(10),6000)
        data_ori = data_f

    item = path_ori.split("/")[-1].split(".")[0]
    path_gen = "data_input/data_"+ item +".csv"
    if not os.path.exists(path_gen):
        # 第一次调用
        read_data = pd.read_csv(path_ori)
        data_embedded = TSNE(n_components=2).fit_transform(read_data)
        pd.DataFrame(data_embedded).to_csv(path_gen,index=False)
    data_f = pd.read_csv(path_gen).values
    return data_ori, data_f, data_l, item
