#!/usr/bin/python

__author__ = "ricardocdlr"

import json

def main():

	dir_json = 'data_set.json'
	data = json.loads(open(dir_json).read())

	#Maximums
	offstreet_max = 0.0
	tree_max = 0.0
	complaints_max = 0.0
	violations_max = 0.0
	cat1_max = 0.0
	cat2_max = 0.0
	cat3_max = 0.0
	health_max = 0.0
	parks_max = 0.0
	bike_max = 0.0

	SFPD_max = 0.0
	max_311 = 0.0

	#Find maximum tallies.
	for point in data:
		if point['bicycle_parking'] > bike_max:
			bike_max = point['bicycle_parking']
		if point['cat1_eviction_notices'] > cat1_max:
			cat1_max = point['cat1_eviction_notices']
		if point['cat2_eviction_notices'] > cat2_max:
			cat2_max = point['cat2_eviction_notices']
		if point['cat3_eviction_notices'] > cat3_max:
			cat3_max = point['cat3_eviction_notices']
		if point['fire_violations'] > violations_max:
			violations_max = point['fire_violations']
		if point['fire_safety_complaints'] > complaints_max:
			complaints_max = point['fire_safety_complaints']
		if point['healthcare_facilities'] > health_max:
			health_max = point['healthcare_facilities']
		if point['offstreet_parking'] > offstreet_max:
			offstreet_max = point['offstreet_parking']
		if point['recreation_sites'] > parks_max:
			parks_max = point['recreation_sites']
		if point['street_trees'] > tree_max:
			tree_max = point['street_trees']

		if point['SFPD_incidents'] > SFPD_max:
			SFPD_max = point['SFPD_incidents']
		if point['311s'] > max_311:
			max_311 = point['311s']

	print(SFPD_max, max_311)

	print(bike_max, cat1_max, cat2_max, cat3_max, violations_max, complaints_max, health_max, offstreet_max, parks_max, tree_max)

	for point in data:
		#Scale tallies between [0, 1]
		point['bicycle_parking'] = float(point['bicycle_parking']) / bike_max
		point['cat1_eviction_notices'] = float(point['cat1_eviction_notices']) / cat1_max
		point['cat2_eviction_notices'] = float(point['cat2_eviction_notices']) / cat2_max
		point['cat3_eviction_notices'] = float(point['cat3_eviction_notices']) / cat3_max
		point['fire_violations'] = float(point['fire_violations']) / violations_max
		point['fire_safety_complaints'] = float(point['fire_safety_complaints']) / complaints_max
		point['healthcare_facilities'] = float(point['healthcare_facilities']) / health_max
		point['offstreet_parking'] = float(point['offstreet_parking']) / offstreet_max
		point['recreation_sites'] = float(point['recreation_sites']) / parks_max
		point['street_trees'] = float(point['street_trees']) / tree_max

		#Put label tallies into 1000 buckets
		point['311s'] = point['311s'] / (max_311 / 1000)
		point['SFPD_incidents'] = point['SFPD_incidents'] / (SFPD_max / 1000)

	with open('data_set_1000.json', 'w') as fp:
		json.dump(data, fp)

if __name__ == "__main__":
	main()
