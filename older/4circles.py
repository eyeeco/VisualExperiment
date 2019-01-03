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

# 在外面跑好的数据
read_data = pd.read_csv('data_input/cross.csv',header=None,dtype=np.float)
data_test = read_data.iloc[:,:3].values
labels_ori = np.squeeze(read_data.iloc[:,3:].values)
labels = labels_ori
# pca预降维
data_pca = PCA(n_components=2).fit_transform(data_test)

data_embedded = data_pca

data = pd.DataFrame(data=[-1 for i in range(len(data_embedded))],columns=['label'])

# 抽样 2% 标记样本
color = np.array(['#ee0909','black','green','red','blue','#339989','#89ffed','pink','#7D26CD','grey'])
data_length = len(read_data)
colors = np.repeat('white',data_length)
size = np.repeat(10,data_length)
row = (data_length * np.random.rand(data_length//100)).astype('int')
mark = labels[row].astype('int')
colors[row] = color[mark]
size[row] = 20

# bokeh 绘图
source = ColumnDataSource(data=dict(x=data_embedded[:,0], y=data_embedded[:,1], fill_color=colors, size=size))
source2 = ColumnDataSource(data=dict(x=data_embedded[row,0], y=data_embedded[row,1], fill_color=colors[row], size=size[row]//2))
TOOLS="reset,lasso_select"
p1 = figure(tools=TOOLS,active_drag="lasso_select",plot_width=1000,plot_height=1000)
r1 = p1.circle(x='x',y='y',source=source,fill_color='fill_color',size='size')
p2 = figure(tools=TOOLS,plot_width=500,plot_height=500)
r2 = p2.circle(x='x',y='y',source=source2,fill_color='fill_color',size='size')
director = TextInput(title="请输入实验者 序号_姓名(拼音)")

# 回调函数和数据写入
def writeData(mark=-1,list_selected=[]):
    usr_name = director.value.strip()
    if not usr_name:
        usr_name = 'origin'
    data.iloc[list_selected,0] = mark
    data.to_csv('data_output/4circles/'+usr_name+'.csv')

def callback():
    global colors
    global labels
    selected = source.selected['1d']['indices']
    res_label = np.sort(np.bincount(labels[selected].astype('int')))
    if selected:
        if len(res_label)>1 and res_label[-1] < np.sum(res_label) * 0.8:
            data_mini = data_test[selected]
            data_pca = PCA(n_components=2).fit_transform(data_mini)
            labels = labels[selected]
            source.data = dict(x=data_pca[:,0],y=data_pca[:,1], fill_color=colors[selected], size=size[selected])
        else:
            ca = np.argmax(res_label)
            for i in selected:
                colors[i] = color[ca]
            labels = labels_ori
            source.data = dict(x=data_embedded[:,0],y=data_embedded[:,1], fill_color=colors, size=size)
            writeData(ca,selected)

# 选择插件及布局
button = Button(label="确定")
button.on_click(callback)
root = column(column(director,button),column(p1,p2))
curdoc().add_root(root)
