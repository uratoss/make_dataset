#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import argparse
import neologdn
import pickle
import numpy as np

from parse import parse
from mkvocab import mkvocab

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("files", help="files that you want to add vocabuary", nargs="*")
    parser.add_argument(
        "-o", "--out_path", default="./", help="output path of precessed file"
    )
    args = parser.parse_args()

    out_dir = args.out_path
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    vocab = {"<PAD>": 0}
    rvocab = {0: "<PAD>"}
    xs = []
    ts = []
    for file_name in args.files:
        normalized = neologdn.normalize(open(file_name).read())
        # parsed_surf = parse(normalized,mode='phr')
        # parsed_base = parse(normalized,mode='phr_base')
        parsed_surf = parse(normalized, mode="morph")

        for i in range(0, len(parsed_surf) - 1):
            # xs.append(parsed_base[i]+" "+parsed_base[i+1]+" "+parsed_base[i+2])
            # # xs.append(parsed_surf[i]+" "+parsed_surf[i+1]+" "+parsed_surf[i+2])
            # ts.append(parsed_surf[i+3]+" "+parsed_surf[i+4]+" "+parsed_surf[i+5]+" <EOS>")
            xs.append(parsed_surf[i])
            ts.append(parsed_surf[i + 1] + " <EOS>")
        l = ts[-1].split()
        l[-1:-1] = ["<EOT>"]
        ts[-1] = " ".join(l)
    xs = "\n".join(xs)
    ts = "\n".join(ts)
    mkvocab(xs, vocab, rvocab)
    mkvocab(ts, vocab, rvocab)

    out_path = os.path.join(out_dir, "vocab.txt")
    with open(out_path, "w") as f:
        print("\n".join(vocab), file=f)
    out_path = os.path.join(out_dir, "vocab.dump")
    with open(out_path, "wb") as f:
        pickle.dump(vocab, f)
    out_path = os.path.join(out_dir, "rvocab.dump")
    with open(out_path, "wb") as f:
        pickle.dump(rvocab, f)

    out_path = os.path.join(out_dir, "x.txt")
    with open(out_path, "w") as f:
        print(xs, file=f)
    out_path = os.path.join(out_dir, "t.txt")
    with open(out_path, "w") as f:
        print(ts, file=f)
