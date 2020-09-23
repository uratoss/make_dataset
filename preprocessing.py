#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import argparse


def power_set(elements):
    p_set = [[]]
    for element in elements:
        tmp = []
        for p_element in p_set:
            tmp.append(p_element + [element])
        p_set.extend(tmp)
    return p_set


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("x_name", help="x text name that you want to processing")
    parser.add_argument("y_name", help="y text name that you want to processing")
    parser.add_argument(
        "-o", "--out_path", default="./", help="output path of precessed file"
    )
    args = parser.parse_args()

    xs_list = open(args.x_name).read().replace(" ", "").strip().split("\n")
    ys_list = open(args.y_name).read().replace(" ", "").strip().split("\n")
    rxs_list = []
    rys_list = []
    for xs, ys in zip(xs_list, ys_list):
        x_out_path = os.path.join(args.out_path, "x.txt")
        y_out_path = os.path.join(args.out_path, "t.txt")
        xs = [x for x in xs.split("<nn>") if len(x) > 0]
        ys = [y for y in ys.split("<nn>") if len(y) > 0]
        xs = power_set(xs)[1:]
        ys = power_set(ys)[1:]
        if len(xs) < len(ys):
            tmp = xs
            xs = ys
            ys = tmp
            tmp = x_out_path
            x_out_path = y_out_path
            y_out_path = tmp
        for x in xs:
            for y in ys:
                with open(x_out_path, "a") as f:
                    print("".join(x), end=" \n", file=f)
                with open(y_out_path, "a") as f:
                    print("".join(y), end=" \n", file=f)


if __name__ == "__main__":
    main()
