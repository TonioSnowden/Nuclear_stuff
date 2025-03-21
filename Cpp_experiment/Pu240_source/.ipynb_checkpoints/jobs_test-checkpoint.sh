#!/bin/bash
#SBATCH --job-name=dataset_test_creation
#SBATCH --account=fc_neutronix
#SBATCH --partition=savio4_gpu  # Partition (queue) name
#SBATCH --nodes=1                  # Number of nodes
#SBATCH --ntasks=1                 # Number of tasks (processes)
#SBATCH --cpus-per-task=4         # Number of CPU cores per task
#SBATCH --mem=16G                  # Memory per node (16 GB)
#SBATCH --gres=gpu:A5000:1
#SBATCH --time=02:00:00           # Time limit hrs:min:sec
#SBATCH --output=logs/%j.log           # Standard output log
#SBATCH --error=logs/%j.err            # Standard error log
#SBATCH --mail-type=END,FAIL      # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=tonio_oppi@berkeley.edu  # Where to send mail

module load python/3.11

echo "source_file,fuel_density,coolant_density,radius,particle_times" > particle_times_output.csv

fuel_density = 19.5
coolant_density = HDPE_DENSITY
radius density = 1.0

jq --arg fuel_density "$fuel_density" --arg coolant_density "$coolant_density" --arg radius "$radius" \
'.fuel_density = ($fuel_density | tonumber) | .coolant_density = ($coolant_density | tonumber) | .radius = ($radius | tonumber)' \
config.json > tmp.json && mv tmp.json config.json
            
# Run the OpenMC simulation
apptainer exec --bind /global/scratch/users/toniooppi/nuclear_data:/nuclear_data /global/scratch/users/toniooppi/openmc_latest.sif python pu240source.py

# Run the OpenMC tally command
apptainer exec --bind /global/scratch/users/toniooppi/nuclear_data:/nuclear_data /global/scratch/users/toniooppi/openmc_latest.sif openmc -t

# Run the analysis script
apptainer exec --bind /global/scratch/users/toniooppi/nuclear_data:/nuclear_data /global/scratch/users/toniooppi/openmc_latest.sif python plot_track.py "pu240source.py" "$fuel_density" "$coolant_density" "$radius"