import numpy as np
from glob import glob

# variables
sourceDirectory = "/N/dc2/scratch/kevrusse/output"
outputDirectory = "/N/dc2/scratch/kevrusse/output/grids/"
fileList = glob(sourceDirectory + '/*.txt')
  
fileLAS = ""
delimiter = ';'
comments = '#'

xres = 1.0
yres = 1.0

# File name of the slope grid 
slopegrid = outputDirectory + "slope.asc" 
print slopegrid
# File name of the aspect grid 
aspectgrid = outputDirectory + "aspect.asc" 
# Output file name for shaded relief 
shadegrid = outputDirectory + "relief.asc" 
## Shaded elevation parameters 
# Sun direction
azimuth = 315.0
# Sun angle 
altitude = 45.0 
# Elevation exageration 
z = 1.0 
# Resolution 
scale = 1.0 
# No data value for output 
NODATA = -9999 
# Needed for numpy conversions 
deg2rad = 3.141592653589793 / 180.0 
rad2deg = 180.0 / 3.141592653589793


# Loop through text files created by LAStools and create numpy arrays from variables, skip header rows.
print "creating preliminary array"
prelimArray = [np.loadtxt(fileLAS, comments=comments, delimiter=delimiter, skiprows=19) for fileLAS in fileList]
# Then append the arrays to a new final array
print "creating final array"
myArray = np.concatenate(prelimArray)

print "created array"
print myArray[0]

# create search window for slope function
window = []
for row in range(3):
    for col in range(3):
        window.append(myArray[row:(row + myArray.shape[0] - 2), col:(col + myArray.shape[1] - 2)])

# process each cell
x = ((z * window[0] + z * window[3] + z * window[3] + z * window[6]) - (z * window[2] + z * window[5] + z * window[5] + z * window[8])) / (8.0 * xres * scale);

y = ((z * window[6] + z * window[7] + z * window[7] + z * window[8]) - (z * window[0] + z * window[1] + z * window[1] + z * window[2])) / (8.0 * yres * scale);

# calculate surfaces
slope = 90.0 - np.arctan(np.sqrt(x*x + y*y)) * rad2deg
print "created slope"
aspect = np.arctan2(x, y)
print "...and aspect..."
shaded = np.sin( altitude * deg2rad) * np.sin( slope * deg2rad) + np.cos( altitude * deg2rad) * np.cos( slope * deg2rad) * np.cos(( azimuth - 90.0) * deg2rad - aspect);
shaded = shaded * 255
print "finished shaded relief"

with open(slopegrid, "wb") as f:
	np.savetxt(f, slope, fmt="%4i") 
print "saved slope"

with open(aspectgrid, "wb") as f:
	np.savetxt(f, aspect, fmt="%4i")
print "saved aspect"

with open(shadegrid, "wb") as f:
	np.savetxt(f, shaded, fmt="%4i")
print "saved shaded relief"
