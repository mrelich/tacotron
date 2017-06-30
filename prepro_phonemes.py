#/usr/bin/python2
# -*- coding: utf-8 -*-

'''
By kyubyong park. kbpark.linguist@gmail.com. 
https://www.github.com/kyubyong/tacotron
'''

import codecs
import csv
import os
import re

from hyperparams import Hyperparams as hp
import numpy as np


def load_vocab():

    # Read infile
    # TODO: make this entire thing a class to
    #       handle data prep
    infile = open(hp.ph_file,'r')
    ph_list = []
    for line in infile:
        ph_list.append(line.split('\n')[0])
    infile.close()

    # +1 for masking
    char2idx = {char:idx+1 for idx, char in enumerate(ph_list)}
    idx2char = {idx+1:char for idx, char in enumerate(ph_list)}
    return char2idx, idx2char    

def create_train_data():
    # Load vocabulary
    char2idx, idx2char = load_vocab() 
      
    texts, sound_files = [], []
    reader = csv.reader(codecs.open(hp.text_file, 'rb', 'utf-8'))
    for row in reader:
        sound_fname, text, duration = row
        sound_file = hp.sound_fpath + "/" + sound_fname + ".wav"
         
        if hp.min_len <= len(text) <= hp.max_len:
            # Ignoring whitespace.  I don't know if the white space will matter
            # in the case of phonemes...
            texts.append(np.array([char2idx[char] for char in text.split()], np.int32).tostring())
            sound_files.append(sound_file)
             
    return texts, sound_files
     
def load_train_data():
    """We train on the whole data but the last num_samples."""
    texts, sound_files = create_train_data()
    if hp.sanity_check: # We use a single mini-batch for training to overfit it.
        texts, sound_files = texts[:hp.batch_size]*1000, sound_files[:hp.batch_size]*1000
    else:
        texts, sound_files = texts[:-hp.num_samples], sound_files[:-hp.num_samples]
    return texts, sound_files
 
def load_eval_data():
    """We evaluate on the last num_samples."""
    texts, _ = create_train_data()
    if hp.sanity_check: # We generate samples for the same texts as the ones we've used for training.
        texts = texts[:hp.batch_size]
    else:
        texts = texts[-hp.num_samples:]
    
    X = np.zeros(shape=[len(texts), hp.max_len], dtype=np.int32)
    for i, text in enumerate(texts):
        _text = np.fromstring(text, np.int32) # byte to int 
        X[i, :len(_text)] = _text
    
    return X
 

