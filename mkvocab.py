#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import pickle
import argparse

def mkvocab(text,vocab,rvocab):
    for word in set(text.replace('\n',' ').split()):
        if word not in vocab:
            vocab[word] = len(vocab)
            rvocab[vocab[word]]=word
    return vocab,rvocab


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f','--files',help='files that you want to add vocabuary', nargs='*', required=True)
    args = parser.parse_args() 

    vocab = {}
    rvocab = {}
    for file in args.files:
        mkvocab(open(file).read(),vocab,rvocab)
    with open('vocab.txt','w') as f:
        print('\n'.join(vocab),file=f)
    with open('vocab.dump','wb') as f:
        pickle.dump(vocab,f)
    with open('rvocab.dump','wb') as f:
        pickle.dump(rvocab,f)
