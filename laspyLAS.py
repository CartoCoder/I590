from laspy.file import File
import numpy as np
sourceDirectory = "/N/dc2/scratch/kevrusse/output"
outputDirectory = "/N/dc2/scratch/kevrusse/output/grids/"
fileList = glob(sourceDirectory + '/*.txt')
target = laspyLAS.asc
cell = 1.0
NODATA = 0
source = "/N/dc2/scratch/kevrusse/Karst/data/Benton/in2013_28251900_12.las"
las = File(source, mode="r")
min = las.header.min
max = las.header.max
xdist = max[0] - min[0]
ydist = max[1] - min[1]
cols = int(xdist)/cell
rows = int(ydist)/cell
cols += 1
rows += 1

count = np.zeros((rows, cols)).astype(np.float32)
zsum = np.zeros((rows, cols)).astype(np.float32)
ycell = -1*cell

projx = (las.x - min[0])/cell
projy = (las.y - min[1])/ycell

ix = projx.astype(np.int32)
iy = projy.astype(np.int32)

for x,y,z in np.nditer([ix, iy, las.z]):
    count[y, x]+=1
    zsum[y, x]+=z

nonzero = np.where(count>0, count, 1)
zavg = zsum/nonzero

mean = np.ones((rows, cols)) * np.mean(zavg)
left = np.roll(zavg, -1, 1)
lavg = np.where(left>0, left, mean)
right = np.roll(zavg, 1, 1)
ravg = np.where(right>0, right, mean)
interpolate = (lavg + ravg)/2
fill = np.where(zavg>0, zavg, interpolate)

header = "ncols %s\ n" % fill.shape[1] 
header += "nrows %s\ n" % fill.shape[0] 
header += "xllcorner %s\ n" % min[0] 
header += "yllcorner %s\ n" % min[1] 
header += "cellsize %s\ n" % cell 
header += "NODATA_value %s\ n" % NODATA

with open(target, "wb") as f:
    f.write(header)
    np.savetxt(f, fill, fmt="%1.2f")
