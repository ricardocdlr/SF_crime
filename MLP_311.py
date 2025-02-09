#!/usr/bin/python

__author__ = "ricardocdlr"

import tensorflow as tf
import numpy as np
import json

import matplotlib.pyplot as mlp

from dataset import DataSet

def append_vector(array_x, array_y, point):
	vector_x = []
	vector_y = []

	vector_x.append(float(point['bicycle_parking']))
	vector_x.append(float(point['cat1_eviction_notices']))
	vector_x.append(float(point['cat2_eviction_notices']))
	vector_x.append(float(point['cat3_eviction_notices']))
	vector_x.append(float(point['fire_safety_complaints']))
	vector_x.append(float(point['fire_violations']))
	vector_x.append(float(point['healthcare_facilities']))
	vector_x.append(float(point['offstreet_parking']))
	vector_x.append(float(point['recreation_sites']))
	vector_x.append(float(point['street_trees']))

	#vector_y.append(point['311s'])

	for a in xrange(MAX_311):
		if (a == point['311s']):
			vector_y.append(1.0)
		else:
			vector_y.append(0.0)

	array_x.append(vector_x)
	array_y.append(vector_y)

def main():

	#Import and format data into tensors.
	dir_json = 'data_set_1000.json'
	data = json.loads(open(dir_json).read())

	training_x = []
	testing_x = []

	training_y = []
	testing_y = []

	MAX_311 = 285

	for point in data:
		if (point['index'] % 2 == 0):
			append_vector(testing_x, testing_y, point)
		else:
			append_vector(training_x, training_y, point)

	train_data = DataSet(training_x, training_y)

	train_len = len(training_x)
	test_len = len(testing_x)
	batch_size = 400
	steps = 16000

	#Create session.
	sess = tf.InteractiveSession()

	#Input placeholders.
	x = tf.placeholder(tf.float32, [None, 10])
	y_expected = tf.placeholder(tf.float32, shape=[None, MAX_311])

	#Neural network hidden layers and variables.
	W1 = tf.Variable(tf.random_normal([10, 500]))
	b1 = tf.Variable(tf.constant(0.0, shape=[500]))
	h1 = tf.nn.relu(tf.matmul(x, W1) + b1)

	W2 = tf.Variable(tf.random_normal([500, 500]))
	b2 = tf.Variable(tf.constant(0.0, shape=[500]))
	h2 = tf.nn.relu(tf.matmul(h1, W2) + b2)

	W3 = tf.Variable(tf.random_normal([500, 1000]))
	b3 = tf.Variable(tf.constant(0.0, shape=[1000]))
	h3 = tf.nn.relu(tf.matmul(h2, W3) + b3)

	h3 = tf.nn.dropout(h3, 0.5)

	#Neural network output.
	W4 = tf.Variable(tf.random_normal([1000, MAX_311]))
	b4 = tf.Variable(tf.constant(0.0, shape=[MAX_311]))
	y = tf.nn.relu(tf.matmul(h3, W4) + b4)

	#Error measure.
	cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(y, y_expected))

	#Minimize cross_entropy with gradient descent.
	train_step = tf.train.GradientDescentOptimizer(.00001).minimize(cross_entropy)

	#Calculate error.
	correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_expected, 1))
	error = 1 - tf.reduce_mean(tf.cast(correct_prediction, "float"))

	#Train.
	saver = tf.train.Saver()
	ces = [0]*(train_len * steps / batch_size)
	errors = [0]*(((train_len / batch_size + 10) * steps) / 1)

	full_set = {x : training_x, y_expected : training_y}

	sess.run(tf.initialize_all_variables())
	validation = {x : testing_x, y_expected : testing_y}
	for i in range(steps):
		for j in range(train_len / batch_size):
			batch_xs, batch_ys = train_data.next_batch(batch_size)
			feed = {x : batch_xs, y_expected : batch_ys}
			train_step.run(feed_dict=feed)
			ce = cross_entropy.eval(feed_dict=feed)
			ces[((train_len / batch_size)* i)+j] = ce
			if (j % 10 == 0):
				e = error.eval(feed_dict=validation)
				errors[(train_len * i / (10 * batch_size)) + (j / 10)] = e
		print "Epoch " + str(i)

	print "Test data accuracy:"
	print 1 - error.eval(feed_dict=validation)

	temp = 0

	for a in xrange(len(ces)):
		if ces[a] != 0:
			temp = a

	ces = ces[0:temp]
	temp = 0

	for a in xrange(len(errors)):
		if errors[a] != 0:
			temp = a

	errors = errors[0:temp]

	mlp.plot(ces, 'ro')
	mlp.ylabel('Cross entropy')
	mlp.xlabel('Batch')
	mlp.title('Cross Entropy Over Batches')
	mlp.show()

	mlp.plot(errors, 'bo')
	mlp.ylabel('Validation Error')
	mlp.xlabel('Batch (X10)')
	mlp.title('Validation Error Over Batches')
	mlp.show()

if __name__ == "__main__":
	main()
