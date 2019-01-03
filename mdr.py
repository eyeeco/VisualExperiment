import numpy as np
import pandas as pd
import os

from bokeh.models import ColumnDataSource, Button
from bokeh.layouts import row, column
from bokeh.plotting import figure, curdoc
from bokeh.models.widgets import TextInput

from utils import InfoManager, TestAcc
from getData import getData
from sklearn.manifold import TSNE, Isomap
from sklearn.decomposition import PCA

# 选择实验项目
data_ori, data_f, data_l, item = getData(kind=3)

# 取得参数
info = InfoManager(data_f, data_l, 2)
data1, labels1, size1, colors1 = info.get_info(1, 5)
data2, labels2, size2, colors2 = info.get_info(0, 20)
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
    label_save.iloc[list_selected,0] = mark
    label_save.to_csv(out_path+'/'+usr_name+'.csv',index_label='id')
    TestAcc(label_save.values, labels1)

t = 0

def Callback():
    global colors1
    global t
    global pre_selected1, pre_selected2
    selected1 = source1.selected['1d']['indices']
    selected2 = source2.selected['1d']['indices']
    if selected1 and selected2:
        if t:
            selected1 = np.array(pre_selected1)[selected1]
            selected2 = np.array(pre_selected2)[selected2]
            t = 0
        res_label = np.bincount(labels2[selected2].astype('int'))
        max_label = np.sort(res_label)[-1]
        if len(res_label>0) and max_label < np.sum(res_label) * 0.8:
            data_ch1 = data1_ori[selected1]
            data_ch2 = data2_ori[selected2]
            pre_selected1 = selected1
            pre_selected2 = selected2
            t = 1
            data_ch = np.vstack([data_ch1, data_ch2])
            count_1 = len(data_ch1)
            data_emb = TSNE(n_components=2).fit_transform(data_ch)
            data1_l = data_emb[:count_1].T
            data2_l = data_emb[count_1:].T
            source1.data = dict(x=data1_l[0],y=data1_l[1], fill_color=colors1[selected1], size=size1[selected1])
            source2.data = dict(x=data2_l[0],y=data2_l[1], fill_color=colors2[selected2], size=size2[selected2])
        else:
            ca = np.argmax(res_label)
            for i in selected1:
                colors1[i] = color[ca]
            source1.data = dict(x=data1[0],y=data1[1], fill_color=colors1, size=size1)
            source2.data = dict(x=data2[0],y=data2[1], fill_color=colors2, size=size2)
            Writedata(ca,selected1)

# 插件及布局
button = Button(label="确定")
button.on_click(Callback)
root = column(row(director,button),pic)
curdoc().add_root(root)
