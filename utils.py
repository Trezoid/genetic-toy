import math, random
import scores
import breeder
from genomes import child
from breeder import breeder, mutator


wordList = set()

class scorer: 
    length_target = 0

    def __init__(self, target=280):
        self.length_target = target
        if not len(wordList):
            f = open('words.txt', 'r')
            for line in f.readline():
                wordList.add(line)

    def score_obj(self, obj):
        words = obj.words()
        score = len(words) * scores.WORD_COUNT + len(obj.chars) * scores.CHAR_COUNT
        for word in words:
            if word in wordList:
                score += scores.REAL_WORD
            else:
                score += scores.NOT_WORD

        if len(obj.string()) < self.length_target:
            score += scores.WITHIN_TARGET
        else:
            score += (self.length_target - len(obj.string())) * (scores.CHAR_COUNT * 50)
        
        
        return score


class generation:
    gen_list = []
    pop_size = 1000
    def __init__(self, generation=None, population=1000):
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
            keep_count = math.floor(len(self.gen_list) / 100) * scores.KEEP_PERCENT
            mute_count = math.floor(len(self.gen_list) / 100) * scores.MUTATE_PERCENT
            generation = self.sort_gen(generation)

            for child_num, child_obj in enumerate(generation.gen_list):
                if child_num < keep_count:
                    new_gen.append(child_obj)
                    top.append(child_obj)
                elif child_num >= len(generation.gen_list) - mute_count:
                    new_child = child_obj
                    self.mute.mutate(new_child)
                    new_gen.append(new_child)
                else:
                    high = random.choices(generation.gen_list, reversed(range(len(generation.gen_list))))[0]
                    new_child = self.breed.breed(high, child_obj)
                    new_gen.append(new_child)

            self.gen_list = new_gen

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

