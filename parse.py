#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import MeCab
import CaboCha
import os
import argparse
import subprocess

# @param mode parse mode
# morph = default, use mecab, morphologcal analysis
# morph_base = default, use mecab, morphologcal analysis with base form
# phr = default, use mecab, phrase
def parse(lines, mode="morph"):
    sq = []
    dicdir = (
        subprocess.run(
            ["mecab-config", "--dicdir"], encoding="utf-8", stdout=subprocess.PIPE
        ).stdout.strip()
        + "/mecab-ipadic-neologd"
    )
    if mode in {"morph", "morph_base"}:
        m = MeCab.Tagger("-d " + dicdir)

        for line in lines.splitlines():
            if not (line):
                continue
            s = []
            for mline in m.parse(line.strip()).splitlines()[:-1]:
                surface = mline.split("\t")[0]
                feature = mline.split("\t")[1].split(",")
                if (feature[0] == "記号") or (mode == "morph"):
                    s.append(surface)
                else:
                    s.append(feature[6])
            sq.append(" ".join(s))
    elif mode in {"phr"}:
        c = CaboCha.Parser("-f1 -d" + dicdir)
        for line in lines.splitlines():
            if not (line):
                continue
            tree = c.parse(line)
            for i in range(0, tree.size()):
                token = tree.token(i)
                text = token.surface if token.chunk else (text + " " + token.surface)
                if i == tree.size() - 1 or tree.token(i + 1).chunk:
                    sq.append(text)
    return sq


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("text_name", help="text name that you want to processing")
    parser.add_argument(
        "-o", "--out_path", default="./", help="output path of precessed file"
    )
    args = parser.parse_args()

    sq = parse(open(args.text_name).read(), mode="morph")
    out_path = os.path.join(args.out_path, os.path.basename(args.text_name))
    with open(out_path, "w") as f:
        print("\n".join(sq), file=f)
