import random, sys
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from sklearn.decomposition import PCA
import pandas as pd

class kmeans():

    def __init__(self, path, k, pca_dims=2):
        """
        initializes the kmeans algorithm by specifying important information
        for algorithm to know
        :param path: path to the data
        :param k: main parameter to the kmeans algorithm- how many groups to
        classify into
        """

        # split into test, train data
        self.train = get_data(path)

        # create k x-dimensional center coordinates randomly
        self.dimensions = len(self.train)
        self.centers = [random.choice([*zip(*self.train)]) for _ in range(k)]
        # current classes
        self.classes = [[[] for dim in range(self.dimensions)] for _ in range(k)]

        self.pca_dims = pca_dims

    def run(self, n=100, display_every=10):
        """
        runs the kmeans algorithm based on parameters given to object
        :param n: number of iterations to run algorithm for
        """

        for i in range(n):
            self._iterations = i
            self._classify()
            if i % display_every == 0: self._visualize()
            if self._change_centers(1e-12): break
        self._visualize()

    def _classify(self):
        """
        classifies all points (assignment step)
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
        does the classifying of the point based on distance from each centroid
        center point
        :param xs: the coordinate of the point to classify, in iterable form
        """

        # defined distance function between two points
        def distance(a, b):
            return np.sum(np.power(np.array(a) - np.array(b), 2)) ** (0.5)
        dists = [distance(xs, center) for center in self.centers]

        # find the smallest distance between all centers
        return np.argmin(dists)


    def _change_centers(self, threshold=1e-10):
        """
        find new center points of the centroids by calculating the "mean"
        point for each current class (update step)
        :param threshold: difference threshold
        :return: whether the differences are all less than the threshold
        """

        # find new centers
        new_centers = [[np.mean(dim) if len(dim) > 0 else 0 for dim in _class] for _class in self.classes]
        # figure out if difference is significant (all less than threshold)
        diffs = []
        for ind, center in enumerate(self.centers):
            diffs.append(sum([(new_centers[ind][i]-center[i]) ** 2 for i in range(len(center))]) ** (0.5))
        if np.max(diffs) < threshold:
            return True
        else:
            self.centers = new_centers
            return False

    def _visualize(self):
        fig = plt.figure()
        if self.pca_dims == 3:
            ax = fig.add_subplot(111, projection='3d')
        elif self.pca_dims == 2:
            ax = fig.add_subplot(111)

        # PCA down to 3 dimensions- but add everything into 1
        all_data = [[] for _ in range(self.dimensions)]
        breaks = [0]
        for ind, dimension in enumerate(all_data):
            # add all classes
            for _class in self.classes:
                dimension += _class[ind]
                # mark down where each class values end for later
                if ind == 0: breaks.append(len(dimension))
            # add all centroids
            for center in self.centers:
                dimension.append(center[ind])
            # mark down where the centroids end for later
            if ind == 0: breaks.append(len(dimension))

        
        # use scikit learn's PCA (transpose to make sure input is correct)
        reduced_data = PCA(n_components=self.pca_dims).fit_transform(np.array(all_data).T)

        # find each group to plot, plot it
        for i in range(1, len(breaks) - 1):
            if self.pca_dims == 2:
                x, y = reduced_data[breaks[i-1]:breaks[i]].T
                plt.scatter(x, y, label="group {}".format(i))
            elif self.pca_dims == 3:
                x, y, z = reduced_data[breaks[i-1]:breaks[i]].T
                ax.scatter(x, y, z, label="group {}".format(i))
            
        # plot center points
        if self.pca_dims == 2:
            x, y = reduced_data[breaks[-2]:breaks[-1]].T
            plt.scatter(x, y, c='r', label="center")
        elif self.pca_dims == 3:
            x, y, z = reduced_data[breaks[-2]:breaks[-1]].T
            ax.scatter(x, y, z, c='r', label="center")

        box = ax.get_position()
        ax.set_position([box.x0, box.y0,
                         box.width * 0.8, box.height])
        plt.legend(bbox_to_anchor=(1.05, 1), borderaxespad=0.)
        plt.title("k: {}, iterations: {}".format(len(self.centers), self._iterations))
        plt.show()


### ONLY FOR PRELIMINARY TESTING ###
#
# def data_gen(filepath, dimensions):
#     with open(filepath) as f:
#         d = json.load(f)
#     data = [[] for i in range(dimensions)]
#     for c in d:
#         bounddistance = d[c]["BoundDistance"]
#         size = d[c]["Number"]
#         for i in range(dimensions):
#             cur_centre = d[c]["Centres"][i]
#             data[i] += np.random.uniform(
#                 low=(cur_centre - bounddistance),
#                 high=(cur_centre + bounddistance),
#                 size=size
#             ).tolist()
#     return data


def get_data(filepath):
    """
    convert data into format:
    [[x1's], [x2's], [x3's], ...] (depending on number of dimensions data is in)
    :param filepath: path to specific file type in format: 
    data.frame with columns: "post #", "username", "text", (7 Watson API output emotions)
    """
    all_data = pd.read_csv(filepath)
    # get the appropriate columns' values
    select_vals = all_data.iloc[:,all_data.columns.get_loc('Anger'):].values

    # required format is all values of 1 dimension are in same array
    return select_vals.T.tolist()


def main():
    path = "../../data/raw/sentiments/"
    file = "mamistruggling" + "200_sentencelevelsentiments.csv"
    for k in range(11, 19):
        a = kmeans(path + file, k=k, pca_dims=2)
        a.run(n=500, display_every=100)

if __name__ == "__main__":
    main()
