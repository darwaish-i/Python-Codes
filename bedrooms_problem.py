bedrooms = ['Lisbon', 'Madrid', 'London', 'Dublin', 'Paris']

preferences = [('Mary', ('Lisbon', 'Paris')),
               ('Peter', ('Lisbon', 'Paris')),
               ('Stuart', ('Madrid', 'Lisbon')),
               ('Jessica', ('Madrid', 'Dublin')),
               ('Fred', ('Paris', 'Madrid')),
               ('John', ('London', 'Madrid')),
               ('Paul', ('London', 'Paris')),
               ('Suzane', ('Dublin', 'London')),
               ('Amanda', ('Dublin', 'London')),
               ('Laura', ('Dublin', 'London'))]

domain = [(0, (len(bedrooms) * 2) - i - 1) for i in range(0, len(bedrooms) * 2)]

def print_function(solution):
  vacancies = []
  for i in range(len(bedrooms)):
    vacancies += [i, i]
  #print(vacancies)

  for i in range(len(solution)):
    current = solution[i]
    bedroom = bedrooms[vacancies[current]]
    print(preferences[i][0], bedroom)
    del vacancies[current]


# [6,1,2,1,2,0,2,2,0,0]
def fitness_function(solution):
    cost = 0
    vacancies = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4]
    for i in range(len(solution)):
        current = solution[i]
        bedroom = bedrooms[vacancies[current]]
        preference = preferences[i][1]
        if preference[0] == bedroom:
            cost += 0
        elif preference[1] == bedroom:
            cost += 1
        else:
            cost += 3

        del vacancies[current]

    return cost

fitness_function([6,1,2,1,2,0,2,2,0,0])