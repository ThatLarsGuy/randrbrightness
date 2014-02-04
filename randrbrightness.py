#!/usr/bin/env python2
import sys
import os
import cPickle as pickle
from subprocess import call

#Configuration
pickle_filepath = "/home/me/randrbrightness/current_state.pickle"
default_brightness = 1.0	#Default brightness
default_colour_temp = 6000	#Default/maximum colour temp
minimum_colour_temp = 3000	#Minimum colour temp
brightness_increment = 0.1
colour_temp_increment = 300


#Retrieve current brightness from disk, otherwise set default value
if not os.path.exists(pickle_filepath):
    current_state = {}
    current_state['current_brightness'] = default_brightness
    current_state['current_colour_temp'] = default_colour_temp
else:
    with open(pickle_filepath) as pickle_handle:
        current_state = pickle.load(pickle_handle)

print 'Current brightness: ' + str(current_state['current_brightness']) + ' - Current temp: ' + str(current_state['current_colour_temp']) + ' - Change: ' + sys.argv[1]

#Move brightness/temp up or down, depending on argument
if sys.argv[1] == 'up':
	if current_state['current_brightness'] < 1.0:
		current_state['current_brightness'] += brightness_increment
if sys.argv[1] == 'down':
	if current_state['current_brightness'] > brightness_increment:
		current_state['current_brightness'] -= brightness_increment
if sys.argv[1] == 'warmer':
	if current_state['current_colour_temp'] > minimum_colour_temp:
		current_state['current_colour_temp'] -= colour_temp_increment
if sys.argv[1] == 'cooler':
	if current_state['current_colour_temp'] < default_colour_temp:
		current_state['current_colour_temp'] += colour_temp_increment

#Persist current brightness to disk
with open(pickle_filepath, 'w') as pickle_handle:
	pickle.dump(current_state, pickle_handle)


#Apply current brightness
#eg: redshift -o -l 0:0 -m randr -t 4000:4000 -b 1.0
call(["redshift", "-o", "-l", "0:0", "-m", "randr", "-t", str(current_state['current_colour_temp'])+":"+str(current_state['current_colour_temp']), "-b", str(current_state['current_brightness'])])


