import numpy as np
import pandas as pd

class InfoManager:
    """
    get the information for Bokeh Application
    """
    color = np.array(['#899933','black','green','red','blue','#339989','#89ffed','pink','#7D26CD','grey','white'])

    def __init__(self, data_f, data_l, points=1):
        self.data_f = data_f
        self.data_l = data_l
        self.points = points

    def get_basic(self):
        data_length = len(self.data_f)
        interval = data_length//(len(np.bincount(self.data_l)) * self.points )
        label_order = [x for x in range(data_length)][::interval]
        label_order = [x for x in label_order]
        data_order = [x for x in range(data_length) if x not in label_order]
        return data_order, label_order

    def get_info(self, role=1, size_t=5):
        data_order, label_order = self.get_basic()
        if role == 1:
            length = len(data_order)
            data = self.data_f[data_order].T
            label = np.array([int(x) for x in self.data_l[data_order]])
            size = np.repeat(size_t, length)
            colors = np.repeat(InfoManager.color[10], length)
            return data, label, size, colors
        else :
            length = len(label_order)
            data = self.data_f[label_order].T
            label = np.array([int(x) for x in self.data_l[label_order]])
            size = np.repeat(size_t, length)
            colors = InfoManager.color[label]
            return data, label, size, colors

def TestAcc(exp, truth):
    count = 0
    label_length = 0
    for i in range(len(truth)):
        if exp[i] != -1:
            label_length += 1
        if truth[i] == exp[i] :
            count += 1

    print("标记准确率：(只计算标记过的样本)", count/label_length)
    print("标记准确率：(全部样本)", count/len(truth))
    return label_length
