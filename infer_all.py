# Copyright The PyTorch Lightning team.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import json
import os
from datetime import datetime
from typing import Any, Dict, List, Optional

import hydra
import tqdm
from datasets.load import load_dataset
from hydra.utils import get_class
from omegaconf import DictConfig, OmegaConf
from pytorch_lightning.utilities.distributed import rank_zero_info

from lightning_transformers.core.config import TaskConfig
from lightning_transformers.core.instantiator import HydraInstantiator, Instantiator
from lightning_transformers.core.nlp import HFTokenizerConfig, HFTransformer


def run(
    dataset_path: Any,
    input_fields: List[str],
    instantiator: Instantiator,
    checkpoint_path: Optional[str] = None,
    task: TaskConfig = TaskConfig(),
    model_data_kwargs: Optional[Dict[str, Any]] = None,
    tokenizer: Optional[HFTokenizerConfig] = None,
    pipeline_kwargs: Optional[dict] = None,  # mostly for the device
    predict_kwargs: Optional[dict] = None,
) -> List[Dict[str, Any]]:
    model: HFTransformer
    if checkpoint_path:
        model = get_class(task._target_).load_from_checkpoint(checkpoint_path)
    else:
        model = instantiator.model(task,
                                   model_data_kwargs=model_data_kwargs,
                                   tokenizer=tokenizer,
                                   pipeline_kwargs=pipeline_kwargs)

    predict_kwargs = predict_kwargs or {}
    dataset = load_dataset(dataset_path)
    # create output data file
    filename = "output-{}.json".format(datetime.now())
    with open(os.path.join(os.getcwd(), filename), "w+",
              encoding="utf-8") as save_fobj:
        for sample in tqdm.tqdm(dataset):
            out = model.hf_pipeline(
                ''.join(sample[input_field] for input_field in input_fields),
                **predict_kwargs)
            sample['scores'] = out
            save_fobj.write(json.dumps(sample, ensure_ascii=False) + '\n')


def main(cfg: DictConfig) -> Any:
    rank_zero_info(OmegaConf.to_yaml(cfg))
    instantiator = HydraInstantiator()
    y = run(
        cfg.dataset_path,
        cfg.input_fields,
        instantiator,
        checkpoint_path=cfg.get("checkpoint_path"),
        task=cfg.task,
        model_data_kwargs=cfg.get("model_data_kwargs"),
        tokenizer=cfg.get("tokenizer"),
        pipeline_kwargs=cfg.get("pipeline_kwargs", {}),
        predict_kwargs=cfg.get("predict_kwargs", {}),
    )
    rank_zero_info(y)
    return y


@hydra.main(config_path="../../conf", config_name="config")
def hydra_entry(cfg: DictConfig) -> None:
    main(cfg)


if __name__ == "__main__":
    hydra_entry()
