import json
import jsonlines
from typing import AnyStr, Callable

from torch import threshold


def convert_josn_2_jsonl(json_path: AnyStr, jsonl_path: AnyStr):
    """convert json file to jsonlines file.

    Args:
        json_path (AnyStr): input file
        jsonl_path (AnyStr): output file
    """
    with jsonlines.open(jsonl_path, mode='w') as writer:
        with open(json_path, encoding='utf8') as f:
            writer.write_all(json.load(f))


def merget_predict_into_sample(sample_path: AnyStr, result_path: AnyStr,
                               output_path: AnyStr):
    """将预测结果输出到文件中

    Args:
        sample_path (AnyStr): 样本数据路径，样本应为jsonl格式
        result_path (AnyStr): 结果数据路径，结果应为jsonl格式，其形如`{"label": "label_1", "score": score}`
        output_path (AnyStr): 输出文件，结果为jsonl
    """

    samples = jsonlines.open(sample_path)
    results = jsonlines.open(result_path)
    output = jsonlines.open(output_path, mode='w')

    for sample, result in zip(samples, results):
        sample['predict'] = result['label']
        sample['score'] = result['score']
        output.write(sample)


def filter_file(input_path: AnyStr, output_path: AnyStr,
                callback: Callable[[], bool], *args, **kwargs):
    with jsonlines.open(input_path) as reader:
        with jsonlines.open(output_path, mode='w') as writer:
            for json_data in reader:
                if callback(json_data, *args, **kwargs):
                    writer.write(json_data)
