# Experiment

## 政策级别分类

这部分主要作用于短文本分类，即爬取数据的`title`部分。
该部分分类除`国家级`这一类别之外，其他类别比较平衡。

### 实验一

本次实验的文件位于[outputs](outputs/2021-12-04/03-02-33)下，模型为roberta-wwm-chinese-ext, 具体的超参数和模型文件可以查看保存的tensorboard。

实验的目的是为了做一次快速验证，之前已经在超长文本上耽误很多时间了，这次把决定在短文本做实验。

数据放在[data](data)下，细分目录对应于上面的output。数据这回是采用随机分的，可能不太理想，
最终的训练结果在0.78左右，列举一下问题和解决方案：
1. 数据不平衡导致，考虑对`国家级`类别数据做数据增强，方案参考[nlpcda](https://github.com/425776024/nlpcda)，[EDA_NLP_for_Chinese](https://github.com/zhanlaoban/EDA_NLP_for_Chinese)和[从理论到实践解决文本分类中的样本不均衡问题](https://zhuanlan.zhihu.com/p/361152151), 其次考虑单独对国家级做二元分类器
2. 数据集本身是1-fold，考虑增强以后做5-fold的多模型融合
3. 微平均导致metric表示有所问题，参考[分类器的评价指标](https://zhuanlan.zhihu.com/p/268927444)和[A review on evaluation metrics for data classification evaluations](https://www.academia.edu/download/37219940/5215ijdkp01.pdf)
4. 考虑特征融合，这个优先级最低

### 实验二