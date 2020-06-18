#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import MeCab
import os
import argparse
import subprocess

def parse(lines,mode = 'd'):
    dicdir = subprocess.run(['mecab-config', '--dicdir'], encoding='utf-8', stdout=subprocess.PIPE).stdout.strip() + '/mecab-ipadic-neologd'
    m = MeCab.Tagger('--unk-feature <unk> -d '+dicdir)
    sq = []
    for line in lines.splitlines():
        if not(line):
            continue
        s = []
        for mline in m.parse(line.strip()).splitlines()[:-1]:
            surface = mline.split('\t')[0]
            feature = mline.split('\t')[1].split(',')
            if feature[0] == '<unk>' or feature[0] == '記号' or mode == 'd':
                s.append(surface)
            else:
                s.append(feature[6])
        sq.append(' '.join(s))
    return sq
 
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('text_name',help ='text name that you want to processing')
    parser.add_argument('-o','--out_path',default='./',help='output path of precessed file')
    args = parser.parse_args()

    sq = parse(open(args.text_name).read())
    out_path = os.path.join(args.out_path,os.path.basename(args.text_name))
    with open(out_path,'w') as f:
        print('\n'.join(sq),file=f)
