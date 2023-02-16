#!/usr/bin/env python3

"""
Creates a "training set" and "test set" from word/description pairs
pulled from the code from AAAI-20 paper "Multi-channel Reverse Dictionary Model"
See https://github.com/thunlp/MultiRD for data and download the data into
this directory.  The file data_desc_c.json is the only one used here.

(Note:  This data set is originally from Hill, et al (https://arxiv.org/abs/1504.00548)
but the above paper, which uses the data set, is the only downloadble version I could
find.)
"""

import json

f = open("data_desc_c.json").read()

with open("data/train.jsonl", "w") as fs_train:
    with open("data/test.jsonl", "w") as fs_test:
        for i, record in enumerate(json.loads(f)):
            fs = (i < 100) and fs_train or fs_test
            print(
                json.dumps(
                    {"word": record["word"], "definition": record["definitions"]}
                ),
                file=fs,
            )
