import random
import sys
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import json

class kmeans():

    def __init__(self, path, k):
        """

        """

        # split into test, train data
        self.train = data_gen(path, dimensions=3)

        # create k x-dimensional center coordinates randomly
        self.dimensions = len(self.train)
        self.centers = [random.choice([*zip(*self.train)]) for _ in range(k)]
        # current classes
        self.classes = [[[] for dim in range(self.dimensions)] for _ in range(k)]

    def run(self, n=100):
        """

        """

        for i in range(n):
            self._iterations = i
            self._classify()
            if i % 10 == 0: self._visualize()
            self._change_centers()

    def _classify(self):
        """

        """

        # erase current classes
        self.classes = [[[] for dim in range(self.dimensions)] for _ in range(len(self.classes))]

        # classify the current coordinate, add to identified classes
        for xs in zip(*self.train):
            curr_class = self._classify_helper(xs)
            for _ind, _class in enumerate(self.classes[curr_class]):
                _class.append(xs[_ind])
        # print(self.classes)

    def _classify_helper(self, xs):
        """

        """

        # euclidean distance between each coordinate and center
        dists = [sum([(xs[dim] - center[dim]) ** 2 for dim in range(len(center))]) ** (0.5) for center in self.centers]

        # find the smallest distance between all centers
        return np.argmin(dists)

    def _change_centers(self):
        """

        """

        self.centers = [[np.mean(dim) for dim in _class] for _class in self.classes]

    def _visualize(self):
        if self.dimensions == 2:
            for _class in self.classes:
                x, y = [_class[i] for i in range(self.dimensions)]
                ax.scatter(x, y)
            x, y = [[i[j] for i in self.centers] for j in range(self.dimensions)]
            plt.scatter(x, y, c="r")
        elif self.dimensions == 3:
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            for _class in self.classes:
                x, y, z = [_class[i] for i in range(self.dimensions)]
                ax.scatter(x, y, z)
            x, y, z = [[i[j] for i in self.centers] for j in range(self.dimensions)]
            ax.scatter(x, y, z, c="r")
        plt.title("k: {}, iterations: {}".format(len(self.centers), self._iterations))
        plt.show()

def data_gen(filepath, dimensions):
    with open(filepath) as f:
        d = json.load(f)
    data = [[] for i in range(dimensions)]
    for c in d:
        bounddistance = d[c]["BoundDistance"]
        size = d[c]["Number"]
        for i in range(dimensions):
            cur_centre = d[c]["Centres"][i]
            data[i] += np.random.uniform(
                low=(cur_centre - bounddistance),
                high=(cur_centre + bounddistance),
                size=size
            ).tolist()
    return data


def main():
    for k in range(2, 4):
        a = kmeans("test_data_set.json", k)
        a.run(30)

if __name__ == "__main__":
    main()
