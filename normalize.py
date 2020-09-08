#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import argparse
import neologdn

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("text_name", help="text name that you want to processing")
    parser.add_argument(
        "-o", "--out_path", default="./", help="output path of precessed file"
    )
    args = parser.parse_args()

    normalized = neologdn.normalize(open(args.text_name).read())
    out_path = os.path.join(args.out_path, os.path.basename(args.text_name))
    print(normalized)
    with open(out_path, "w") as f:
        print(normalized, file=f)
