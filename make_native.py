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

    m = MeCab.Tagger('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')

    ys = []
    for yl in open(args.text_name).read().replace(' ','').strip().split('\n'):
      y = []
      for ml in m.parse(yl).split('\n'):
        if ml == '' or ml =='EOS':
            continue
        ms = ml.split(',')
        if ms[6] == '*':
            y.append(ms[0].split('\t')[0])
        elif ms[0].split('\t')[1] == '記号' :
            y.append(ms[0].split('\t')[0])
        else:
            y.append(ms[6])
      ys.append(' '.join(y))
    out_path = os.path.join(args.out_path,os.path.basename(args.text_name))
    with open(out_path,'w') as f:
        for y in ys:
            print(y,end=' \n',file=f)
            print(y)

if __name__ == '__main__':
    main()
