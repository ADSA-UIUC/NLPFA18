import random, sys, os, re
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from sklearn.decomposition import PCA
import pandas as pd

class kmeans():

    def __init__(self, data, k, plot_title="", display_dims=0):
        """
        initializes the kmeans algorithm by specifying important information
        for algorithm to know
        :param path: path to the data
        :param k: main parameter to the kmeans algorithm- how many groups to
        classify into
        """

        np.set_printoptions(precision=4)

        self.data = data

        # to customize visualization graph
        self.plot_title = plot_title

        # create k x-dimensional center coordinates randomly
        self.dimensions = len(self.data)
        self.centers = [random.choice([*zip(*self.data)]) for _ in range(k)]
        
        # current classes
        self.classes = [[[] for dim in range(self.dimensions)] for _ in range(k)]

        self.pca_dims = display_dims

    def get_centers(self):
        return self.centers

    def run(self, error_threshold, n, display_every):
        """
        runs the kmeans algorithm based on parameters given to object
        :param n: number of iterations to run algorithm for
        """

        error = 2
        for i in range(n):
            # to use in other parts of the class
            self._iterations = i
            self._classify()
            if i % display_every == 0 and self.pca_dims > 0: self._visualize()

            # if the centers don't change, then quit out of loop
            # print("current centers")
            # print(np.array(self.centers))
            if self._change_centers(1e-5): break

            error_diff = abs(error - self.error())
            if error_diff < 1e-5: break
            error = self.error()
            # print("k: {}, iteration: {}, error: {}".format(len(self.centers), i + 1, error))

            if error < error_threshold: 
                return (True, error)
        if self.pca_dims == 2 or self.pca_dims == 3:
            self._visualize()
        return (False, self.error())

    def _classify(self):
        """
        classifies all points (assignment step)
        """

        # erase current classes
        self.classes = [[[] for dim in range(self.dimensions)] for _ in range(len(self.classes))]

        # classify the current coordinate, add to identified classes
        for xs in zip(*self.data):
            curr_class = self._classify_helper(xs)
            for ind, _class in enumerate(self.classes[curr_class]):
                # stick each coordinate of 7 dimensional point in the right arrays
                _class.append(xs[ind])

    def _classify_helper(self, xs):
        """
        does the classifying of the point based on distance from each centroid
        center point
        :param xs: the coordinate of the point to classify, in iterable form
        """

        # defined distance function between two points
        def distance(a, b):
            return np.sum((np.array(a) - np.array(b)) ** 2)
        dists = [distance(xs, center) for center in self.centers]

        # find the smallest distance between all centers
        return np.argmin(dists)

    def _change_centers(self, threshold=1e-5):
        """
        find new center points of the centroids by calculating the "mean"
        point for each current class (update step)
        :param threshold: difference threshold
        :return: whether the differences are all less than the threshold
        """

        # find new centers
        new_centers = [[np.mean(dim) if len(dim) > 0 else 0 for dim in _class] for _class in self.classes]
        centers_count = {tuple(center):new_centers.count(center) for center in new_centers}

        for i in range(len(new_centers)):
            if all([coord == 0 for coord in new_centers[i]]):
                new_centers[i] = random.choice([*zip(*self.data)])
            elif centers_count[tuple(new_centers[i])] > 1:
                new_centers[i] = random.choice([*zip(*self.data)])
        
        # figure out if difference is significant (all less than threshold)
        diffs = []
        for ind, center in enumerate(self.centers):
            diffs.append(np.max([new_centers[ind][i]-center[i] for i in range(len(center))]))

        # print("new centers")
        # print(np.array(new_centers))
        # print("diffs")
        # print(np.array(diffs))

        if np.max(diffs) < threshold:
            # print("returning True")
            return True
        else:
            # print("returning False")
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
        plt.title("{}\nk: {}, iterations: {}".format(self.plot_title, len(self.centers), self._iterations + 1))
        plt.show()

    def _euclidean_distance(self, a, b):
        """
        find euclidean distance between two points
        :return: euclidean distance
        """
        return sum([(p1 - p2) ** 2 for p1, p2 in zip(a, b)]) ** (0.5)

    def error(self):
        """
        find the error of the kmeans algorithm at the current state
        :return: average distance from each point to its center 
        """

        sum, count = 0, 0
        for dim, center in enumerate(self.centers):
            for point in self.classes[dim]:
                sum += self._euclidean_distance(point, center)
            count += len(self.classes[dim])
        return sum / count 


def get_data(folderpath, all_files=True):
    """
    convert data into format:
    [[x1's], [x2's], [x3's], ...] (depending on number of dimensions data is in)
    :param filepath: path to specific file type in format: 
    data.frame with columns: "post #", "username", "text", (7 Watson API output emotions)
    """
    filenames = os.listdir(folderpath)
    all_values = pd.DataFrame()
    for filename in filenames:
        if not re.match(".+_sentencelevelsentiments\.csv", filename):
            continue
        all_data = pd.read_csv(folderpath + filename)
        # get the appropriate columns' values
        select_vals = all_data.iloc[:,all_data.columns.get_loc('Anger'):]
        all_values = all_values.append(select_vals)
    # required format is all values of 1 dimension are in same array
    return all_values.values.T.tolist()


def main():
    path = "../data/raw/sentiments/"
    data = get_data(path)
    errors = []
    kmin, kmax = 50, 55
    for k in range(kmin, kmax):
        a = kmeans(data, k=k, display_dims=2)
        finished, error = a.run(n=20, display_every=10)
        errors.append(error)
        print("k: {}, error: {}".format(k, error))
    plt.plot(range(kmin, kmax), errors)
    plt.show()

if __name__ == "__main__":
    sys.exit(main())
