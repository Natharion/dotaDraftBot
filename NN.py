from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import pandas as pd
import tensorflow as tf
import os
import csv
import time
import logging

import argparse
class dotaDraftBot:
	CSV_RESULTS = []
	CSV_COLUMN_NAMES = []
	CSV_LABEL_NAME = 'Result'
	
	FEATURE_COLUMNS = []
	
	BATCH_SIZE = 100
	TRAIN_STEPS = 1000
	
	def __init__(self): #WORKS
		self.generate_column_names()
		self.generate_results()
		self.load_data()
		self.prepare()
		
	def generate_column_names(self): #WORKS
		if os.path.isfile('heroes.csv'):
			with open('heroes.csv', newline='') as csvfile:
				UnusedCounter = 0
				HeroesReader = csv.DictReader(csvfile, delimiter=';')
				for row in HeroesReader:
					if row['Name'] == 'Unused':
						self.CSV_COLUMN_NAMES.append('Unused'+str(UnusedCounter))
						UnusedCounter = UnusedCounter + 1
					else:
						self.CSV_COLUMN_NAMES.append(row['Name'])
			self.CSV_COLUMN_NAMES.append(self.CSV_LABEL_NAME)
		else:
			return False
		return True
		
	def generate_results(self): #WORKS, don't ask me why it's done that way
		self.CSV_RESULTS.append('Radiant')
		self.CSV_RESULTS.append('Dire')

	def load_data(self): #WORKS TOO
		train = pd.read_csv('learning.csv', names=self.CSV_COLUMN_NAMES, header=0)
		self.train_features, self.train_label = train, train.pop(self.CSV_LABEL_NAME)

		test = pd.read_csv('verification.csv', names=self.CSV_COLUMN_NAMES, header=0)
		self.test_features, self.test_label = test, test.pop(self.CSV_LABEL_NAME)
		return (self.train_features, self.train_label), (self.test_features, self.test_label)
	
	def prepare(self):
		for key in self.train_features.keys():
			self.FEATURE_COLUMNS.append(tf.feature_column.numeric_column(key=key))
		self.classifier = tf.estimator.DNNClassifier(
		feature_columns=self.FEATURE_COLUMNS, hidden_units=[10, 15, 20, 15, 10], n_classes=2)
		time.clock()
	
	def train_input_fn(self, features, labels, batch_size=100):
		dataset = tf.data.Dataset.from_tensor_slices((dict(features), labels))
		dataset = dataset.repeat().batch(self.BATCH_SIZE)
		print('Data preparation complete at: ' + str(time.clock()))
		return dataset.make_one_shot_iterator().get_next()
	
	def eval_input_fn(self, features, labels, batch_size=100):
		features=dict(features)
		if labels is None:
			inputs = features
		else:
			inputs = (features, labels)

		# Convert the inputs to a Dataset.
		dataset = tf.data.Dataset.from_tensor_slices(inputs)

		# Batch the examples
		assert batch_size is not None, "batch_size must not be None"
		dataset = dataset.batch(batch_size)

		# Return the read end of the pipeline.
		return dataset.make_one_shot_iterator().get_next()
	
	def train(self):
		self.classifier.train(input_fn=lambda:self.train_input_fn(self.train_features, self.train_label,self.BATCH_SIZE),steps=self.TRAIN_STEPS)
		print('Training time ' + str(time.clock()))

	def eval(self):
		eval_result = self.classifier.evaluate(input_fn=lambda:self.eval_input_fn(self.test_features, self.test_label, self.BATCH_SIZE))
		print('Test set accuracy: {accuracy:0.3f}\n'.format(**eval_result))
		return eval_result

if __name__ == '__main__':
	#args = parser.parse_args(argv[1:])
	os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
	
	NN = dotaDraftBot()
	NN.train()
	NN.eval()