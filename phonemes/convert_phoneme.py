
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-#
# Basic script to convert the text file to a phoneme representation.  #
# Also, output a list of unique phonemes so we can read them back in  #
# to generate a dictionary.                                           #
#                                                                     #
# Depends on: g2p-seq2seq-cmudict                                     #
#   https://github.com/cmusphinx/g2p-seq2seq                          #
# Unfortunately this requires tensorflow 1.0.0, so best to setup a    #
# virtual environment to do this processing.                          #
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-#


from word2phoneme import Word2Phoneme as W2P
import csv
import codecs
import re

# For purpose of training, just take small
# subset of total results, say 1k
n_to_keep = 1000

# Specify the input and output file
# TODO: Make this configurable
inname  = '../WEB/text.csv'
outname = '../WEB/text_ph2.csv'
outph   = '../WEB/phonemes2.txt'

# Setup the W2P model
# path is unpacked model directory
conv = W2P('g2p-seq2seq-cmudict') 

# Now loop over every line in the input file
# convert to phonemes, and write to output
# This output will be already formatted 
ph_list = []
reader  = csv.reader(codecs.open(inname, 'rb', 'utf-8'))
outfile = open(outname,'w')
c = 0
for row in reader:
    sound_fname, text, duration = row
    text = re.sub(r"[^ a-z]", "", text.strip().lower())

    # Loop over words and insert some token to identify
    # spaces in words
    text_ph = "" 
    for word in text.split():
        text_ph += conv.convert(word) + " _ "

    #text_ph = conv.convert_sentence(text)

    # write ouput
    outfile.write(','.join([sound_fname, text_ph, duration]))
    outfile.write('\n')
    
    # Get unique phonemes    
    for ph in text_ph.split():
        if ph not in ph_list:
            ph_list.append(ph)

    # Decide if we should break or not
    if c >= n_to_keep:
        break
    c += 1
            
outfile.close()

# Save the dictionary
phout = open(outph,'w')
for ph in ph_list:
    phout.write(ph + '\n')
phout.close()

