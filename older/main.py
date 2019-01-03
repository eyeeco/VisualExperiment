import numpy as np
import pandas as pd

from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
from sklearn.decomposition import TruncatedSVD
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

from bokeh.layouts import row
from bokeh.plotting import figure, curdoc
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Button,  CDSView, IndexFilter
from bokeh.models.widgets import Slider, Select, TextInput

# 静态资源
color = np.array(['#09eeee','black','green','red','blue','#339989','#89ffed','pink','#7D26CD','grey','white'])

# 读入数据的特征和标记
# read_data = pd.read_csv('data_input/embedded2.csv')
# data_f = np.squeeze(read_data.iloc[:,1:3].values)
# data_l = np.squeeze(read_data.iloc[:,3:])

read_data = pd.read_csv('data_input/data_1k.csv')
data_f = np.squeeze(read_data.values)
data_l = np.repeat(range(10),100)



info = InfoManager(data_f, data_l, 1)
data1, labels1, size1, colors1 = info.get_info(1, 5)
data2, labels2, size2, colors2 = info.get_info(0, 20)


# 存放实验数据
label_save = pd.DataFrame(np.repeat(-1,len(labels1)), columns=['label'])
pd.DataFrame(labels1).to_csv('data_output/mnist2/results.csv')

# # 分离标记与非标记样本
# data_length = len(data_f)
# interval = data_length//(10 * points)
# label_order = [x for x in range(data_length)][::interval]
# data_order = [x for x in range(data_length) if x not in label_order]
# data1_length = len(data_order)
# data2_length = len(label_order)
#
# # 分别将训练样本和测试样本的各项参数写开
# data1 = data_f[data_order].T
# data2 = data_f[label_order].T
# labels1 = np.array([int(x) for x in data_l[data_order]])
# labels2 = np.array([int(x) for x in data_l[label_order]])
# size1 = np.repeat(5, data1_length)
# size2 = np.repeat(20, data2_length)
# colors1 = np.repeat('white', data1_length)
# colors2 = color[labels2]

# Bokeh 绘图
source1 = ColumnDataSource(data=dict(x=data1[0], y=data1[1], fill_color=colors1, size=size1))
source2 = ColumnDataSource(data=dict(x=data2[0], y=data2[1], fill_color=colors2, size=size2))
TOOLS="reset,lasso_select"
pic = figure(tools=TOOLS,active_drag="lasso_select",plot_width=1000,plot_height=1000)
clr1 = pic.circle(x='x',y='y',source=source1,fill_color='fill_color',size='size')
clr2 = pic.circle(x='x',y='y',source=source2,fill_color='fill_color',size='size')
director = TextInput(title="请输入实验者 姓名(拼音)")


# 回调函数和数据写入
def writeData(mark=-1,list_selected=[]):
    usr_name = director.value.strip()
    if not usr_name:
        usr_name = 'origin'
    label_save.iloc[list_selected,0] = mark
    label_save.to_csv('data_output/mnist2/'+usr_name+'.csv')

def callback():
    global colors1
    selected1 = source1.selected['1d']['indices']
    selected2 = source2.selected['1d']['indices']
    if selected1 and selected2:
        print(selected2)
        ca = np.argmax(np.bincount(labels2[selected2].astype('int')))
        for i in selected1:
            colors1[i] = color[ca]
        source1.data = dict(x=data1[0],y=data1[1], fill_color=colors1, size=size1)
        writeData(ca,selected1)

# 选择插件及布局
button = Button(label="确定")
button.on_click(callback)
root = column(director,button,pic)
curdoc().add_root(root)
