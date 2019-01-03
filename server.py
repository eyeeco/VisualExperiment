from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return '''
<div style="text-align:center">
<p1>格式塔感知实验</p1>
<p><a href='http://192.168.3.2:5006/2moons' target='_blank'>实验一：双月数据集实验</a><p>
<p><a href='http://192.168.3.2:5007/4circles' target='_blank'>实验二：四类物体遮挡实验</a><p>
<p><a href='http://192.168.3.2:5008/mnist_deep1' target='_blank'>实验三：手写体数据集实验1</a><p>
<p><a href='http://192.168.3.2:5009/mnist_deep2' target='_blank'>实验四：手写体数据集实验2</a><p>
<p><a href='http://192.168.3.2:5010/mnist_deep3' target='_blank'>实验五：手写体数据集实验3</a><p>
</div>
'''

app.run(host='0.0.0.0',port=9999)
