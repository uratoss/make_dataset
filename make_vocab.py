#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import argparse
import neologdn

import MeCab
import pandas as pd
import subprocess

from parse import parse

# class PandasTagger(MeCab.Tagger){{{
class PandasTagger(MeCab.Tagger):
    def __init__(self, option=""):
        super().__init__(option)
        self.columns = [
            "表層形",
            "品詞",
            "品詞細分類1",
            "品詞細分類2",
            "品詞細分類3",
            "活用型",
            "活用形",
            "原形",
            "読み",
            "発音",
        ]

    def pandas_parse(self, text):
        results = []
        for line in self.parse(text).split("\n"):
            if line == "EOS":
                break
            surface, feature = line.split("\t")
            feature = [None if f == "*" else f for f in feature.split(",")]
            results.append([surface] + feature)
        return pd.DataFrame(results, columns=self.columns)


# }}}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("files", help="files that you want to add vocabuary", nargs="*")
    parser.add_argument(
        "-o", "--out_dir", default="./", help="output directory path of precessed file"
    )
    args = parser.parse_args()

    dicdir = (
        subprocess.run(
            ["mecab-config", "--dicdir"], encoding="utf-8", stdout=subprocess.PIPE
        ).stdout.strip()
        + "/mecab-ipadic-neologd"
    )
    tagger = PandasTagger("-d " + dicdir + ' -U %m"\t"%H,*,*"\n"')

    out_dir = args.out_dir
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    base_dir = os.path.join(out_dir, "base")
    os.makedirs(base_dir)
    surf_dir = os.path.join(out_dir, "surf")
    os.makedirs(surf_dir)

    vocab_list = None
    for file_path in args.files:
        normalized = neologdn.normalize(open(file_path).read())

        parsed = parse(normalized, mode="morph")
        with open(os.path.join(surf_dir, os.path.basename(file_path)), "w") as f:
            print("\n".join(parsed), file=f)
        parsed = parse(normalized, mode="morph_base")
        with open(os.path.join(base_dir, os.path.basename(file_path)), "w") as f:
            print("\n".join(parsed), file=f)

        df = tagger.pandas_parse(open(file_path).read())
        vocab_list = df if vocab_list is None else vocab_list.append(df)
    vocab_list.drop_duplicates().reset_index(drop=True).to_csv(
        os.path.join(out_dir, "vocab.csv")
    )
