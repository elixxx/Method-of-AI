import matplotlib.pyplot as plt
from GA import GA
from CandidateAI import create_random_CandidateAI
from copy import deepcopy


_population_cnt = 200
_rate_crossover = 0.6
_rate_mutation = 0.05
_sample_candidate = create_random_CandidateAI
_strategy = "onePointSwap"
_tournament_win_rate = 0.8
_tournament_size = 40
_calc_diversity = True
_cnt_generations = 100

fitness_avg = list()
fitness_max = list()
diversity = list()
valid_candidate = list()
gen = GA(population_cnt=_population_cnt, rate_crossover=_rate_crossover, rate_mutation=_rate_mutation, sample_candidate=_sample_candidate)
print("Cross: " + str(_rate_crossover) + "- Mutation: " + str(_rate_mutation) + "- tourSize: " + str(
    _tournament_size) + "- tourRate: " + str(_tournament_win_rate))
for generation in range(_cnt_generations):
    gen.mutate()
    gen.crossover(strategy=_strategy)
    gen.evaluate(calc_diversity=_calc_diversity)
    gen.selection(tournament_win_rate=_tournament_win_rate, tournament_size=_tournament_size)
    if gen.generation%10 == 0:
        print("Gen: " + str(gen.generation) + "- Fitness_avg: " + str(gen.fitness_avg) + "- Fitness_best: "
            + str(gen.best_candidate.get_fitness()) + "- Diversity: " + str(gen.diversity))
    fitness_avg.append(gen.fitness_avg)
    fitness_max.append(gen.best_candidate.get_fitness())
    diversity.append(gen.diversity)
    if (gen.best_candidate.get_fitness() > 1.0):
        valid_candidate.append(deepcopy(gen.best_candidate))
for best in valid_candidate:
    print("Candidate Fitness "+str(best.get_fitness()))
    best.print()

plt.plot(fitness_avg)
plt.plot(fitness_max)
plt.plot(diversity)
plt.show()