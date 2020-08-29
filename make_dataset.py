#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import argparse
import neologdn
import pickle
import numpy as np
import glob

from parse import parse
from mkvocab import mkvocab

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("files", help="files that you want to add vocabuary", nargs="*")
    parser.add_argument(
        "-o", "--out_path", default="./", help="output path of precessed file"
    )
    args = parser.parse_args()

    vocab = {"<PAD>": 0}
    rvocab = {0: "<PAD>"}
    xs = []
    ts = []
    chunk = 1
    for file_paths in args.files:
        files = glob.glob(file_paths)
        for file_name in files:
            parsed = [
                f.strip() for f in open(file_name).read().replace("\n", "").split("<P>")
            ]

            for i in range(len(parsed) - (chunk * 2 - 1)):
                x = ""
                for j in range(chunk):
                    x += parsed[i + j] + " "
                xs.append(x)
                y = ""
                for j in range(chunk):
                    y += parsed[i + chunk + j] + " "
                end_str = (
                    "<EOT> <EOS>" if (i + chunk + j + 1) > len(parsed) - 1 else "<EOS>"
                )
                ts.append(y + end_str)
    xs = "\n".join(xs)
    ts = "\n".join(ts)
    mkvocab(xs, vocab, rvocab)
    mkvocab(ts, vocab, rvocab)

    out_path = os.path.join(args.out_path, "vocab.txt")
    with open(out_path, "w") as f:
        print("\n".join(vocab), file=f)
    out_path = os.path.join(args.out_path, "vocab.dump")
    with open(out_path, "wb") as f:
        pickle.dump(vocab, f)
    out_path = os.path.join(args.out_path, "rvocab.dump")
    with open(out_path, "wb") as f:
        pickle.dump(rvocab, f)

    out_path = os.path.join(args.out_path, "x.txt")
    with open(out_path, "w") as f:
        print(xs, file=f)
    out_path = os.path.join(args.out_path, "t.txt")
    with open(out_path, "w") as f:
        print(ts, file=f)
