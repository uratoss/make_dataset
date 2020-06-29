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
        parsed = parse(normalized)

        head = '<BOT>'
        for sq in parsed:
            xs.append(head +' '+ sq)
            ts.append(' '.join(xs[-1].split()[1:]+['<EOS> ']))
            head = ' '.join(sq.split()[-3:])
        ts[-1] = ts[-1].replace('<EOS>','<EOT>')

    xs = '\n'.join(xs)
    ts = '\n'.join(ts)
    mkvocab(xs,vocab,rvocab)
    mkvocab(ts,vocab,rvocab)

    with open('vocab.txt','w') as f:
        print('\n'.join(vocab),file=f)
    with open('vocab.dump','wb') as f:
        pickle.dump(vocab,f)
    with open('rvocab.dump','wb') as f:
        pickle.dump(rvocab,f)

    out_path = os.path.join(args.out_path,'x.txt')
    with open(out_path,'w') as f:
        print(xs,file=f)
    out_path = os.path.join(args.out_path,'t.txt')
    with open(out_path,'w') as f:
        print(ts,file=f)

