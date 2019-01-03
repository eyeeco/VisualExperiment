## An VisualExperiment
图像分类任务中，为了获取标签，一种可行的办法是运用标签传播的策略。
即在一个数据集中标记少量标签，继而通过元素间的相关性使得计算机为这些数据打上标签。
但是标记传播本身有很大局限性。
首先，标签传播需要计算元素的大量元素相关关系，这种计算消耗在数据量较大时会十分昂贵；
其次，标签传播的正确率并不能令人满意，而且极易被相邻的元素误导；
标签传播还存在着参数敏感、密度敏感等许多问题。

为了获取需要的标签，可视化交互是该问题的一个很好的解决方案。
从用户的角度出发，利用格式塔心理学指导下用户的感性认知对图形进行判断而完成需要的标签任务。
该实验以用户标签为基础进行，招募志愿者进行标签实验。
每个实验者都会产生一组实验数据，表示对某个数据集的标签情况，在实验结束后，对这些实验数据处理：

1. 考察这些标签的正确率
2. 将这些人工标签放入卷积神经网络中进行训练，考察训练样本的正确率
3. 考察实验样本之间统计学规律，探究实验数据的鲁棒性

## Envirment
* python3.6
* numpy (1.14.0)
* pandas (0.22.0)
* scikit-learn (0.19.1)
* bokeh (0.12.13)

## Instruct
bokeh serve appname --address 0.0.0.0 --allow-websocket-origin= ip : port

ie:

bokeh serve mnist_deep.py --address 0.0.0.0 --allow-websocket-origin=192.168.23.134:5006