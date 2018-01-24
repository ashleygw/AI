from population import Population
population = Population(100)
for i in range(100000):
    population.run()
    if i % 31 == 0:
        population.evaluate()
        population.selection()
