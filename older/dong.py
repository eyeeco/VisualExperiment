import numpy as np
import pandas as pd

from bokeh.layouts import row
from bokeh.plotting import figure, curdoc, show
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Button,  CDSView, IndexFilter
from bokeh.models.widgets import Slider, Select, TextInput

# 读入数据
read_data = pd.read_csv('data_input/data_em.csv')
data = np.squeeze(read_data.iloc[:,1:3].values)
data_order = read_data['data_order']
label_order = read_data['label_order']
labels = np.squeeze(read_data['labels'])

# 将标记与非标记分离，方便视觉观察
data1 = data[data_order]
data2 = data[label_order]
data1_length = len(data1)
data2_length = len(data2)

data1 = data1.T
data2 = data2.T
labels1 = labels[data_order].values
labels2 = labels[label_order].values
size1 = np.repeat(20,data1_length)
size2 = np.repeat(10,data2_length)
color = np.array(['green','black','pink','red','grey','blue'])
colors1 = color[labels1]
colors2 = np.repeat('white',data2_length)

# bokeh 项目
source1 = ColumnDataSource(data=dict(x=data1[0], y=data1[1], fill_color=colors1, size=size1))
source2 = ColumnDataSource(data=dict(x=data2[0], y=data2[1], fill_color=colors2, size=size2))
TOOLS="reset,lasso_select"
p1 = figure(tools=TOOLS,active_drag="lasso_select",plot_width=1000,plot_height=1000)
r = p1.circle(x='x',y='y',source=source1,fill_color='fill_color',size='size')
r2 = p1.circle(x='x',y='y',source=source2,fill_color='fill_color',size='size',fill_alpha=0.5)

# def callback():
#     global colors
#     selected = source1.selected['1d']['indices']
#     print(selected)

# 回调函数和数据写入
def writeData(mark=-1,list_selected=[]):
    label_save = pd.DataFrame(labels2)
    label_save.iloc[list_selected,0] = mark
    label_save.to_csv('data_output/dong2.csv')

def callback():
    global colors2
    selected = source1.selected['1d']['indices']
    selected2 = source2.selected['1d']['indices']
    print(selected)
    print(selected2)
    if selected and selected2:
        ca = np.argmax(np.bincount(labels1[selected].astype('int')))
        for i in selected2:
            colors2[i] = color[ca]
        source2.data = dict(x=data2[0],y=data2[1], fill_color=colors2, size=size2)
        writeData(ca,selected2)

# 选择插件及布局
button = Button(label="确定")
button.on_click(callback)
root = column(button,p1)
curdoc().add_root(root)
