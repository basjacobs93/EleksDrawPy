from .hashindex import Index
import math
import random


def anneal(state, max_temp, min_temp, steps):
    factor = -math.log(float(max_temp) / min_temp)
    state = state.copy()
    best_state = state.copy()
    best_energy = state.energy()
    previous_energy = best_energy
    for step in xrange(steps):
        temp = max_temp * math.exp(factor * step / steps)
        undo = state.do_move()
        energy = state.energy()
        change = energy - previous_energy
        if change > 0 and math.exp(-change / temp) < random.random():
            state.undo_move(undo)
        else:
            previous_energy = energy
            if energy < best_energy:
                # print step, temp, energy
                best_energy = energy
                best_state = state.copy()
    return best_state

def get_max_temp(state, iterations):
    state = state.copy()
    previous = state.energy()
    total = 0
    for _ in xrange(iterations):
        state.do_move()
        energy = state.energy()
        total += abs(energy - previous)
        previous = energy
    average = total / iterations
    return average * 2

def sort_paths_greedy(paths, reversable=True):
    first = max(paths, key=lambda x: x[0][1])
    paths.remove(first)
    result = [first]
    points = []
    for path in paths:
        x1, y1 = path[0]
        x2, y2 = path[-1]
        points.append((x1, y1, path, False))
        if reversable:
            points.append((x2, y2, path, True))
    index = Index(points)
    while index.size:
        x, y, path, reverse = index.search(result[-1][-1])
        x1, y1 = path[0]
        x2, y2 = path[-1]
        index.remove((x1, y1, path, False))
        if reversable:
            index.remove((x2, y2, path, True))
        if reverse:
            result.append(list(reversed(path)))
        else:
            result.append(path)
    return result

def sort_paths(paths, iterations=100000, reversable=True):
    '''
    This function re-orders a set of 2D paths (polylines) to minimize the
    distance required to visit each path. This is useful for 2D plotting to
    reduce wasted movements where the instrument is not drawing.

    If allowed, the algorithm will also reverse some paths if doing so reduces
    the total distance.

    The code uses simulated annealing as its optimization algorithm. The number
    of iterations can be increased to improve the chances of finding a perfect
    solution. However, a perfect solution isn't necessarily required - we just
    want to find something good enough.

    With randomly generated paths, the algorithm can quickly find a solution
    that reduces the extra distance to ~25 percent of its original value.
    '''
    state = Model(list(paths), reversable)
    max_temp = anneal.get_max_temp(state, 10000)
    min_temp = max_temp / 1000.0
    state = anneal.anneal(state, max_temp, min_temp, iterations)
    for path, reverse in zip(state.paths, state.reverse):
        if reverse:
            path.reverse()
    return state.paths

def sort_points(points, iterations=100000):
    '''
    Like sort_paths, but operates on individual points instead.
    This is basically a traveling salesman optimization.
    '''
    paths = [[x] for x in points]
    paths = sort_paths(paths, iterations, False)
    points = [x[0] for x in paths]
    return points

class Model(object):
    def __init__(self, paths, reversable=True, reverse=None, distances=None, total_distance=None):
        self.paths = paths
        self.reversable = reversable
        self.reverse = reverse or [False] * len(self.paths)
        if distances:
            self.total_distance = total_distance or 0
            self.distances = distances
        else:
            self.total_distance = 0
            self.distances = [0] * (len(paths) - 1)
            self.add_distances(range(len(self.distances)))
    def subtract_distances(self, indexes):
        n = len(self.distances)
        for i in indexes:
            if i >= 0 and i < n:
                self.total_distance -= self.distances[i]
    def add_distances(self, indexes):
        n = len(self.distances)
        for i in indexes:
            if i < 0 or i >= n:
                continue
            j = i + 1
            if self.reverse[i]:
                x1, y1 = self.paths[i][0]
            else:
                x1, y1 = self.paths[i][-1]
            if self.reverse[j]:
                x2, y2 = self.paths[j][-1]
            else:
                x2, y2 = self.paths[j][0]
            self.distances[i] = math.hypot(x2 - x1, y2 - y1)
            self.total_distance += self.distances[i]
    def energy(self):
        # return the total extra distance for this ordering
        return self.total_distance
    def do_move(self):
        if self.reversable and random.random() < 0.25:
            # mutate by reversing a random path
            n = len(self.paths) - 1
            i = random.randint(0, n)
            indexes = [i - 1, i]
            self.subtract_distances(indexes)
            self.reverse[i] = not self.reverse[i]
            self.add_distances(indexes)
            return (1, i, 0)
        else:
            # mutate by swapping two random paths
            n = len(self.paths) - 1
            i = random.randint(0, n)
            j = random.randint(0, n)
            indexes = set([i - 1, i, j - 1, j])
            self.subtract_distances(indexes)
            self.paths[i], self.paths[j] = self.paths[j], self.paths[i]
            self.add_distances(indexes)
            return (0, i, j)
    def undo_move(self, undo):
        # undo the previous mutation
        mode, i, j = undo
        if mode == 0:
            indexes = set([i - 1, i, j - 1, j])
            self.subtract_distances(indexes)
            self.paths[i], self.paths[j] = self.paths[j], self.paths[i]
            self.add_distances(indexes)
        else:
            indexes = [i - 1, i]
            self.subtract_distances(indexes)
            self.reverse[i] = not self.reverse[i]
            self.add_distances(indexes)
    def copy(self):
        # make a copy of the model
        return Model(
            list(self.paths), self.reversable, list(self.reverse),
            list(self.distances), self.total_distance)

def test(n_paths, n_iterations, seed=None):
    random.seed(seed)
    paths = []
    for _ in range(n_paths):
        x1 = random.random()
        y1 = random.random()
        x2 = random.random()
        y2 = random.random()
        path = [(x1, y1), (x2, y2)]
        paths.append(path)
    before = Model(paths).energy()
    if n_iterations:
        paths = sort_paths(paths, n_iterations)
    else:
        paths = sort_paths_greedy(paths)
    after = Model(paths).energy()
    pct = 100.0 * after / before
    return pct

if __name__ == '__main__':
    # test the module
    for n_paths in [10, 100, 1000, 10000]:
        for n_iterations in [None, 10, 100, 1000, 10000, 100000, 1000000]:
            pct = test(n_paths, n_iterations, 123)
            print(n_paths, n_iterations, pct)
