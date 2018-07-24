import math, re
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
                'alt_char': (3, self.altChar,),
                'high_half': (10, self.highHalf,),
                'low_half': (2, self.lowHalf,),
                'low_end': (5, self.lowEnd,),
                'word_walk': (8, self.wordWalk),
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
        new_genome = []
        read_from = high
        next_read = low
        for i in range(min(len(high.chars), len(low.chars))):
            new_genome.append(read_from.chars[i])
            if re.match('\w', read_from.chars[i]):
                tmp = read_from
                read_from = next_read
                next_read = tmp
        return genome(new_genome)

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
        end_perc = (len(low.chars) / 100) * 10
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
                'first_half': (3, self.rep_last_half),
                'every_n': (1, self.rep_every_n),
                'rep_all': (5, self.rep_all),
                'full': (5, self.full_replace),
                'shuffle': (10, self.shuffle_all)
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
