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
    chunk = 3
    offset = -3
    for file_paths in args.files:
        files = glob.glob(file_paths)
        for file_name in files:
            parsed = [
                f.strip() for f in open(file_name).read().replace("\n", "").split("<P>")
            ]

            head = "<BOT> "
            for i in range(len(parsed)):
                x = head
                for j in range(chunk):
                    if i + j > len(parsed) - 1:
                        break
                    x = x + parsed[i + j] + " <P> "
                if i + j + 1 > len(parsed) - 1:
                    x = " ".join(x.split()[:-1] + ["<EOT>"])
                    # end_str = "<EOT>"
                    end_str = "<P>"
                else:
                    end_str = parsed[i + j + 1].split()[0].strip()
                xs.append(x.strip())
                ts.append((" ".join(x.split()[1:]) + " " + end_str).strip())
                x_split = parsed[i].split()
                head = ""
                for k in range(max(offset, -len(x_split)), 0, 1):
                    head = head + x_split[k] + " "
                head = head + "<P> "
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
