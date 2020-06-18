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

    vocab = {}
    rvocab = {}
    for file in args.files:
        normalized = neologdn.normalize(open(file).read())
        parsed = parse(normalized)
        mkvocab('\n'.join(parsed),vocab,rvocab)

        shifted = []
        head = '<bot>'
        for sq in parsed:
            shifted.append(head +' '+ sq)
            head = ' '.join(sq.split()[-2:])
        print(shifted)
        data = ' <eos> \n'.join(shifted)

        #embeded = []
        #for sq in parsed:
        #    embeded.append([ vocab[word] for word in sq.split()])
        #embeded = np.array(embeded)
        #print(embeded.shape)
    print(data)
    with open('vocab.txt','w') as f:
        print('\n'.join(vocab),file=f)
    with open('vocab.dump','wb') as f:
        pickle.dump(vocab,f)
    with open('rvocab.dump','wb') as f:
        pickle.dump(rvocab,f)

    out_path = os.path.join(args.out_path,'xs.txt')
    with open(out_path,'w') as f:
        print(data,file=f)

