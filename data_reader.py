#!/usr/bin/python

__author__ = "ricardocdlr"

import json
import math

def calculate_distance(long_1, lat_1, long_2, lat_2):
	d_lat = (lat_2 - lat_1) * math.pi / 180
	d_long = (long_2 - long_1) * math.pi / 180
	lat_1 = lat_1 * math.pi / 180
	lat_2 = lat_2 * math.pi / 180

	a = math.sin(d_lat / 2) * math.sin(d_lat / 2) + math.sin(d_long / 2) * \
	math.sin(d_long / 2) * math.cos(lat_1) * math.cos(lat_2)
	c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
	return R * c

def generate_data_point(y, x):
	global count
	global point_list

	point = {}
	point['index'] = 0
	point['311s'] = 0
	point['SFPD_incidents'] = 0
	point['bicycle_parking'] = 0
	
	#Non Payment, Failure to Sign Renewal, Owner Move In
	#Demolition, Capital Improvement, Substantial Rehab, Ellis Act Withdrawal
	#Condo Conversion, Late Payments, Development
	point['cat1_eviction_notices'] = 0
	
	#Lead Remediation
	point['cat2_eviction_notices'] = 0
	
	#Breach, Nuisance, Illegal Use, Unapproved Subtenant, Access Denial
	point['cat3_eviction_notices'] = 0
	
	point['fire_safety_complaints'] = 0
	point['fire_violations'] = 0
	point['healthcare_facilities'] = 0
	point['offstreet_parking'] = 0
	point['recreation_sites'] = 0
	point['street_trees'] = 0

	for data in data_311['data']:
		if ((not (data[21][1] == None)) and (not (data[21][2] == None))):
			if (calculate_distance(x, y, float(data[21][2]), float(data[21][1])) <= RANGE):
				point['311s'] = point['311s'] + 1
	
	for data in data_SFPD_incidents['data']:
		if (calculate_distance(x, y, float(data[17]), float(data[18])) <= RANGE):
			point['SFPD_incidents'] = point['SFPD_incidents'] + 1

	for data in data_parking['data']:
		if (calculate_distance(x, y, float(data[17][2]), float(data[17][1])) <= RANGE):
			point['offstreet_parking'] = point['offstreet_parking'] + 1

	for data in data_bike_parking['data']:
		if (calculate_distance(x, y, float(data[16][2]), float(data[16][1])) <= RANGE):
			point['bicycle_parking'] = point['bicycle_parking'] + 1

	for data in data_parks_recs['data']:
		if (not int(data[0]) == 1):
			if ((not (data[18][2] == None)) and (not (data[18][1] == None))):
				if (calculate_distance(x, y, float(data[18][2]), float(data[18][1])) <= RANGE):
					point['recreation_sites'] = point['recreation_sites'] + 1

	for data in data_evictions['data']:
		if ((not (data[37][2] == None)) and (not (data[37][1] == None))):
			if (calculate_distance(x, y, float(data[37][2]), float(data[37][1])) <= RANGE):
				if (data[14] or data[18] or data[21] or data[22] or data[23] or data[24] or \
					data[25] or data[26] or data[29] or data[31]):
					point['cat1_eviction_notices'] = point['cat1_eviction_notices'] + 1
				elif (data[30]):
					point['cat2_eviction_notices'] = point['cat2_eviction_notices'] + 1
				elif (data[15] or data[16] or data[17] or data[19] or data[20]):
					point['cat3_eviction_notices'] = point['cat3_eviction_notices'] + 1

	for data in data_fire_complaints['data']:
		if ((not (data[25][2] == None)) and (not (data[25][1] == None))):
			if (calculate_distance(x, y, float(data[25][2]), float(data[25][1])) <= RANGE):
				point['fire_safety_complaints'] = point['fire_safety_complaints'] + 1

	for data in data_fire_violations['data']:
		if ((not (data[25][2] == None)) and (not (data[25][1] == None))):
			if (calculate_distance(x, y, float(data[25][2]), float(data[25][1])) <= RANGE):
				point['fire_violations'] = point['fire_violations'] + 1

	for data in data_trees['data']:
		if ((not (data[23]== None)) and (not (data[24]== None))):
			if (calculate_distance(x, y, float(data[24]), float(data[23])) <= RANGE):
				point['street_trees'] = point['street_trees'] + 1
	
	for data in data_healthcare_facilities['data']:
		if ((not (data[13][2] == None)) and (not (data[13][1] == None))):
			if (calculate_distance(x, y, float(data[13][2]), float(data[13][1])) <= RANGE):
				point['healthcare_facilities'] = point['healthcare_facilities'] + 1

	if (not ((point['311s'] == 0) and (point['SFPD_incidents'] == 0) and \
		(point['bicycle_parking'] == 0) and (point['cat1_eviction_notices'] == 0) and \
		(point['cat2_eviction_notices'] == 0) and (point['cat3_eviction_notices'] == 0) and \
		(point['fire_safety_complaints'] == 0) and (point['fire_violations'] == 0) and \
		(point['healthcare_facilities'] == 0) and (point['offstreet_parking'] == 0) and \
		(point['recreation_sites'] == 0) and (point['street_trees'] == 0))):
		count = count + 1
		point['index'] = count
		point_list.append(point)


