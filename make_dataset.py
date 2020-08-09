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

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('files',help='files that you want to add vocabuary', nargs='*')
    parser.add_argument('-o','--out_path',default='./',help='output path of precessed file')
    args = parser.parse_args()

    vocab = {'<PAD>':0}
    rvocab = {0:'<PAD>'}
    xs = []
    ts = []
    for file_paths in args.files:
        files = glob.glob(file_paths)
        for file_name in files:
            normalized = neologdn.normalize(open(file_name).read())
            parsed = parse(normalized,mode='phr')

            for i in range(len(parsed)-1):
                xs.append(parsed[i])
                ts.append(parsed[i+1]+" <EOS>")
            l = ts[-1].split()
            l[-1:-1] = ["<EOT>"]
            ts[-1] = ' '.join(l)
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

