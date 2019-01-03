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
read_data = pd.read_csv('data_input/embedded3.csv')
data_embedded = np.squeeze(read_data.iloc[:,1:3].values)
labels = np.squeeze(read_data.iloc[:,3:].values)
data = pd.DataFrame(data=[-1 for i in range(len(data_embedded))],columns=['label'])

# 抽样 2% 标记样本
color = np.array(['#ee0909','black','green','red','blue','#339989','#89ffed','pink','#7D26CD','grey'])
data_length = len(read_data)
colors = np.repeat('white',data_length)
size = np.repeat(5,data_length)
row = (data_length * np.random.rand(data_length//100)).astype('int')
mark = labels[row].astype('int')
colors[row] = color[mark]
size[row] = 10

# bokeh 绘图
source = ColumnDataSource(data=dict(x=data_embedded[:,0], y=data_embedded[:,1], fill_color=colors, size=size))
TOOLS="reset,lasso_select"
p1 = figure(tools=TOOLS,active_drag="lasso_select",plot_width=1000,plot_height=1000)
r = p1.circle(x='x',y='y',source=source,fill_color='fill_color',size='size')
director = TextInput(title="请输入实验者 序号_姓名(拼音)")

# 回调函数和数据写入
def writeData(mark=-1,list_selected=[]):
    usr_name = director.value.strip()
    if not usr_name:
        usr_name = 'origin'
    data.iloc[list_selected,0] = mark
    data.to_csv('data_output/mnist3/'+usr_name+'.csv')

def callback():
    global colors
    selected = source.selected['1d']['indices']
    if selected:
        ca = np.argmax(np.bincount(labels[selected].astype('int')))
        for i in selected:
            colors[i] = color[ca]
        source.data = dict(x=data_embedded[:,0],y=data_embedded[:,1], fill_color=colors, size=size)
        writeData(ca,selected)

# 选择插件及布局
button = Button(label="确定")
button.on_click(callback)
root = column(director,button,p1)
curdoc().add_root(root)