def scan_data(x_start, y_start, x_end, y_end):
	x_end = float(x_end)
	y_end = float(y_end)

	y = float(y_start)
	while (y <= y_end):
		x = float(x_start)
		while (x <= x_end) :
			generate_data_point(y, x)
			x = x + COORDINATE_RANGE
		y = y + COORDINATE_RANGE

def main():

	R = 6371

	LAT_SOUTHEAST = 37.725
	LAT_GGB = 37.810
	LAT_NORTHWEST = 37.787

	LONG_SOUTHEAST = -122.387
	LONG_GGB = -122.478
	LONG_NORTHWEST = -122.508

	COORDINATE_RANGE = 0.003
	RANGE = 0.25

	count = 0
	point_list = []

	dir_311 = '311_case_data.json'
	dir_offstreet_parking = 'offstreet_parking.json'
	dir_bicycle_parking = 'bicycle_parking.json'
	dir_recreation_sites = 'recreation_sites.json'
	dir_eviction_notices = 'eviction_notices.json'
	dir_fire_complaints = 'fire_safety_complaints.json'
	dir_fire_violations = 'fire_violations.json'
	dir_trees = 'street_tree_list.json'
	dir_healthcare_facilities = 'healthcare_facilities.json'
	dir_SFPD_incidents = 'SFPD_incidents.json'

	data_311 = json.loads(open(dir_311).read())
	print '311 calls loaded'

	data_SFPD_incidents = json.loads(open(dir_SFPD_incidents).read())
	print 'SFPD incidents loaded'

	data_parking = json.loads(open(dir_offstreet_parking).read())
	print 'off-street parking loaded'

	data_bike_parking = json.loads(open(dir_bicycle_parking).read())
	print 'bicycle parking loaded'

	data_parks_recs = json.loads(open(dir_recreation_sites).read())
	print 'parks and recreation sites loaded'

	data_evictions = json.loads(open(dir_eviction_notices).read())
	print 'eviction notices loaded'

	data_fire_complaints = json.loads(open(dir_fire_complaints).read())
	print 'fire safety complaints loaded'

	data_fire_violations = json.loads(open(dir_fire_violations).read())
	print 'fire safety violations loaded'

	data_trees = json.loads(open(dir_trees).read())
	print 'public trees loaded'

	data_healthcare_facilities = json.loads(open(dir_healthcare_facilities).read())
	print 'healthcare facilities loaded'

	print '________________________________________________________'
	scan_data(LONG_NORTHWEST, LAT_SOUTHEAST, LONG_GGB, LAT_NORTHWEST)
	scan_data(LONG_GGB, LAT_SOUTHEAST, LONG_SOUTHEAST, LAT_GGB)

	print 'data scanned'

	with open('data_set.json', 'w') as fp:
		json.dump(point_list, fp)

if __name__ == "__main__":
	main()
