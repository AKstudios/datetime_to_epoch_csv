# ===========================================================================
# This code takes a processed csv file as argument, extracts unique timestamps
# based on HouseNumber, visit and location and converts them into epoch times.
# This is for processing HUD project's data files

# Developed by Akram Ali
# Updated on: 05/17/2019

# ===========================================================================
# import libraries
# ===========================================================================

import csv
import itertools
from datetime import datetime, timedelta
import datetime as dtz
from tqdm import tqdm
from ordered_set import OrderedSet
import sys

# ===========================================================================
# define global variables
# ===========================================================================

filename = str(sys.argv[1])       # read filename from argument
count = 0
dt=[]
all_locations=[]
all_visits=[]
all_variables=[]
points=[]
indices=[]

# ===========================================================================
# read file and extract datetime, locations & visits
# ===========================================================================

with open(filename, 'r') as file:
    print ("reading CSV file ..")
    csv_data = list(csv.reader(file, delimiter =',')) # read csv file in a list
    csv_data.pop(0) # remove headers

print ("extracting datetime, locations & visits ..")
for row in tqdm(csv_data):
    # convert first column to datetime objects
    dt.append(datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S'))
    all_locations.append(row[1])    # get all locations from second column
    all_visits.append(row[2])       # get all visits from third column
    all_variables.append(row[6])    # get all visits from seventh column

# ===========================================================================
# extract time ranges and indices for unique variables
# ===========================================================================

# create an ordered set for all variables to iterate through
locations = OrderedSet(all_locations)
visits = OrderedSet(all_visits)
variables = OrderedSet(all_variables)

print ("sorting all locations and visits ..")
for location in tqdm(locations):
    for visit in visits:
        for variable in variables:
            flag = 0
            i=0     # counter for first timestamp
            n=0     # counter for number of timestamps for that location/visit
            for row in csv_data:
                i+=1
                if row[1]==location and row[2]==visit and row[6]==variable:
                    if flag == 0:
                        _i = i
                        flag = 1
                    n+=1

            if n > 0:
                points.append(n-1)
            else:
                points.append(0)
            indices.append(_i-1)

# ===========================================================================
# replace timestamps into epoch times using indices and points created before
# ===========================================================================

print ("replacing timestamps with epoch times in UTC ..")
for a in tqdm(range(len(indices))):
    if points[a] == 0:
        pass
    else:
        b = indices[a]
        utc = datetime.strptime(csv_data[b][0], '%Y-%m-%d %H:%M:%S').replace(tzinfo=dtz.timezone.utc)
        for n in range(points[a]+1):
            epoch = utc.timestamp()     # this converts the datetime into epoch
            csv_data[b][0] = epoch
            utc += timedelta(seconds=60)    # increment timestamp by 1 minute
            b += 1

# ===========================================================================
# save final list into a csv file
# ===========================================================================

print ("writing epoch times to csv file ..")
with open('%s.epoch' % filename, 'w', newline='') as myfile:
    wr = csv.writer(myfile)
    header = ['DateTime','HouseNumber','Visit','Test','Location','Monitor',
    'Variable','Unit','Value']
    wr.writerow(header)
    wr.writerows(csv_data)

# ===========================================================================
# done!
# ===========================================================================

print ("done")
