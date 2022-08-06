#!/bin/bash

#SBATCH --job-name="test-job"
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=10M
#SBATCH --time=01:00:00


echo "test-job"

sleep 5

echo "again test job stuff"

sleep 3000



