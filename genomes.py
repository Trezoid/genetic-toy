import re, random

CHAR_LIST = list('abcdefghijklmnopqrstuvwxyz?. !')
MAX_LENGTH = 600

class child:
    chars = []
    score = 0
 
    def __init__(self, genome=None):
        self.chars = self.setGenome(genome)

    def setGenome(self, genome):
        if genome and len(genome) > 0:
            return genome[:MAX_LENGTH]
        
        lenstr = random.randint(1, MAX_LENGTH)
        new_genome = []
        for n in range(lenstr):
            new_genome.append(random.choice(CHAR_LIST)) 
        return new_genome

    def string(self):
        return ''.join(self.chars)

    def words(self):
        return re.findall("[\w']+", self.string())

    def set_score(self, score):
        self.score = score

    def set_single(self, genomePoint):
        self.chars[genomePoint] = random.choice(CHAR_LIST)

    def __repr__(self):
        return self.string()
