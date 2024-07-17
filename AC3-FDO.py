domains = {
    'A': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
    'B': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    'C': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25],
    'D': [0, 1, 2, 3, 4],
    'E': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30],
}

constraints = {
    ('A', 'B'): lambda a, b: 18*a <= 380 - 34*b,
    ('B', 'A'): lambda b, a: 380 - 34*b >= 18*a,
    ('C', 'D'): lambda c, d: 7*c <= 280 - 10*d,
    ('D', 'C'): lambda d, c: 280 - 10*d >= 7*c,
    ('C', 'E'): lambda c, e: 7*c <= 350 - 2*e,
    ('E', 'C'): lambda e, c: 350 - 2*e >= 7*c,
}

def revise(x, y):
    revised = False
    x_domain = domains[x]
    y_domain = domains[y]
    all_constraints = [
        constraint for constraint in constraints if constraint[0] == x and constraint[1] == y]
    for x_value in x_domain:
        satisfies = False
        for y_value in y_domain:
            for constraint in all_constraints:
                constraint_func = constraints[constraint]
                if constraint_func(x_value, y_value):
                    satisfies = True
        if not satisfies:
            x_domain.remove(x_value)
            revised = True
    return revised

def ac3(arcs):
    queue = arcs[:]
    while queue:
        (x, y) = queue.pop(0)
        revised = revise(x, y)
        if revised:
            neighbors = [neighbor for neighbor in arcs if neighbor[1] == x]
            queue = queue + neighbors

arcs = [
    ('A', 'B'), ('B', 'A'), 
    ('C', 'D'), ('D', 'C'), 
    ('C', 'E'), ('E', 'C'), 
]

ac3(arcs)

print(domains)