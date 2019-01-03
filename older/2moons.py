import numpy as np
import pandas as pd


from bokeh.layouts import row
from bokeh.plotting import figure, curdoc
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Button,  CDSView, IndexFilter
from bokeh.models.widgets import Slider, Select, TextInput

#  cube 的参数
path_ori = "data_input/cube/cube.csv"
data_ori = pd.read_csv(path_ori).iloc[:,:3].values
data_l = pd.read_csv(path_ori).iloc[:,3].values
path_gen = "data_input/data_"+path_ori.split("/")[-1].split(".")[0]+".csv"

data_f = pd.read_csv(path_gen).values
data_embedded = data_f.T

size = np.repeat(10, len(data_f))
color = np.array(['#09eeee','black','green','red','blue','#339989','#89ffed','pink','#7D26CD','grey','white'])
colors = color[data_l]

# bokeh 绘图
source = ColumnDataSource(data=dict(x=data_embedded[0], y=data_embedded[1], fill_color=colors, size=size))
TOOLS="reset,lasso_select"
p1 = figure(tools=TOOLS,active_drag="lasso_select",plot_width=1000,plot_height=1000)
r = p1.circle(x='x',y='y',source=source,fill_color='fill_color',size='size')
director = TextInput(title="请输入实验者 序号_姓名(拼音)")

def callback():
    global colors
    selected = source.selected['1d']['indices']
    print(selected)
    print(data_ori[selected])

# 选择插件及布局
button = Button(label="确定")
button.on_click(callback)
root = column(director,button,p1)
curdoc().add_root(root)
