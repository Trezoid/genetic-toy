from utils import generation

gen = generation(population=1000)
for i in range(5000000):         
    gen = generation(gen, population=1000)
    if i % 1000 == 0:
        print(gen.gen_list[0].string())
    print(f'generation {i}: {[i.score for i in gen.gen_list[0:20]]}')

