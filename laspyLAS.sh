#!/bin/bash
#PBS -k o
#PBS -M kevrusse@indiana.edu
#PBS -m abe
#PBS -N laspyLAS
#PBS -l nodes=1:ppn=2,pmem=2gb,walltime=00:60:00
#PBS -o output.$PBS_JOBID

cd /N/u/kevrusse/Karst/scripts
pip install laspy
python laspyLAS.py
