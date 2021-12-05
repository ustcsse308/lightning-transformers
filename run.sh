#!/bin/sh
export DATAPATH="/bdata1/pc/github/private/lightning-transformers/data"

python train.py task=nlp/text_classification \
    dataset.cfg.train_file=$DATAPATH/train.json \
    dataset.cfg.validation_file=$DATAPATH/valid.json \
    dataset.cfg.test_file=$DATAPATH/test.json \
    backbone.pretrained_model_name_or_path="hfl/chinese-roberta-wwm-ext" \
    trainer.precision=16 \
    trainer.gpus=[2,3] \
    trainer.max_epochs=40 \
    log=True \
    +auto_scale_batch_size=True \
    +trainer/logger=tensorboard
