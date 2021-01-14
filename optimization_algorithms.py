import time
import random
import math
import sys

people = [('Lisbon', 'LIS'),
          ('Madrid', 'MAD'),
          ('Paris', 'CDG'),
          ('Dublin', 'DUB'),
          ('Brussels', 'BRU'),
          ('London', 'LHR')]

flights = {}
for line in open('flights.txt'):
  #print(line)
  #print(line.split(','))
  origin, destiny, departure, arrival, price = line.split(',')
  flights.setdefault((origin, destiny), [])
  flights[(origin, destiny)].append((departure, arrival, int(price)))

def print_schedule(schedule):
  flight_id = -1
  for i in range(len(schedule) // 2):
    name = people[i][0]
    origin = people[i][1]
    flight_id += 1
    going = flights[(origin, destiny)][schedule[flight_id]]
    flight_id += 1
    returning = flights[(destiny, origin)][schedule[flight_id]]
    print(name, origin, destiny, going[0], going[1], going[2], returning[0], returning[1], returning[2])

def get_minutes(hour):
  t = time.strptime(hour, '%H:%M')
  minutes = t[3] * 60 + t[4]
  return minutes


def fitness_function(solution):
    total_price = 0
    last_arrival = 0
    first_departure = 1439

    flight_id = -1
    for i in range(len(solution) // 2):
        origin = people[i][1]
        flight_id += 1
        going = flights[(origin, destiny)][solution[flight_id]]
        flight_id += 1
        returning = flights[(destiny, origin)][solution[flight_id]]

        total_price += going[2]
        total_price += returning[2]

        if last_arrival < get_minutes(going[1]):
            last_arrival = get_minutes(going[1])
        if first_departure > get_minutes(returning[0]):
            first_departure = get_minutes(returning[0])

    total_wait = 0
    flight_id = -1
    for i in range(len(solution) // 2):
        origin = people[i][1]
        flight_id += 1
        going = flights[(origin, destiny)][solution[flight_id]]
        flight_id += 1
        returning = flights[(destiny, origin)][solution[flight_id]]

        total_wait += last_arrival - get_minutes(going[1])
        total_wait += get_minutes(returning[0]) - first_departure

    # 3PM - 10AM
    # 11AM - 3PM
    if last_arrival > first_departure:
        total_price += 50

    return total_price + total_wait

domain = [(0,9)] * (len(people) * 2)


def random_search(domain, fitness_function):
  best_cost = sys.maxsize
  for i in range(10000):
    solution = [random.randint(domain[i][0],domain[i][1]) for i in range(len(domain))]
    cost = fitness_function(solution)
    if cost < best_cost:
      best_cost = cost
      best_solution = solution
  return best_solution

# [6, 9, 5, 3, 3, 4, 5, 4, 3, 2, 5, 5]
def hill_climb(domain, fitness_function):
  solution = [random.randint(domain[i][0],domain[i][1]) for i in range(len(domain))]
  while True:
    neighbors = []
    for i in range(len(domain)):
      if solution[i] > domain[i][0]:
        if solution[i] != domain[i][1]:
          neighbors.append(solution[0:i] + [solution[i] + 1] + solution[i + 1:])
      if solution[i] < domain[i][1]:
        if solution[i] != domain[i][0]:
          neighbors.append(solution[0:i] + [solution[i] - 1] + solution[i + 1:])

    actual = fitness_function(solution)
    best = actual
    for i in range(len(neighbors)):
      cost = fitness_function(neighbors[i])
      if cost < best:
        best = cost
        solution = neighbors[i]

    if best == actual:
      break

  return solution

# [6, 9, 5, 3, 3, 4, 5, 4, 3, 2, 5, 5]
def simulated_anneling(domain, fitness_function, temperature = 10000.0,
                       cooling = 0.95, step = 1):
  solution = [random.randint(domain[i][0],domain[i][1]) for i in range(len(domain))]
  while temperature > 0.1:
    i = random.randint(0, len(domain) - 1)
    direction = random.randint(-step, step)
    temp_solution = solution[:]
    temp_solution[i] += direction
    if temp_solution[i] < domain[i][0]:
      temp_solution[i] = domain[i][0]
    elif temp_solution[i] > domain[i][1]:
      temp_solution[i] = domain[i][1]

    cost_solution = fitness_function(solution)
    cost_solution_temp = fitness_function(temp_solution)
    probability = pow(math.e, (-cost_solution_temp - cost_solution) / temperature)

    if (cost_solution_temp < cost_solution or random.random() < probability):
      solution = temp_solution

    temperature = temperature * cooling

  return solution

def mutation(domain, step, solution):
  gene = random.randint(0, len(domain) - 1)
  mutant = solution
  if random.random() < 0.5:
    if solution[gene] != domain[gene][0]:
      mutant = solution[0:gene] + [solution[gene] - step] + solution[gene + 1:]
  else:
    if solution[gene] != domain[gene][1]:
      mutant = solution[0:gene] + [solution[gene] + step] + solution[gene + 1:]
  return mutant

# [6, 7, 6, 7, 3, 9, 7, 7, 0, 9, 6, 7]
def crossover(domain, solution1, solution2):
  gene = random.randint(1, len(domain) - 2)
  return solution1[0:gene] + solution2[gene:]

def genetic(domain, fitness_function, population_size = 15, step = 1,
            probability_mutation = 0.2, elitism = 0.2,
            number_generations = 500):
  population = []
  for i in range(population_size):
    solution = [random.randint(domain[i][0], domain[i][1]) for i in range(len(domain))]
    population.append(solution)

  number_elitism = int(elitism * population_size)

  for i in range(number_generations):
    costs = [(fitness_function(individual), individual) for individual in population]
    costs.sort()
    ordered_individuals = [individual for (cost, individual) in costs]
    population = ordered_individuals[0:number_elitism]
    while len(population) < population_size:
      if random.random() < probability_mutation:
        m = random.randint(0, number_elitism)
        population.append(mutation(domain, step, ordered_individuals[m]))
      else:
        i1 = random.randint(0, number_elitism)
        i2 = random.randint(0, number_elitism)
        population.append(crossover(domain, ordered_individuals[i1], ordered_individuals[i2]))
  return costs[0][1]

genetic_solution = genetic(domain, fitness_function)
genetic_solution