# Experiment

## 政策级别分类

这部分主要作用于短文本分类，即爬取数据的`title`部分。
该部分分类除`国家级`这一类别之外，其他类别比较平衡。

### 实验一

本次实验的文件位于[outputs](archive/policy_level/experiment_01)下，模型为roberta-wwm-chinese-ext, 具体的超参数和模型文件可以查看保存的tensorboard。

实验的目的是为了做一次快速验证，之前已经在超长文本上耽误很多时间了，这次把决定在短文本做实验。

数据放在[data](data)下，细分目录对应于上面的output。数据这回是采用随机分的，可能不太理想，
最终的训练结果在**0.78**左右，列举一下问题和解决方案：
1. 数据不平衡导致，考虑对`国家级`类别数据做数据增强，方案参考[nlpcda](https://github.com/425776024/nlpcda)，[EDA_NLP_for_Chinese](https://github.com/zhanlaoban/EDA_NLP_for_Chinese)和[从理论到实践解决文本分类中的样本不均衡问题](https://zhuanlan.zhihu.com/p/361152151), 其次考虑单独对国家级做二元分类器
2. 数据集本身是1-fold，考虑增强以后做5-fold的多模型融合
3. 微平均导致metric表示有所问题，参考[分类器的评价指标](https://zhuanlan.zhihu.com/p/268927444)和[A review on evaluation metrics for data classification evaluations](https://www.academia.edu/download/37219940/5215ijdkp01.pdf)
4. 考虑特征融合，这个优先级最低

### 实验二

由于之前误将UUID和title两个字段拼接到一起了，导致实验二一直处于排查错误的阶段，这次训练主要是针对数据样本做分层5折交叉训练，并且将department这一字段加在了title字段的后面，作为输入进行训练。训练效果比意向中的好不少，F1值最高直接达到了**0.952**，至于剩下0.05的问题，一方面是部分样本还是存在标错的原因，具体查看了几个样例，确实存在，但还是比较少，后期用模型跑一遍全样本挑错误case出来就行了。

另外需要注意的是由于国家级的样本数量实在太少了，这次没有将国家级加入训练。解决方法是学弟提供的思路，他们在做知识图谱的时候发现国务院存在公开数据。我沿着他们的调研方向继续往下走，找到了官方调研报告：[2021年政府政务数据调研报告](http://www.cesi.cn/images/editor/20211103/20211103155731200.pdf)。继续找下去应该能解决我们数据缺少的问题。

实验结果参考目录[实验二](archive/policy_system/experiment_02)

实验模型见服务器上[保存模型](outputs/2021-12-25/20-37-45)

## 政策条线分类

### 实验一


