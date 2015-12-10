#!/bin/sh
#PBS -N ProcessLas2Txt
#PBS -l nodes=1:ppn=4,pmem=4gb,walltime=01:00:00
#PBS -M kevrusse@indiana.edu
#PBS -m ae
#PBS -o output.$PBS_JOBID

module load lastools/1.0
cd /N/u/kevrusse/Karst/data/Benton
las2txt -i *.las -parse xyz -sep semicolon -header pound -odir /N/dc2/scratch/kevrusse/output

