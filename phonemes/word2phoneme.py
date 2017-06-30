
import tensorflow as tf
from g2p_seq2seq.g2p import G2PModel
from six import text_type
import os

class Word2Phoneme:

    # Constructor
    def __init__(self, path_to_model):
        assert( os.path.isdir(path_to_model) )

        self.model = G2PModel(path_to_model)
        self.model.load_decode_model()
        
    # Method to convert words to phoneme representation
    def convert(self, word):
        return self.model.decode_word( text_type(word, encoding='utf-8', errors='replace') )

    # Method to convert sentence
    def convert_sentence(self, sentence):
        words = []
        for word in sentence.split():
            words.append( self.convert(word) )
        return ' '.join(words)
    
