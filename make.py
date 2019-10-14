#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import MeCab
import os
import argparse

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument('text_name',help ='text name that you want to processing')
    parser.add_argument('-o','--out_path',default='./',help='output path of precessed file')
    args = parser.parse_args()

    m = MeCab.Tagger('-Owakati -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')

    ys = [m.parse(ys).replace('\n','').strip() for ys in open(args.text_name).read().replace(' ','').strip().split('\n')]
    out_path = os.path.join(args.out_path,os.path.basename(args.text_name))
    with open(out_path,'w') as f:
        for y in ys:
            print(y,end=' \n',file=f)
            print(y)

if __name__ == '__main__':
    main()
