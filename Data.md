# 数据集说明


- title_system_0: 包含政策标题，发文部门，对应标签为政策类别，标签中不含有‘其他’类
- title_system_1: 包含政策标题，发文部门，对应标签为政策类别, 标签只有‘其他’类
  - others_predict_result.jsonl为不包含其他类的模型对title_system_0数据进行训练的模型，在title_system_1上预测的结果
  - merge_preditc_sample.jsonl为预测结果加入tilte_system_1之后的合并文件，多出了预测标签和相应分数两个字段
  - filter_merged_{condition}.jsonl文件为对merge_preditc_sample.jsonl中数据进行筛选之后的结果，如filter_merged_low_score_0.5.jsonl包含预测标签值小于0.5的样本。
- title_system_2: 筛选title_system_1/filter_merged_low_score_0.5.jsonl中的可以作为真正'其他'类的数据，加入到title_system_0中进行训练，这一步目的是为了模型输出时能包含其他类，因为之前使用tilte_system_0训练时无法输出其他类
  - train_data_with_pesudo_others.jsonl: 将’其他‘类作为伪标签，训练出一个包含可以预测’其他‘类的模型