import numpy as np
import pandas as pd

read_data = pd.read_csv('data_output/data_cube1_dark/results.csv')
read_exp = pd.read_csv('data_output/data_cube1_dark/origin.csv')
exp = np.squeeze(read_exp.iloc[:,1:])
truth = np.squeeze(read_data.iloc[:,1:])

count = 0
label_length = 0
for i in range(len(truth)):
    if exp[i] != -1:
        label_length += 1
    if truth[i] == exp[i] :
        count += 1

print("标记准确率：(只计算标记过的样本)", count/label_length)
print("标记准确率：(全部样本)", count/len(truth))
