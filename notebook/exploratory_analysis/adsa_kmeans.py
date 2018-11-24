# Inbuilt packagges
import json
import random
import sys

import matplotlib.pyplot as plt

# Own packages
from adsa_data_gen import data_gen


class k_means():

	def __init__(self, path):
		with open(path) as f:
			d = json.load(f)
		self.data_gen = data_gen(dimensions=2, kwargs=d)
		self.test, self.train = self.data_gen.create_data()
		self.x = self.train[0]
		self.y = self.train[1]
		# plt.plot(self.x, self.y, 'ro')
		# plt.show()
		# RANDOMLY SELECT STARTING POINTS (should be parameterized)
		self.x_center1 = random.choice(self.x)
		self.y_center1 = random.choice(self.y)
		self.x_center2 = random.choice(self.x)
		self.y_center2 = random.choice(self.y)
		self.cur_class1 = [[], []]
		self.cur_class2 = [[], []]

	def _classify(self):
		"""
		Call the helper _classify function on all points and store them
		in the respective array according to what it is classified as
		"""

		# delete previous data
		self.cur_class1 = [[], []]
		self.cur_class2 = [[], []]

		# loop through each point and classify
		for x, y in zip(self.x, self.y):
			if self._classify_helper(x, y):
				self.cur_class1[0].append(x)
				self.cur_class1[1].append(y)
			else:
				self.cur_class2[0].append(x)
				self.cur_class2[1].append(y)

	def _change_centres(self):
		"""
		After each iteration the cluster center changes
		Calculate the new cluster centers and store them in the
		class' member variables
		"""
		
		# set the new center points as the average of the current clusters
		# if centers don't move that much, then quit program (rather than choosing n for convergence)
		self.x_center1 = sum(self.cur_class1[0]) / len(self.cur_class1[0])
		self.y_center1 = sum(self.cur_class1[1]) / len(self.cur_class1[1])
		self.x_center2 = sum(self.cur_class2[0]) / len(self.cur_class2[0])
		self.y_center2 = sum(self.cur_class2[1]) / len(self.cur_class2[1])

	def run(self, k=2, n=100):
		"""
		Call classify to complete the class
		"""
		for i in range(n):
			self._classify()

	def _classify_helper(self, x, y):
		"""
		In this function you should return which
		class will the point (x,y) be classified as

		Return 0 when class 1
		Return 1 when class 2
		"""
		dist0 = ((x - self.x_center1) ** 2 + (y - self.y_center1) ** 2) ** (0.5)
		dist1 = ((x - self.x_center2) ** 2 + (y - self.y_center2) ** 2) ** (0.5)

		if dist0 > dist1:
			return 1
		return 0

	def error(self):
		class1_sum, class2_sum = 0, 0
		for x, y in zip(self.cur_class1[0], self.cur_class1[1]):
			class1_sum += ((x - self.x_center1) ** 2 + (y - self.y_center1) ** 2) ** (0.5)
		for x, y in zip(self.cur_class2[0], self.cur_class2[1]):
			class2_sum += ((x - self.x_center2) ** 2 + (y - self.y_center2) ** 2) ** (0.5)
		return class1_sum / len(self.cur_class1[0]) + class2_sum / len(self.cur_class2[0])

def main(path, k=10):
	ks = []
	errors = []
	for i in range(1, 100):
		kmeans = k_means(path=path)
		kmeans.run(i)
		err = kmeans.error()
		errors.append(err)
		ks.append(i)
	plt.plot(ks, errors)
	plt.show()


if __name__ == "__main__":
	sys.exit(main(path="./data_sets/data_set.json", k=100))
