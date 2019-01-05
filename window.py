import numpy as np
import pandas as pd
import os
from os.path import join, dirname

from bokeh.models import ColumnDataSource, Button, Div
from bokeh.layouts import layout, widgetbox
from bokeh.layouts import row, column
from bokeh.plotting import figure, curdoc
from bokeh.models.widgets import TextInput, Slider

from utils import InfoManager, TestAcc
from getData import getData
from sklearn.manifold import TSNE

# 选择实验项目
data_ori, data_f, data_l, item = getData(kind=1)

# 取得参数
info = InfoManager(data_f, data_l, 2)
data1, labels1, size1, colors1 = info.get_info(1, 5)
data2, labels2, size2, colors2 = info.get_info(0, 10)
# 准备二次降维的原始数据
data_order, label_order = info.get_basic()
data1_ori = data_ori[data_order]
data2_ori = data_ori[label_order]

#Bokeh 绘图
source1 = ColumnDataSource(data=dict(x=data1[0], y=data1[1], fill_color=colors1, size=size1))
source2 = ColumnDataSource(data=dict(x=data2[0], y=data2[1], fill_color=colors2, size=size2))
TOOLS="reset,lasso_select"
pic = figure(tools=TOOLS,active_drag="lasso_select",plot_width=1000,plot_height=1000)
clr1 = pic.circle(x='x',y='y',source=source1,fill_color='fill_color',size='size')
clr2 = pic.circle(x='x',y='y',source=source2,fill_color='fill_color',size='size')
director = TextInput(title="请输入实验者 姓名(拼音)")
reviews = Slider(title="标记点的形状大小", value=10, start=5, end=20, step=1)

# 静态资源
color = np.array(['#09eeee','black','green','red','blue','#339989','#89ffed','pink','#7D26CD','grey','white'])
label_save = pd.DataFrame(np.repeat(-1,len(labels1)), columns=['label'])
out_path = 'data_output/' + item
if not os.path.exists(out_path):
    os.makedirs(out_path)
pd.DataFrame(labels1,columns=['label']).to_csv(out_path+'/results.csv',index_label='id')

# 回调函数和数据写入
def Writedata(mark=-1,list_selected=[]):
    usr_name = director.value.strip()
    if not usr_name:
        usr_name = 'origin'
    if list_selected:
        label_save.iloc[list_selected,0] = mark
        label_save.to_csv(out_path+'/'+usr_name+'.csv',index_label='id')
        label_length = TestAcc(label_save.values, labels1)
    else:
        label_length = 0
    pic.title.text = "%d 点 已选择/ %d 点 待选择" %(label_length, len(label_save)-label_length)

t = 0

def Callback():
    global colors1
    selected1 = source1.selected['1d']['indices']
    selected2 = source2.selected['1d']['indices']
    if selected1 and selected2:
        res_label = np.bincount(labels2[selected2].astype('int'))
        ca = np.argmax(res_label)
        for i in selected1:
            colors1[i] = color[ca]
        source1.data = dict(x=data1[0],y=data1[1], fill_color=colors1, size=size1)
        source2.data = dict(x=data2[0],y=data2[1], fill_color=colors2, size=size2)
        Writedata(ca,selected1)

def update_plot():
    global size2
    size2 = np.repeat(reviews.value,len(size2))
    # source1.data = dict(x=data1[0],y=data1[1], fill_color=colors1, size=size1)
    source2.data = dict(x=data2[0],y=data2[1], fill_color=colors2, size=size2)

# 插件及布局
button = Button(label="确认选择")
button.on_click(Callback)
controls = [director, reviews, button]
desc = Div(text=open(join(dirname(__file__), "template.html")).read(), width=1500)
reviews.on_change('value', lambda attr, old, new: update_plot())
inputs = widgetbox(*controls, sizing_mode='scale_height')
l = layout([
    [desc],
    [pic, inputs],
], sizing_mode='fixed')

curdoc().add_root(l)
curdoc().title = "交互感知实验: "+item

Writedata()
