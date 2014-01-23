#!/usr/bin/env python2
import sys
import os
import cPickle as pickle
from subprocess import call

#Configuration
pickle_filepath = "/home/me/randrbrightness/current_brightness.pickle"

default_brightness = 1.0	#(Full brightness)

brightness_increment = 0.1

max_colour_temp = 5000		#Default colour temp (5000 is a bit 'warmer')

temp_reduction_increment = 300	#For each 0.1 brightness decrease, this value will be subtracted from the gamma
				#(I like the colour temp to grow 'warmer' as the brightness decreases)
				#Set this to 0 if you don't want the colour temp to change



#Retrieve current brightness from disk, otherwise set default value
if not os.path.exists(pickle_filepath):
    current_brightness = default_brightness
else:
    with open(pickle_filepath) as pickle_handle:
        current_brightness = pickle.load(pickle_handle)

print str(current_brightness) + ' moving ' + sys.argv[1]

#Move brightness up or down, depending on argument
if sys.argv[1] == 'up':
	if current_brightness < 1.0:
		current_brightness += brightness_increment
if sys.argv[1] == 'down':
	if current_brightness > brightness_increment:
		current_brightness -= brightness_increment

#Persist current brightness to disk
with open(pickle_filepath, 'w') as pickle_handle:
	pickle.dump(current_brightness, pickle_handle)


#Calculate new colour temp
dimming_factor = (1.0 - current_brightness) * 10
print dimming_factor
new_temp = max_colour_temp - (dimming_factor * temp_reduction_increment)
print new_temp

#Apply current brightness
#eg: redshift -o -l 0:0 -m randr -t 4000:4000 -b 1.0
call(["redshift", "-o", "-l", "0:0", "-m", "randr", "-t", str(new_temp)+":"+str(new_temp), "-b", str(current_brightness)])


