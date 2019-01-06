from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return '''
<div style="text-align:center">
<p1>感知交互实验</p1>
<p><a href='http://10.7.15.44:5007/window' target='_blank'>实验一：1K数据集实验(SIDR, 每类标记 1)</a><p>
<p><a href='http://10.7.15.44:5008/window' target='_blank'>实验一：1K数据集实验(MIDR, 每类标记 1)</a><p>
<p><a href='http://10.7.15.44:5009/window' target='_blank'>实验一：1K数据集实验(SIDR, 每类标记 1)</a><p>
<p><a href='http://10.7.15.44:5010/window' target='_blank'>实验一：1K数据集实验(MIDR, 每类标记 2)</a><p>
<p><a href='http://10.7.15.44:5011/window' target='_blank'>实验二：魔方数据集实验(SIDR, 每类标记 2)</a><p>
<p><a href='http://10.7.15.44:5012/window' target='_blank'>实验二：魔方数据集实验(MIDR, 每类标记 5)</a><p>
<p><a href='http://10.7.15.44:5013/window' target='_blank'>实验二：魔方数据集实验(SIDR, 每类标记 2)</a><p>
<p><a href='http://10.7.15.44:5014/window' target='_blank'>实验二：魔方数据集实验(MIDR, 每类标记 5)</a><p>
<p><a href='http://10.7.15.44:5015/window' target='_blank'>实验三：MNIST数据集实验(SIDR, 每类标记 3)</a><p>
<p><a href='http://10.7.15.44:5016/window' target='_blank'>实验三: MNIST数据集实验(SIDR, 每类标记 3)</a><p>
</div>
'''

app.run(host='0.0.0.0',port=9999)
