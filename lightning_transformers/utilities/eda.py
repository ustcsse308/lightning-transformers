import argparse

from nlpcda import Simbert

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--filepath")
parser.add_argument("-a", "--action")
parser.add_argument("-tc", "--target_class")


def augmentation(filepath, target_class: str):
    f_obj = open(filepath, "r", encoding='utf-8')


_config = {
    'model_path':
    'E:\ZacBi\Download\Compressed\chinese_simbert_L-12_H-768_A-12',
    'CUDA_VISIBLE_DEVICES': '0',
    'max_len': 64,
    'seed': 1
}


def augmentation_simbert(text: str, config: dict, create_num: int):
    simbert = Simbert(config=config)
    synonyms = simbert.replace(sent=text, create_num=create_num)
    return synonyms


if __name__ == "__main__":
    a = augmentation_simbert('把我的一个亿存银行安全吗', _config, 5)
    for c in a:
        print(c)