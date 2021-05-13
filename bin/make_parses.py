

sents = [
'I went to W.L.H. There, I studied for my Spanish class.',
'Every king and peasant, every young couple in love, every mother and father lived there.',
'Shakespare said that nothing is either good or bad, but that thinking makes it so.'
]


print("BENEPAR")

import tqdm

def nop(it, *a, **k):
    return it

tqdm.tqdm = nop

import benepar, spacy
import nltk
import supar
import time
from typing import List

supar_parser = supar.Parser.load('crf-con-en')
benepar_parser = spacy.load('en_core_web_md')

if spacy.__version__.startswith('2'):
    benepar_parser.add_pipe(benepar.BeneparComponent("benepar_en3"))
else:
    benepar_parser.add_pipe("benepar", config={"model": "benepar_en3"})

def parse_benepar(text: str) -> str:
    doc = benepar_parser(text)
    s = " ".join([sent._.parse_string for sent in doc.sents])
    if len(list(doc.sents)) > 1:
        s = "(TOP " + s + ")"
    return s

def parse_benepar_pretokenize(text: str) -> str:
    sents = nltk.sent_tokenize(text)
    out = []
    for sent in sents:
        doc = benepar_parser(sent)
        out += [sent._.parse_string for sent in doc.sents]
    s = " ".join(out)
    if len(out) > 1:
        s = "(TOP " + s + ")"
    return s

def parse_crf(text: str) -> str:
    tokens = [nltk.word_tokenize(text)]
    parses = supar_parser.predict(tokens, lang=None, verbose=False).sentences
    s = " ".join([p.__repr__() for p in parses])
    if len(parses) > 1:
        s = "(TOP " + s + ")"
    return s

def parse_crf_pretokenize(text: str) -> str:
    sents = nltk.sent_tokenize(text)
    tokens = [nltk.word_tokenize(x) for x in sents]
    parses = supar_parser.predict(tokens, lang=None, verbose=False).sentences
    s = " ".join([p.__repr__() for p in parses])
    if len(parses) > 1:
        s = "(TOP " + s + ")"
    return s


import os

directory = r'./parses/'
for entry in os.scandir(directory):
    if entry.path.endswith(".txt") and entry.is_file():
        print(entry.path)
        print(entry.name)
        name = os.path.splitext(entry.name)[0]
        text = ""
        comment = ""
        with open(entry.path) as f:
            for line in f:
                split = line.partition('#')
                text += split[0].rstrip()
                comment += "".join(split[1:])
        benepar_name = "./parses/parsed/" + name + "_benepar.txt"
        benepar_pretokenized_name = "./parses/parsed/" + name + "_benepar_pretokenized.txt"
        crf_name = "./parses/parsed/" + name + "_crf.txt"
        crf_pretokenized_name = "./parses/parsed/" + name + "_crf_pretokenized.txt"

        with open(benepar_name, "w") as f:
            f.write(comment)
            f.write(parse_benepar(text))

        with open(benepar_pretokenized_name, "w") as f:
            f.write(comment)
            f.write(parse_benepar_pretokenize(text))

        with open(crf_name, "w") as f:
            f.write(comment)
            f.write(parse_crf(text))

        with open(crf_pretokenized_name, "w") as f:
            f.write(comment)
            f.write(parse_crf_pretokenize(text))
