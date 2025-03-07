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

echo "source_file,fuel_density,coolant_density,radius,number_of_particles,particle_times" > particle_times_output.csv

# Define base constants
ISOTOPES_DENSITY=19.5  # Base density value for isotopes
AIR_DENSITY=0.001      # Base density value for air
HDPE_DENSITY=0.95      # Base density value for HDPE
SPHERE_RADIUS=1.0      # Base sphere radius value

# First run all combinations with pu240source.py
echo "Running simulations with pu240source.py..."
for density_offset in $(seq -0.5 0.1 0.1); do
    density=$(echo "$ISOTOPES_DENSITY + $density_offset" | bc -l)
    for air_density_offset in $(seq -0.5 0.1 0.1); do
        air_density=$(echo "$AIR_DENSITY + $air_density_offset" | bc -l)
        for radius in $(seq 0.5 0.5 5.0); do
            for particles in 10 100 250 500 1000; do
                echo "Running simulation with pu240source.py: density=$density, air_density=$air_density, radius=$radius, particles=$particles"
            
                # Update the parameters in the config.json file
                jq --arg density "$density" --arg air_density "$air_density" --arg radius "$radius" --arg particles "$particles" \
                '.density = ($density | tonumber) | .air_density = ($air_density | tonumber) | .radius = ($radius | tonumber) | .particles = ($particles | tonumber)' \
                config.json > tmp.json && mv tmp.json config.json
                
                # Run the OpenMC simulation
                apptainer exec --bind /global/scratch/users/toniooppi/nuclear_data:/nuclear_data /global/scratch/users/toniooppi/openmc_latest.sif python pu240source.py
                
                # Run the OpenMC tally command
                apptainer exec --bind /global/scratch/users/toniooppi/nuclear_data:/nuclear_data /global/scratch/users/toniooppi/openmc_latest.sif openmc -t
                
                # Run the analysis script
                apptainer exec --bind /global/scratch/users/toniooppi/nuclear_data:/nuclear_data /global/scratch/users/toniooppi/openmc_latest.sif python plot_track.py "pu240source.py" "$density" "$air_density" "$radius" "$particles"
            done
        done
    done
done

# Now run all combinations with pu240sourceair.py
echo "Running simulations with pu240sourceair.py..."
for density_offset in $(seq -0.5 0.1 0.1); do
    density=$(echo "$ISOTOPES_DENSITY + $density_offset" | bc -l)
    for hdpe_density_offset in $(seq -0.5 0.1 0.1); do
        hdpe_density=$(echo "$HDPE_DENSITY + $hdpe_density_offset" | bc -l)
        for radius in $(seq 0.5 0.5 5.0); do
            for particles in 10 100 250 500 1000; do
                echo "Running simulation with pu240sourceair.py: density=$density, air_density=$hdpe_density, radius=$radius, particles=$particles"
            
                # Update the parameters in the config.json file
                jq --arg density "$density" --arg air_density "$air_density" --arg radius "$radius" --arg particles "$particles" \
                '.density = ($density | tonumber) | .air_density = ($hdpe_density | tonumber) | .radius = ($radius | tonumber) | .particles = ($particles | tonumber)' \
                config.json > tmp.json && mv tmp.json config.json
                
                # Run the OpenMC simulation
                apptainer exec --bind /global/scratch/users/toniooppi/nuclear_data:/nuclear_data /global/scratch/users/toniooppi/openmc_latest.sif python pu240sourceair.py
                
                # Run the OpenMC tally command
                apptainer exec --bind /global/scratch/users/toniooppi/nuclear_data:/nuclear_data /global/scratch/users/toniooppi/openmc_latest.sif openmc -t
                
                # Run the analysis script
                apptainer exec --bind /global/scratch/users/toniooppi/nuclear_data:/nuclear_data /global/scratch/users/toniooppi/openmc_latest.sif python plot_track.py "pu240sourceair.py" "$density" "$air_density" "$radius" "$particles"
            done
        done
    done
done