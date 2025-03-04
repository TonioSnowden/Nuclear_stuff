#!/bin/bash
#SBATCH --job-name=munier_neuralnet_top10
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

source uppsala_env/bin/activate

# Run the OpenMC simulation with varying parameters
for density in 19.1 19.5 20.0; do
    for radius in 0.5 1.0 1.5; do
        for particles in 10 100 1000; do
            # Update the parameters in the Python script
            sed -i "s/pu240.set_density('g\/cm3', .*/pu240.set_density('g\/cm3', $density)/" Nuclear_stuff/Cpp_experiment/Pu240_source/pu240source.py
            sed -i "s/sphere = openmc.Sphere(r=.*/sphere = openmc.Sphere(r=$radius)/" Nuclear_stuff/Cpp_experiment/Pu240_source/pu240source.py
            sed -i "s/settings.particles = .*/settings.particles = $particles/" Nuclear_stuff/Cpp_experiment/Pu240_source/pu240source.py
            
            # Run the OpenMC simulation
            apptainer exec --bind /global/scratch/users/toniooppi/nuclear_data:/nuclear_data /global/scratch/users/toniooppi/openmc_latest.sif python Nuclear_stuff/Cpp_experiment/Pu240_source/pu240source.py
            
            # Run the OpenMC tally command
            apptainer exec --bind /global/scratch/users/toniooppi/nuclear_data:/nuclear_data /global/scratch/users/toniooppi/openmc_latest.sif openmc -t
            
            # Run the analysis script
            python Nuclear_stuff/Cpp_experiment/Pu240_source/plot_track.py
        done
    done
done

# After all simulations, create the dataset
python create_dataset.py