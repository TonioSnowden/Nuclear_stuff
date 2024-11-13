import openmc
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

def create_and_run_model(pu239_concentration, total_time=10):
    pu240_concentration = 1 - pu239_concentration
    
    # Create Pu mix material
    pu_mix = openmc.Material(name='Pu-Mix')
    pu_mix.add_nuclide('Pu239', pu239_concentration)
    pu_mix.add_nuclide('Pu240', pu240_concentration)
    pu_mix.set_density('g/cm3', 19.8)
    
    materials = openmc.Materials([pu_mix])
    
    # Geometry
    sphere = openmc.Sphere(r=1.0, boundary_type='vacuum')
    cell = openmc.Cell(fill=pu_mix, region=-sphere)
    universe = openmc.Universe(cells=[cell])
    geometry = openmc.Geometry(universe)
    
    # Energy distribution
    pu239_watt = openmc.stats.Watt(a=0.885247, b=3.802690)
    pu240_watt = openmc.stats.Watt(a=0.794930, b=4.689270)
    
    lambda_239 = np.log(2)/(24110*365.25*24*3600)
    lambda_240 = np.log(2)/(6561*365.25*24*3600)
    
    expected_decays_239 = 37000 * np.exp(lambda_239 * 31557600) * total_time * pu239_concentration
    expected_decays_240 = 37000 * np.exp(lambda_240 * 31557600) * total_time * pu240_concentration
    expected_decays = expected_decays_239 + expected_decays_240
    
    source = openmc.IndependentSource()
    source.time = openmc.stats.Uniform(0, total_time)
    source.angle = openmc.stats.Isotropic()
    source.space = openmc.stats.Point((0, 0, 0))
    source.energy = openmc.stats.Mixture(
        probability=[pu239_concentration, pu240_concentration],
        distribution=[pu239_watt, pu240_watt]
    )
    source.particle = "neutron"
    
    # Settings
    settings = openmc.Settings()
    settings.run_mode = 'fixed source'
    settings.batches = 100
    settings.particles = int(expected_decays)
    settings.source = source
    
    # Tallies
    time_bins = np.linspace(0, total_time, 10000000)
    time_filter = openmc.TimeFilter(time_bins)
    
    tally = openmc.Tally()
    tally.scores = ['nu-fission']
    tally.filters = [openmc.CellFilter(cell), time_filter]
    
    tallies = openmc.Tallies([tally])
    
    model = openmc.model.Model(geometry, materials, settings, tallies)
    sp_filename = model.run()
    
    return sp_filename

def process_feynman_histogram(time_events, gate_width=2):
    mean_data = time_events['mean']
    windows = np.lib.stride_tricks.sliding_window_view(mean_data[1:], gate_width)
    counts_per_gate = np.sum(windows, axis=1)
    return counts_per_gate

def analyze_concentration(pu239_concentration, total_time=10):
    print(f"\nAnalyzing Pu-239 concentration: {pu239_concentration*100}%")
    
    sp_filename = create_and_run_model(pu239_concentration, total_time)
    
    with openmc.StatePoint(sp_filename) as sp:
        tally_result = sp.get_tally()
        df = tally_result.get_pandas_dataframe()
        
        time_values = df['time low [s]']
        mean_values = df['mean'] * 100000
        
        event_times = pd.DataFrame({
            'time': time_values,
            'mean': mean_values
        })
        
        num_iterations = 16
        y_values = []
        
        # Create directory for this concentration if it doesn't exist
        dir_name = f"results_Pu239_{pu239_concentration*100:.0f}percent"
        os.makedirs(dir_name, exist_ok=True)
        
        # Feynman histograms
        fig = plt.figure(figsize=(20, 20))
        
        for i in range(num_iterations):
            gate_width = 2 ** (i + 1)
            counts = process_feynman_histogram(event_times, gate_width=gate_width)
            counts = counts.round(2)
            
            n = len(counts)
            mean = sum(counts) / n
            squared_diff_sum = sum((x - mean) ** 2 for x in counts)
            variance = squared_diff_sum / n
            Y = (variance / mean) - 1
            y_values.append(Y)
            
            ax = fig.add_subplot(5, 4, i + 1)
            hist, bins, _ = ax.hist(counts, bins=30, density=True, alpha=0.7)
            ax.set_xlabel('Counts outcome')
            ax.set_ylabel('Total counts')
            ax.set_title(f'Gate width={gate_width}\nY={Y:.3f}\nMean={mean:.2f}\nVar={variance:.2f}')
            ax.grid(True)
        
        plt.tight_layout()
        plt.savefig(f'{dir_name}/feynman_histograms.png', dpi=300)
        plt.close()
        
        # Variance/mean vs gate width plot
        plt.figure(figsize=(10, 6))
        gate_widths = [2 ** (i + 1) for i in range(num_iterations)]
        plt.semilogx(gate_widths, y_values, 'bo-')
        plt.xlabel('Gate width')
        plt.ylabel('Variance/Mean - 1 (Y)')
        plt.title(f'Feynman-Y vs Gate Width (Pu-239: {pu239_concentration*100}%)')
        plt.grid(True)
        plt.savefig(f'{dir_name}/feynman_Y_vs_gate_width.png', dpi=300)
        plt.close()
        
        return y_values, gate_widths

def main():
    # Test various concentrations
    concentrations = [0.01, 0.05, 0.10, 0.30, 0.50, 0.70, 0.90, 0.95, 0.99]
    all_y_values = []
    
    for conc in concentrations:
        y_values, gate_widths = analyze_concentration(conc)
        all_y_values.append(y_values)
    
    # Create comparison plot
    plt.figure(figsize=(12, 8))
    for i, conc in enumerate(concentrations):
        plt.semilogx(gate_widths, all_y_values[i], 'o-', 
                    label=f'Pu-239: {conc*100}%')
    
    plt.xlabel('Gate width')
    plt.ylabel('Variance/Mean - 1 (Y)')
    plt.title('Feynman-Y vs Gate Width - Concentration Comparison')
    plt.legend()
    plt.grid(True)
    plt.savefig('concentration_comparison.png', dpi=300)
    plt.close()

if __name__ == "__main__":
    main()