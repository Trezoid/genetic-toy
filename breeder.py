import math, re
import numpy as np
import random
from itertools import chain, zip_longest
from genomes import child as genome

breed = None
mutate = None

class breeder:
    ranges = []
    def __init__(self): 
        global breed
        if breed:
            return

        rates = {
                'alt_char': (2, self.altChar,),
                'high_half': (5, self.highHalf,),
                'low_half': (2, self.lowHalf,),
                'low_end': (5, self.lowEnd,),
                 'word_walk': (1, self.wordWalk),
                'merge_blocks': (8, self.merge_blocks),
                }
        total = sum([r[0] for r in rates.values()])

        for rate in rates.values():
            portion = math.ceil(rate[0])
            for c in range(portion):
                self.ranges.append(rate[1])
        random.shuffle(self.ranges)

        breed = self

    def breed(self, high, low):
        strat = random.choice(self.ranges) 
        return strat(high, low)

    def altChar(self, high, low):
        new_genome = []
        high_len = len(high.chars)
        low_len = len(low.chars)

        high_chars = high.chars[::2]
        low_chars = low.chars[1::2]
        out_arr = [x for x in list(chain.from_iterable(
            zip_longest(high_chars, low_chars))) 
            if x is not None]

        return genome(out_arr)

    def wordWalk(self, high, low):
        high_chars = high.words()[::2]
        low_chars = low.words()[1::2]
        out_arr = [x for x in list(chain.from_iterable(
            zip_longest(high_chars, low_chars))) 
            if x is not None]

        return genome(list(' '.join(out_arr)))

    def merge_blocks(self, high, low):
        block_len = random.randint(2,10)
        high_list = [i.tolist() for i in np.array_split(np.asarray(high.chars), block_len)]
        low_list = [i.tolist() for i in np.array_split(np.asarray(low.chars), block_len)]
        high_blocks = high_list[::2]
        low_blocks = low_list[1::2]

        out_arr = [x for x in list(chain.from_iterable(
            zip_longest(high_blocks, low_blocks))) 
            if x is not None]

        genome_list = []
        for arr in out_arr:
            genome_list = genome_list + arr
        
        return genome(genome_list)

    def highHalf(self, high, low):
        highlen = math.ceil(len(high.chars) / 2)
        lowlen = math.ceil(len(low.chars) / 2)
        new_genome = high.chars[0:highlen]
        new_genome.extend(low.chars[lowlen:len(low.chars) -1])

        return genome(new_genome)

    def lowHalf(self, high, low):
        new_genome = []
        lowlen = math.ceil(len(low.chars) / 2)
        highlen = math.ceil(len(high.chars) / 2)

        new_genome = low.chars[0:lowlen]
        new_genome.extend(high.chars[highlen:len(high.chars) -1])
        return genome(new_genome)

    def lowEnd(self, high, low):
        end_perc = (len(low.chars) / 100) * 30
        new_genome = high.chars[:math.ceil(len(high.chars) - end_perc)]
        new_genome.extend(low.chars[math.ceil(len(low.chars) - end_perc):len(low.chars) -1])

        return genome(new_genome)


class mutator:
    ranges = []
    def __init__(self):
        global mutate
        if mutate:
            return
        rates = {
                'last_half': (5, self.rep_last_half),
                'first_half': (4, self.rep_last_half),
                'every_n': (4, self.rep_every_n),
                'rep_all': (5, self.rep_all),
                'full': (4, self.full_replace),
                'shuffle': (1, self.shuffle_all),
                'shuffle_blocks': (3, self.shuffle_blocks),
                'segment_shuffle': (5, self.segment_shuffle),
                'word_shuffle': (1, self.word_shuffle),
                'rep_block': (8, self.rep_block),
        }

        total = sum([r[0] for r in rates.values()])
        for rate in rates.values():
            portion = math.ceil(rate[0])
            for c in range(portion):
                self.ranges.append(rate[1])
        random.shuffle(self.ranges)
        mutate = self
                
    def mutate(self, child):
        strat = self.ranges[random.randint(0, len(self.ranges) - 1)]
        return strat(child)
    
    def shuffle_blocks(self, child):
        num_blocks = random.randint(2, 10)
        genome_list = [i.tolist() for i in np.array_split(np.asarray(child.chars), num_blocks)]
        out_genome = []
        np.random.shuffle(genome_list)
        for arr in genome_list:
            out_genome = out_genome + arr
        
        child.chars = out_genome
        return child

    def segment_shuffle(self, child):
        num_blocks = random.randint(2, 10)
        genome_list = [i.tolist() for i in np.array_split(np.asarray(child.chars), num_blocks)]
        out_genome = []
        for arr in genome_list:
            np.random.shuffle(arr)
            out_genome = out_genome + arr

        child.chars = out_genome
        return child

    def rep_block(self, child):
        num_blocks = random.randint(2, 10)
        genome_list = [i.tolist() for i in np.array_split(np.asarray(child.chars), num_blocks)]
        block_counts = random.randint(0,math.ceil(num_blocks/4))
        block_list = list(range(num_blocks))
        random.shuffle(block_list)

        for block_id in block_list[:block_counts]:
            block_len = len(genome_list[block_id])
            genome_list[block_id] = child.gen_len(block_len)
        chars = []
        for block in genome_list:
            chars = chars + block
        child.chars = chars
        return child
        
    def word_shuffle(self, child):
        words = child.words()
        np.random.shuffle(words)
        chars = ' '.join(words)
        child.chars = list(chars)
        return child

    def shuffle_all(self, child):
        random.shuffle(child.chars)
        return child

    def rep_last_half(self, child):
        start = math.floor(len(child.chars) / 2)

        half = child.chars[0:start]
        half.extend(child.gen_len(len(child.chars) - start))
        child.chars = half
        return child

    def rep_first_half(self, child):
        end = math.ceil(len(child.chars) / 2)
        start = child.gen_len(end)
        start.extend(child.chars[end, len(child.chars) -1])
        child.chars = start
        return child

    def rep_every_n(self, child, gap=2):
        for n in range(0, len(child.chars) - 1, gap):
            child.set_single(n)

        return child

    def rep_all(self, child):
        new = child.gen_len(len(child.chars) - 1)
        child.chars = new
        return child

    def full_replace(self, child):
        new_child = genome
        child.chars = new_child.chars
        return child
