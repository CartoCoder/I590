#!/bin/bash
#PBS -k o
#PBS -M kevrusse@indiana.edu
#PBS -m abe
#PBS -N ProcessText2DEM
#PBS -l nodes=1:ppn=2,pmem=2gb,walltime=04:00:00
#PBS -o output.$PBS_JOBID

cd /N/u/kevrusse/Karst/scripts
python ProcessText2DEM.py
