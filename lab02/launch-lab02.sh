#!/bin/bash -l

#SBATCH --job-name="ar-lab02"
#SBATCH --account plgar2023-cpu
#SBATCH --partition plgrid

#SBATCH --output="/net/ascratch/people/plgwciezobka/Logs/ar-lab02/%j-%x-output.out"
#SBATCH --error="/net/ascratch/people/plgwciezobka/Logs/ar-lab02/%j-%x-error.err"

#SBATCH --time=00:10:00
#SBATCH --nodes 1
#SBATCH --tasks-per-node=4

module load scipy-bundle/2021.10-intel-2021b

export SLURM_OVERLAP=1
GITREPO="ar2023"

cd $SCRATCH/Files/GitRepos/$GITREPO/lab02
mpiexec ./parallel.py 1000
