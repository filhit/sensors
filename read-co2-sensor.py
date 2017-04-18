import os
import datetime
import sys
import getopt

def get_last_modified_file(directory):
  dated_files = [(os.path.getmtime(os.path.join(directory, fn)), os.path.join(directory, fn)) 
               for fn in os.listdir(directory) if fn.lower().endswith('.csv')]
  dated_files.sort()
  dated_files.reverse()
  newest = dated_files[0][1]
  return newest

def get_last_line_in_file(path):
  with open(path) as file:
    file.seek(-1024, 2)
    return file.readlines()[-1] 

def parse_sensor_output(line):
  data = line.split(",")
  return {
    "time": datetime.datetime.strptime(data[0], "%Y-%m-%d %H:%M:%S"),
    "temperature": float(data[1]),
    "co2": float(data[2])
  }   

def sensor_dead(sensor_output):
  diff = datetime.datetime.now() - sensor_output["time"]
  sensor_dead_threshold = datetime.timedelta(seconds = 30)
  return diff > sensor_dead_threshold

file = get_last_modified_file("/var/lib/co2monitor/data")
line = get_last_line_in_file(file)
sensor_output = parse_sensor_output(line)
if sensor_dead(sensor_output):
  sys.exit("sensor dead")

options, args = getopt.getopt(sys.argv[1:], "", ["co2","temperature"])
for o, a in options:
  if o == "--co2":
    print sensor_output["co2"]
  elif o == "--temperature":
    print sensor_output["temperature"]

