import math, re
import random
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
                'alt_char': (1, self.altChar,),
                'high_half': (5, self.highHalf,),
                'low_half': (2, self.lowHalf,),
                'low_end': (5, self.lowEnd,),
                'word_walk': (10, self.wordWalk),
                }
        total = sum([r[0] for r in rates.values()])

        for rate in rates.values():
            portion = math.ceil(rate[0])
            for c in range(portion):
                self.ranges.append(rate[1])
        random.shuffle(self.ranges)

        breed = self

    def breed(self, high, low):
        strat = self.ranges[random.randint(0, len(self.ranges) - 1)]
        return strat(high, low)

    def altChar(self, high, low):
        new_genome = []
        high_len = len(high.chars)
        low_len = len(low.chars)
        count = 0
        for n in range(0, min(high_len, low_len) - 1):
            if n % 2 == 0:
                new_genome.append(high.chars[n])
            else:
                new_genome.append(low.chars[n])
            count = 0
        
        if count < high_len:
            for y in range(count, high_len - 1):
                new_genome.append(high.chars[y])
        if count < low_len:
            for x in range(count, low_len - 1):
                new_genome.append(low.chars[x])

        return genome(new_genome)

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
        new_genome = []
        highlen = math.ceil(len(high.chars) / 2)
        lowlen = math.ceil(len(low.chars) / 2)
        for i in range(highlen):
            new_genome.append(high.chars[i])
        for i in range(lowlen, len(low.chars) - 1):
            new_genome.append(low.chars[i])
        return genome(new_genome)

    def lowHalf(self, high, low):
        new_genome = []
        lowlen = math.ceil(len(low.chars) / 2)
        highlen = math.ceil(len(high.chars) / 2)
        for i in range(lowlen):
            new_genome.append(low.chars[i])
        for i in range(highlen, len(high.chars) - 1):
            new_genome.append(high.chars[i])
        return genome(new_genome)

    def lowEnd(self, high, low):
        end_perc = (len(low.chars) / 100) * 10
        new_genome = []
        for i in range(len(low.chars)):
            if i < end_perc and i < len(high.chars):
                new_genome.append(high.chars[i])
            else:
                new_genome.append(low.chars[i])
        return genome(new_genome)


class mutator:
    ranges = []
    def __init__(self):
        global mutate
        if mutate:
            return
        rates = {
                'last_half': (2, self.rep_last_half),
                'first_half': (3, self.rep_last_half),
                'every_n': (5, self.rep_every_n),
                'rep_all': (3, self.rep_all),
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

        for n in range(start, len(child.chars) - 1):
            child.set_single(n)
        return child

    def rep_first_half(self, child):
        end = math.ceil(len(child.chars) / 2)

        for n in range(0, end):
            child.set_single(n)

        return child

    def rep_every_n(self, child, gap=2):
        for n in range(0, len(child.chars) - 1, gap):
            child.set_single(n)

        return child

    def rep_all(self, child):
        for n in range(len(child.chars) - 1):
            child.set_single(n)
        return child

    def full_replace(self, child):
        new_child = genome
        child.setGenome(new_child.chars)
        return child
