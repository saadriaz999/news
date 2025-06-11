---
license: apache-2.0
tags:
- generated_from_trainer
datasets:
- cnn_dailymail
model-index:
- name: flan-t5-small-cnn_dailymail
  results: []
---

<!-- This model card has been generated automatically according to the information the Trainer had access to. You
should probably proofread and complete it, then remove this comment. -->

# flan-t5-small-cnn_dailymail

This model is a fine-tuned version of [google/flan-t5-small](https://huggingface.co/google/flan-t5-small) on the cnn_dailymail dataset.
It achieves the following results on the evaluation set:
- eval_loss: 1.7942
- eval_rouge1: 24.347
- eval_rouge2: 11.4242
- eval_rougeL: 20.0736
- eval_rougeLsum: 22.8723
- eval_gen_len: 18.9995
- eval_runtime: 492.0285
- eval_samples_per_second: 23.352
- eval_steps_per_second: 3.892
- epoch: 4.11
- step: 196452

## Model description

More information needed

## Intended uses & limitations

More information needed

## Training and evaluation data

More information needed

## Training procedure

### Training hyperparameters

The following hyperparameters were used during training:
- learning_rate: 5e-05
- train_batch_size: 6
- eval_batch_size: 6
- seed: 42
- optimizer: Adam with betas=(0.9,0.999) and epsilon=1e-08
- lr_scheduler_type: linear
- num_epochs: 10.0

### Framework versions

- Transformers 4.26.1
- Pytorch 1.11.0
- Datasets 2.10.1
- Tokenizers 0.13.2
