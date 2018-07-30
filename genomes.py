import re
from numpy import random
import scores

CHAR_LIST = list('abcdefghijklmnopqrstuvwxyz ')
MAX_LENGTH = scores.GENOME_SIZE
WORD_FINDER = re.compile("[\w']+")

class child:
    chars = []
    score = 0
    words = []
 
    def __init__(self, genome=None):
        self.chars = self.setGenome(genome)

    def setGenome(self, genome):
        if genome and len(genome) > 0:
            return genome[:MAX_LENGTH]
        
        lenstr = random.randint(5, MAX_LENGTH)
        new_genome = random.choice(CHAR_LIST, lenstr).tolist()
        return new_genome

    def string(self):
        return ''.join(self.chars)

    def words(self):
        return WORD_FINDER.findall(self.string())

    def gen_len(self, length):
        length = max(0, length)
        outlist = random.choice(CHAR_LIST, length).tolist()
        return outlist

    def set_score(self, score):
        self.score = score

    def set_single(self, genomePoint):
        self.chars[genomePoint] = random.choice(CHAR_LIST)

    def __repr__(self):
        return self.string()
