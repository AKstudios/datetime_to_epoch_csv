# datetime_to_epoch_csv
This script takes a datafile with datetimes, locations, visits, variables and values, and converts datetime to epoch times at UTC.

The exact order of expected columns in the datafile is:
_DateTime,HouseNumber,Visit,Test,Location,Monitor,Variable,Unit,Value_

To run the script, provide the filename as argument. 

Example:

```
python utc.py CO2_IN.csv
```

# Dependencies:
[tqdm](https://github.com/tqdm/tqdm) and [OrderedSet](https://pypi.org/project/orderedset/)
