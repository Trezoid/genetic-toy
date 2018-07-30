from utils import generation
from scores import GEN_SIZE

gen = generation(population=GEN_SIZE)
for i in range(5000000):         
    gen = generation(gen, population=GEN_SIZE)
    if i % 200 == 0:
        print(gen.gen_list[0].string())
    print(f'generation {i}: {[i.score for i in gen.gen_list[0:20]]}')

