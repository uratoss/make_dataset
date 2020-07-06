#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import argparse
import neologdn
import pickle
import numpy as np

from parse import parse
from mkvocab import mkvocab

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    #parser.add_argument('text_path',help ='text path that you want to processing')
    parser.add_argument('files',help='files that you want to add vocabuary', nargs='*')
    parser.add_argument('-o','--out_path',default='./',help='output path of precessed file')
    args = parser.parse_args()

    vocab = {'<PAD>':0}
    rvocab = {0:'<PAD>'}
    xs = []
    ts = []
    for files in args.files:
        normalized = neologdn.normalize(open(files).read())
        parsed = parse(normalized,mode='b')

        head = ['<BOT>']
        half_len = 1
        for sq in parsed:
            for i in range(0,half_len):
                xs.append(' '.join(head[i:]) +' '+ sq)
                ts.append(' '.join(xs[-1].split()[1:]+['<EOS> ']))
            # 半分ぐらいずらす
            sq_split = sq.split()
            half_len = int(len(sq_split)/2)
            head = sq_split[-half_len:]
        ts[-1] = ts[-1].replace('<EOS>','<EOT>')

    xs = '\n'.join(xs)
    ts = '\n'.join(ts)
    mkvocab(xs,vocab,rvocab)
    mkvocab(ts,vocab,rvocab)

    out_path = os.path.join(args.out_path,'vocab.txt')
    with open(out_path,'w') as f:
        print('\n'.join(vocab),file=f)
    out_path = os.path.join(args.out_path,'vocab.dump')
    with open(out_path,'wb') as f:
        pickle.dump(vocab,f)
    out_path = os.path.join(args.out_path,'rvocab.dump')
    with open(out_path,'wb') as f:
        pickle.dump(rvocab,f)

    out_path = os.path.join(args.out_path,'x.txt')
    with open(out_path,'w') as f:
        print(xs,file=f)
    out_path = os.path.join(args.out_path,'t.txt')
    with open(out_path,'w') as f:
        print(ts,file=f)

