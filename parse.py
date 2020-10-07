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
# morph_base = use mecab, morphologcal analysis with base form
# phr = use cabocha, phrase analysis
# phr_base = use cabocha, phrase analysis with base form
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
    elif mode in {"phr", "phr_base"}:
        c = CaboCha.Parser("-f1 -d" + dicdir)
        for line in lines.splitlines():
            if not (line):
                continue
            tree = c.parse(line)
            for i in range(0, tree.size()):
                token = tree.token(i)
                if mode == "phr":
                    text = (
                        token.surface if token.chunk else (text + " " + token.surface)
                    )
                elif mode == "phr_base":
                    word = (
                        token.surface
                        if len(token.feature.split(",")) == 7
                        else token.feature.split(",")[6]
                    )
                    text = word if token.chunk else (text + " " + word)
                if i == tree.size() - 1 or tree.token(i + 1).chunk:
                    sq.append(text)
    return sq


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("files", help="files that you want to add vocabuary", nargs="*")
    parser.add_argument(
        "-o", "--out_path", default="./", help="output path of precessed file"
    )
    args = parser.parse_args()

    for file_name in args.files:
        sq = parse(open(file_name).read(), mode="morph")
        with open(os.path.join(args.out_path, os.path.basename(file_name)), "w") as f:
            print("\n".join(sq), file=f)
