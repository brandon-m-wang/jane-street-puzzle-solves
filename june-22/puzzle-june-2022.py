import collections
from functools import lru_cache

def print_solved_grid():
    print("\n")
    for i in range(9, -1, -1):
        print()
        for j in range(10):
            if len(coord_to_eligible[(j, i)]) == 1:
                if list(coord_to_eligible[(j ,i)])[0] == 10:
                    print(list(coord_to_eligible[(j ,i)])[0], end=" | ")
                else:
                    print(list(coord_to_eligible[(j, i)])[0], end="  | ")
            else:
                print(" ", end=" | ")


region_to_size = {
    0: 10, 
    1: 2, 
    2: 5, 
    3: 1, 
    4: 9, 
    5: 4, 
    6: 3, 
    7: 3, 
    8: 5, 
    9: 4, 
    10: 1, 
    11: 10, 
    12: 3, 
    13: 3, 
    14: 1, 
    15: 2, 
    16: 1, 
    17: 6, 
    18: 7, 
    19: 3, 
    20: 2, 
    21: 9, 
    22: 6,
}
coord_to_region = {
    (0, 0): 0,
    (1, 0): 0,
    (2, 0): 0,
    (3, 0): 0,
    (4, 0): 2,
    (5, 0): 2,
    (6, 0): 4,
    (7, 0): 4,
    (8, 0): 4,
    (9, 0): 4,
    (0, 1): 0,
    (1, 1): 0,
    (2, 1): 0,
    (3, 1): 2,
    (4, 1): 2,
    (5, 1): 4,
    (6, 1): 4,
    (7, 1): 5,
    (8, 1): 5,
    (9, 1): 4,
    (0, 2): 0,
    (1, 2): 0,
    (2, 2): 1,
    (3, 2): 2,
    (4, 2): 8,
    (5, 2): 3,
    (6, 2): 4,
    (7, 2): 5,
    (8, 2): 5,
    (9, 2): 4,
    (0, 3): 11,
    (1, 3): 0,
    (2, 3): 1,
    (3, 3): 8,
    (4, 3): 8,
    (5, 3): 8,
    (6, 3): 7,
    (7, 3): 6,
    (8, 3): 6,
    (9, 3): 6,
    (0, 4): 11,
    (1, 4): 10,
    (2, 4): 9,
    (3, 4): 8,
    (4, 4): 14,
    (5, 4): 15,
    (6, 4): 7,
    (7, 4): 7,
    (8, 4): 18,
    (9, 4): 18,
    (0, 5): 11,
    (1, 5): 9,
    (2, 5): 9,
    (3, 5): 13,
    (4, 5): 13,
    (5, 5): 15,
    (6, 5): 16,
    (7, 5): 17,
    (8, 5): 17,
    (9, 5): 18,
    (0, 6): 11,
    (1, 6): 11,
    (2, 6): 9,
    (3, 6): 12,
    (4, 6): 13,
    (5, 6): 17,
    (6, 6): 17,
    (7, 6): 17,
    (8, 6): 18,
    (9, 6): 18,
    (0, 7): 11,
    (1, 7): 11,
    (2, 7): 12,
    (3, 7): 12,
    (4, 7): 20,
    (5, 7): 20,
    (6, 7): 17,
    (7, 7): 19,
    (8, 7): 18,
    (9, 7): 18,
    (0, 8): 11,
    (1, 8): 11,
    (2, 8): 22,
    (3, 8): 22,
    (4, 8): 22,
    (5, 8): 21,
    (6, 8): 19,
    (7, 8): 19,
    (8, 8): 21,
    (9, 8): 21,
    (0, 9): 11,
    (1, 9): 22,
    (2, 9): 22,
    (3, 9): 22,
    (4, 9): 21,
    (5, 9): 21,
    (6, 9): 21,
    (7, 9): 21,
    (8, 9): 21,
    (9, 9): 21
}

region_to_coords = collections.defaultdict(list)
coord_to_eligible = {}

for coord, region in coord_to_region.items():
    region_to_coords[region].append(coord)

board_file = open("board.txt", "r")
rows = []
for line in board_file.readlines():
    rows.append(list(map(int, line.split())))
for y, row in enumerate(rows[::-1]):
    for x in range(len(row)):
        coord_to_eligible[(x, y)] = {row[x]}

print_solved_grid()

def is_in_bounds(x, y):
    N = 10
    return x >= 0 and x < N and y >= 0 and y < N

@lru_cache(maxsize=None)
def find_tiles_within_range(x, y, n):
    tiles = set()
    for d_x in range(n):
        for d_y in range(n - d_x):
            possible_tiles = [(x + d_x, y + d_y), (x + d_x, y - d_y), (x - d_x, y + d_y), (x - d_x, y - d_y)]
            for tile in possible_tiles:
                if is_in_bounds(tile[0], tile[1]):
                    tiles.add(tile)
    tiles.remove((x, y))
    return tiles

@lru_cache(maxsize=None)
def find_tiles_with_distance(x, y, n):
    tiles = set()
    for d_x in range(n):
        d_y = n - d_x
        possible_tiles = [(x + d_x, y + d_y), (x + d_x, y - d_y), (x - d_x, y + d_y), (x - d_x, y - d_y)]
        for tile in possible_tiles:
            if is_in_bounds(tile[0], tile[1]):
                tiles.add(tile)
    return tiles

def find_tiles_within_region(x, y):
    tiles = set()
    region = coord_to_region[(x, y)]
    for tile in region_to_coords[region]:
        tiles.add(tile)
    tiles.remove((x, y))
    return tiles


queue = []
completed = set()
for x in range(10):
    for y in range(10):
            if len(coord_to_eligible[(x, y)]) == 1:
                queue.append((x, y))
while queue:
    x, y = queue.pop()
    completed.add((x, y))
    k = list(coord_to_eligible[(x, y)])[0]
    for x2, y2 in find_tiles_within_range(x, y, k):
        coord_to_eligible[(x2, y2)].discard(k)
        if len(coord_to_eligible[(x2, y2)]) == 1 and (x2, y2) not in completed:
            queue.append((x2, y2))

    for x2, y2 in find_tiles_within_region(x, y):
        coord_to_eligible[(x2, y2)].discard(k)
        if len(coord_to_eligible[(x2, y2)]) == 1 and (x2, y2) not in completed:
            queue.append((x2, y2))

    potential = []
    for x2, y2 in find_tiles_with_distance(x, y, k):
        if k in coord_to_eligible[(x2, y2)]:
            potential.append((x2, y2))
    if len(potential) == 1 and potential[0] not in completed:
        coord_to_eligible[potential[0]] = {k}
        queue.append(potential[0])

board_file = open("board.txt", "r")
rows = []
for line in board_file.readlines():
    rows.append(list(map(int, line.split())))

ans = 0
for y, row in enumerate(rows[::-1]):
    row_mul = 1
    for x in range(len(row)):
        row_mul *= row[x]
    ans += row_mul

print(f"\n\nAnswer: {ans}")
