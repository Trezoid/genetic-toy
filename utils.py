import math, random
import numpy as np
import scores
import breeder
from genomes import child
from breeder import breeder, mutator


wordList = set()



class scorer: 
    length_target = 0

    def __init__(self, target=280):
        global wordList
        self.length_target = target
        if not len(wordList):
            with open('/usr/share/dict/words', 'r') as f:
                for line in f:
                    wordList.add(line.strip())

    def score_obj(self, obj):
        global wordList
        unique = set()
        words = obj.words()
        score = len(words) * scores.WORD_COUNT + len(obj.chars) * scores.CHAR_COUNT
        for word in words:
            if word in wordList and len(word) > 1:
                score += scores.REAL_WORD
            else:
                score -= scores.NOT_WORD
            if len(word) < scores.SHORT_WORD:
                score -= scores.VERY_SHORT
            if word in unique:
                score -= scores.DUPLICATE_WORD
            else:
                unique.add(word)


        if len(obj.string()) < self.length_target:
            score += scores.WITHIN_TARGET
        else:
            score += (scores.TARGET_SIZE - len(obj.string())) * 10 
        
        
        return score

class generation:
    gen_list = []
    pop_size = 1000
    def __init__(self, generation=None, population=1000):
        global breed
        global mute
        global score

        self.breed = breeder()
        self.mute = mutator()
        self.scorer = scorer()

        self.pop_size = population
        self.gen_pop(generation)


    def gen_pop(self, generation):
        if not generation:
            for i in range(0, self.pop_size):
                c = child()
                self.gen_list.append(c)
        else:
            new_gen = []
            top = []
            keep_count = scores.KEEP_PERCENT
            #keep_count = math.ceil(len(self.gen_list) / 100) * scores.KEEP_PERCENT
            mute_count = math.ceil(len(self.gen_list) / 100) * scores.MUTATE_PERCENT
            generation = self.sort_gen(generation)

            for child_num, child_obj in enumerate(generation.gen_list):
                if child_num < keep_count:
                    new_gen.append(child_obj)
                    top.append(child_obj)
                elif child_num >=  (len(self.gen_list) - mute_count):
                    new_child = child_obj
                    new_child = self.mute.mutate(new_child)
                    new_gen.append(new_child)
                else:
                    high = random.choice(generation.gen_list[:child_num])
                    new_child = self.breed.breed(high, child_obj)
                    if random.randint(1,100) <= scores.MUTANT_CHILD:
                        new_child = self.mute.mutate(new_child)
                    new_gen.append(new_child)

            self.gen_list = new_gen
            self = self.sort_gen()

    def sort_gen(self, gen=None):
        set_sort = False
        if not gen:
            gen = self
            set_sort = True
        
        for child_obj in gen.gen_list:
            if not child_obj.score:
                child_obj.set_score(self.scorer.score_obj(child_obj))

        gen.gen_list.sort(key=lambda c: c.score, reverse=True)
        if set_sort:
            self.gen_list = gen.gen_list

        return gen

